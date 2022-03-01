# imports
import os
from os.path import join
from tqdm import tqdm
import numpy as np
import pandas as pd
import json
import librosa

# build a class to produce the librispeech data manifest
class LibrispeechManifest():
    
    def __init__(self, root_folder, manifest_filename, got_annotation):
        self.root_folder = root_folder
        self.manifest_filename = manifest_filename
        self.got_annotation = got_annotation
    
    # check if the json file name already existed (if existed, need to throw error or else the new json manifest will be appended to the old one, hence causing a file corruption)
    def json_existence(self):
        assert not os.path.isfile(f'{self.root_folder}{self.manifest_filename}'), "json filename exists! Please remove old json file!"
    
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
            for file in files:
                if file.endswith(".flac"):
                    # retrieve the base path for the particular audio file
                    base_path = os.path.basename(os.path.join(root, file)).split('.')[0]

                    # create the dictionary that is to be appended to the json file
                    if self.got_annotation:
                        data = {
                                'audio_filepath' : os.path.join(root, file),
                                'duration' : librosa.get_duration(filename=os.path.join(root, file)),
                                'text' : df_new.loc[df_new['id'] == base_path, 'annotations'].to_numpy()[0]
                               }
                    else:
                        data = {
                                'audio_filepath' : os.path.join(root, file),
                                'duration' : librosa.get_duration(filename=os.path.join(root, file)),
                               }

                    # write to json file
                    with open(f'{self.root_folder}{self.manifest_filename}', 'a+', encoding='utf-8') as f:
                        f.write(json.dumps(data) + '\n')
                        # json.dump(data, f, ensure_ascii=False, indent=2)
                        # f.write('\n')

if __name__ == '__main__':
    # DEFINING CONSTANTS FOR THE FILE NAMING
    ROOT_FOLDER = './librispeech_data/'
    MANIFEST_FILENAME = 'manifest.json'
    MANIFEST_FILENAME_NO_LABEL = 'manifest_no_annotation.json'
    GOT_ANNOTATION = True

    # instantiate LibrispeechManifest class object
    # with annotation
    get_libri_manifest = LibrispeechManifest(root_folder=ROOT_FOLDER, manifest_filename=MANIFEST_FILENAME, got_annotation=GOT_ANNOTATION)
    
    # without annotation
    #get_libri_manifest_no_label = LibrispeechManifest(root_folder=ROOT_FOLDER, manifest_filename=MANIFEST_FILENAME_NO_LABEL, got_annotation=GOT_ANNOTATION)

    # call the class method to produce the json manifest file
    get_libri_manifest.create_json_manifest()
    #get_libri_manifest_no_label.create_json_manifest()

    print('json manifest file created!')

