from clearml import Task, Dataset
import yaml

# get task configs - ONLY THING NEEDED TO CHANGE
CONFIG_FILE = './config/config_task_librispeech.yaml'

with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)

# PROJECT_NAME = "audio_preproc_test"
# TASK_NAME = "librispeech_manifest_generation"
# DATASET_NAME = "librispeech"
# OUTPUT_URL = "s3://experiment-logging/storage"
# DATASET_PROJECT = "datasets/librispeech"

PROJECT_NAME = config['project_name']
TASK_NAME = config['task_name']
DATASET_NAME = config['dataset_name']
OUTPUT_URL = config['output_url']
DATASET_PROJECT = config['dataset_project']

task = Task.init(project_name=PROJECT_NAME, task_name=TASK_NAME, output_uri=OUTPUT_URL)
task.set_base_docker(
    docker_image="python:3.8.12-slim-buster",
    docker_setup_bash_script=[
        'apt-get update', 'apt-get upgrade -y', 'apt-get install -y'
        'apt-get -y install apt-utils gcc libpq-dev ffmpeg python3-pandas',
        'apt-get -y install libsndfile1',
        'apt-get -y install python3-pandas',
        'python3 -m pip install pandas librosa numpy==1.21.0'
    ]
)

# librispeech_small dataset_task_id: 092896c34c0e45b598777222d9eaaee6
args = {
    'dataset_task_id': config['dataset_task_id'],
    'manifest_filename': config['manifest_filename'],
    'got_annotation': config['got_annotation'],
}
task.connect(args)

# EITHER save it in draft first
#task.execute_remotely()

# Or set to run
task.execute_remotely(queue_name='services', exit_process=True)

from preprocessing.generate_manifest import CONFIG_FILE, GenerateManifest

# register ClearML Dataset
dataset = Dataset.create(
    dataset_project=DATASET_PROJECT, dataset_name=DATASET_NAME, parent_datasets=[args['dataset_task_id'],]
)

# import dataset
#dataset = Dataset.get(dataset_id=args['dataset_task_id'])
# get_mutable_local_copy() is to write into existing file
# get_local_copy() is to make a copy with the new file
dataset_path = dataset.get_local_copy()

# process
librispeech_manifest = GenerateManifest(
    root_folder=dataset_path, 
    manifest_filename=args['manifest_filename'], 
    got_annotation=args['got_annotation']
)

new_manifest_path = librispeech_manifest()

#librispeech_manifest()

#dataset.add_files(dataset_path)
dataset.add_files(new_manifest_path)
dataset.upload(output_url=OUTPUT_URL)
dataset.finalize()

print('Done')