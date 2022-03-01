from clearml import Task, Dataset

PROJECT_NAME = "audio_preproc_test"
TASK_NAME = "librispeech_manifest_generation"
DATASET_NAME = "librispeech"
OUTPUT_URL = "s3://experiment-logging/storage"

task = Task.init(project_name=PROJECT_NAME, task_name=TASK_NAME)
task.set_base_docker(
    docker_images="python:3.8.12-slim-buster",
    docker_setup_bash_script=[
        'apt-get update', 'apt-get upgrade -y', 'apt-get install -y'
        'apt-get -y install apt-utils gcc libpq-dev libsndfile1 ffmpeg',
        'python3 -m pip install librosa numpy pandas'
    ]
)

# librispeech_small dataset_task_id: 092896c34c0e45b598777222d9eaaee6
args = {
    'dataset_task_id': '',
}

task.connect(args)
task.execute_remotely()

from preprocessing.librispeech_data_manifest import LibrispeechManifest

# import dataset
dataset = Dataset.get(dataset_id=args['dataset_task_id'])
dataset_path = dataset.get_local_copy()

# process
