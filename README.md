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
There are some folders that needs to be created by the user to store the datasets (audio and annotations). **The instructions will be shown below in the repository structure on what needs to be created by the user**.  

The repository structure will be as shown below:  
```script
.
├── clearml.conf
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── tasks
    ├── preprocessing
    │   └── generate_manifest.py
    ├── scripts
    │   ├── task_jtubespeech_small.sh
    │   └── task_librispeech.sh
    └── task_generate_manifest.py

```
