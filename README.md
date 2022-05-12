# Manifest Preprocessing
A repository that generates a manifest from the audio and the annotations dataset.   
  
## Introduction

### Methods of Executing the Code
There will be two methods of executing the code, they are:  
- [Executing code on local machine](#executing-code-on-local-machine)  
- [Executing code on ClearML](#executing-code-on-clearml)    

### Tasks
The tasks is as follow:  
1. Generation Manifest - [Local](#generate-manifest-on-local-machine) | [ClearML](#generate-manifest-on-clearml)   
  
## Project Organization 
There are some folders that needs to be created by the user to store the datasets (audio and annotations). **The instructions will be shown below in the repository structure on what needs to be created by the user.**   

The repository structure will be as shown below:  
```
.
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── tasks
    ├── preprocessing
    |   ├── <PUT YOUR DATASET FOLDERS HERE> 
    │   └── generate_manifest.py
    ├── scripts
    │   └── task_librispeech.sh
    └── task_generate_manifest.py
```
The structure of the dataset required by user will be shown below:  
```
<YOUR DATASET FOLDER>
├── train   
│   └── <your audio files (audio files can be in nested folder form also)> 
├── dev    
│   └── <your audio files (audio files can be in nested folder form also)> 
└── test     
    └── <your audio files (audio files can be in nested folder form also)>
```

# Executing code on local machine
**The documentations below are for running the code using local machine, please go to the section on [Executing code on ClearML](#executing-code-on-clearml) if you want to run your code on ClearML**    
1. Ensure that docker is installed in your computer
2. Clone this repository
```shell
git clone https://github.com/nicholasneo78/manifest-preprocessing
```
3. Open the terminal and go to the root directory of this repository
4. Build the Dockerfile that is created in the repository using the docker-compose.yml file
```shell
docker-compose up --build -d
```
5. After building the docker image, check if the image is successfully built, by typing the following command:  
```shell
docker images
```
You should see the image `manifest-preprocessing` with the tag `v0.1.0` in the list of docker images.  

### Entering the docker image
1. To enter into the docker image to execute codes in the pipeline, execute this command
```shell
docker-compose run local bash
```
The codes are then ready to be executed inside the docker image, more information about executing each code will be discussed below.   

## Generate Manifest on Local Machine
To generate a manifest .json file for the train, dev and test set of the data.  

#### Arguments  
- `root_folder`: (str) the root folder where all the audio files and annotations are found (".wav", ".flac", ".txt", etc.)    
- `manifest_filename`: (str) the filepath and the filename of the generated manifest   
- `got_annotation`: (boolean) whether the manifest includes annotations or not   

#### Return
Filepath of the generated manifest file   
   
#### Before executing the code
Before executing the code, check the script `manifest-preprocessing/tasks/preprocessing/generate_manifest.py`, go to the bottom of the code, after the `if __name__ == "__main__"` line, call the class `GenerateManifest` to do the data preprocessing, here is a code snippet to illustrate the manifest generation:   
```python
get_manifest_train = GenerateManifest(root_folder="./<YOUR DATASET FOLDER>/train/", 
                                      manifest_filename="./librispeech/train/train_manifest.json", 
                                      got_annotation=True) # OR False
train_manifest_path = get_manifest_train()

get_manifest_dev = GenerateManifest(root_folder="./<YOUR DATASET FOLDER>/dev/", 
                                    manifest_filename="./<YOUR DATASET FOLDER>/dev/dev_manifest.json", 
                                    got_annotation=True) # OR False
dev_manifest_path = get_manifest_dev()

get_manifest_test = GenerateManifest(root_folder="./<YOUR DATASET FOLDER>/test/", 
                                     manifest_filename="./<YOUR DATASET FOLDER>/test/test_manifest.json", 
                                     got_annotation=True) # OR False
test_manifest_path = get_manifest_test()
```
  
There will be an example of the code tested on the librispeech dataset in the python script.   
   
#### Executing the code
To execute the data preprocessing code, on the terminal, go to this repository and enter into the docker image (refer above for the command), inside the docker container, type the following command:  
```shell
cd /manifest-preprocessing/tasks/preprocessing
python3 generate_manifest.py
```
<br>
  
# Executing code on ClearML
**The documentations below are for running the code using ClearML, please go to the section on [Executing code on local machine](#executing-code-on-local-machine) if you want to run your code locally**  
  
### Getting Started - Install ClearML and boto3
To install ClearML and boto3, simply do a pip install in your environment:  
```shell
pip install clearml boto3
```

### Getting Started - Uploading the datasets to S3 bucket
Upload the following items to your S3 bucket, either via AWS S3 cli or minio client and monitor it with ClearML dashboard:
- Your datasets (train, dev and test)   

## Generate Manifest on ClearML
To generate a manifest .json file for the train, dev and test set of the data.   

#### Arguments
- `docker_image`: (str) the docker image used to load all the dependencies 
- `project_name`: (str) the clearml project name   
- `task_name`: (str) clearml task name     
- `dataset_name`: (str) name of the output dataset produced    
- `output_url`: (str) the clearml url that the task will be output at    
- `dataset_project`: (str) the clearml path which the datasets resides   
- `dataset_task_id`: (str) the task id to retrieve the dataset   
- `train_manifest_filename`: (str) the train manifest filename and directory to store it   
- `dev_manifest_filename`: (str) the dev manifest filename and directory to store it   
- `test_manifest_filename`: (str) the test manifest filename and directory to store it   
- `got_annotation`: (boolean) if annotation is needed in the .json file   
- `queue`: (str) the queue name for clearml   

#### What is produced  
The train, dev and test manifest files will be produced in the s3 bucket and shown in ClearML, depending on the defined n and where you put your dataset_project location.   

#### Before executing the code
Before executing the code, create a script identical to the example given on `generate-manifest/tasks/scripts/task_librispeech.sh` but with your own inputs. Here is a code snippet to illustrate the executed task:    
```shell
python3 ../task_generate_manifest.py \
    --docker_image "nicholasneo78/manifest_preprocessing:latest"
    --project_name "<YOUR_PROJECT_NAME>" \
    --task_name "<YOUR_TASK_NAME>" \
    --dataset_name "<YOUR_DATASET_NAME>" \
    --output_url "<OUTPUT_URL_TO_YOUR_S3_BUCKET>" \
    --dataset_project "<PATH_TO_YOUR_CLEARML_DATASET>" \
    --dataset_task_id "<YOUR_DATASET_TASK_ID>" \
    --train_manifest_filename "train_manifest.json" \
    --dev_manifest_filename "dev_manifest.json" \
    --test_manifest_filename "test_manifest.json" \
    --queue "<YOUR_CLEARML_QUEUE>" \
    --got_annotation \
```
Do not put the flag --got_annotation if you do not want the annotations to be in the generated manifest file. There will be an example of the code tested on the librispeech dataset in the bash script.    
  
#### Executing the code
To execute the code, on the terminal, go to this repository and type the following command:  
```shell
cd tasks/scripts
chmod 777 <YOUR_SCRIPT_FILE>.sh
./<YOUR_SCRIPT_FILE>.sh
```
<br>
