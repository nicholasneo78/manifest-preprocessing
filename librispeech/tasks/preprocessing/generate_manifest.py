# imports
import os
from os.path import join
import numpy as np
import pandas as pd
import json
import librosa
from pathlib import Path
import sys
import argparse

# parsing arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess data to generate pickle data files from the data manifest",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # arguments corresponding to the task initialisation
    parser.add_argument("--dataset_folder",                 type=str, help="the root folder to retrieve the dataset")
    parser.add_argument("--manifest_filename",              type=str, help="the manifest filename and directory to store it")
    parser.add_argument("--got_annotation",                 action='store_true', default=False, help="if annotation is needed in the .json file")   

    return parser.parse_args(sys.argv[1:])

arg = parse_args()

# build a class to produce the librispeech data manifest
class GenerateManifest():
    
    def __init__(self, root_folder, manifest_filename, got_annotation):
        self.root_folder = root_folder
        self.manifest_filename = manifest_filename
        self.got_annotation = got_annotation
    
    # check if the json file name already existed (if existed, need to throw error or else the new json manifest will be appended to the old one, hence causing a file corruption)
    def json_existence(self):
        assert not os.path.isfile(f'{self.manifest_filename}'), "json filename exists! Please remove old json file!"
    
    # helper function to build the lookup table for the id and annotations from all the text files and return the table
    def build_lookup_table(self):
        #initiate list to store the id and annotations lookup
        split_list_frame = []

        # get all the annotations into a dataframe
        for root, subdirs, files in os.walk(self.root_folder):
            for file in files:
                if file.endswith(".txt"):
                    # add on to the code here
                    df = pd.read_csv(os.path.join(root, file), header=None)
                    df.columns = ['name']

                    for i,j in enumerate(df.name):
                        split_list = j.split(" ",1)
                        split_list_frame.append(split_list)

        df_new = pd.DataFrame(split_list_frame, columns=['id', 'annotations']) # id and annotations are just dummy headers here
        return df_new
    
    # helper function to create the json manifest file
    def create_json_manifest(self):
        
        # check if the json filename have existed in the directory
        self.json_existence()
        
        if self.got_annotation:
            # get the lookup table
            df_new = self.build_lookup_table()

        # retrieve the dataframe lookup table
        for root, subdirs, files in os.walk(self.root_folder):
            
            # since self.root_folder is a subset of the root, can just replace self.root with empty string
            modified_root_ = str(Path(root)).replace(str(Path(self.root_folder)), '')
            # replace the slash with empty string after Path standardization
            modified_root = modified_root_.replace('/', '', 1)

            for file in files:
                if file.endswith(".flac"):
                    # retrieve the base path for the particular audio file
                    base_path = os.path.basename(os.path.join(root, file)).split('.')[0]

                    # create the dictionary that is to be appended to the json file
                    if self.got_annotation:
                        data = {
                                'audio_filepath' : os.path.join(modified_root, file),
                                'duration' : librosa.get_duration(filename=os.path.join(root, file)),
                                'text' : df_new.loc[df_new['id'] == base_path, 'annotations'].to_numpy()[0]
                               }
                    else:
                        data = {
                                'audio_filepath' : os.path.join(modified_root, file),
                                'duration' : librosa.get_duration(filename=os.path.join(root, file)),
                               }

                    # write to json file
                    #with open(f'{self.root_folder}{self.manifest_filename}', 'a+', encoding='utf-8') as f:
                    with open(f'{self.manifest_filename}', 'a+', encoding='utf-8') as f:
                        f.write(json.dumps(data) + '\n')
                        # json.dump(data, f, ensure_ascii=False, indent=2)
                        # f.write('\n')

        return f'{self.manifest_filename}'

    def __call__(self):
        return self.create_json_manifest()

if __name__ == '__main__':

    # the directory to the config file with the dataset info that needs to generate the manifest
    #CONFIG_FILE = './config/config_librispeech.yaml'
    # CONFIG_FILE = './config/config_jtubespeech_small.yaml'


    # with open(CONFIG_FILE) as f:
    #     config = yaml.safe_load(f)

    # instantiate GenerateManifest class object
    get_manifest = GenerateManifest(root_folder=arg.dataset_folder, 
                                    manifest_filename=arg.manifest_filename, 
                                    got_annotation=arg.got_annotation)
    get_manifest()

    print('json manifest file created!')
    