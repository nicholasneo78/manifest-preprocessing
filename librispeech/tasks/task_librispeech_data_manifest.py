from clearml import Task, Dataset

PROJECT_NAME = "audio_preproc_test"
TASK_NAME = "librispeech_manifest_generation"
DATASET_NAME = "librispeech"
OUTPUT_URL = "s3://experiment-logging/storage"

task = Task.init(project_name=PROJECT_NAME, task_name=TASK_NAME)
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
    'dataset_task_id': '092896c34c0e45b598777222d9eaaee6',
    'manifest_filename': 'manifest.json',
    'got_annotation': True,
}
task.connect(args)

# EITHER save it in draft first
#task.execute_remotely()

# Or set to run
task.execute_remotely(queue_name='compute', exit_process=True)

from preprocessing.librispeech_data_manifest import LibrispeechManifest

# import dataset
dataset = Dataset.get(dataset_id=args['dataset_task_id'])
dataset_path = dataset.get_local_copy()

# process
librispeech_manifest = LibrispeechManifest(
    root_folder=dataset_path, 
    manifest_filename=args['manifest_filename'], 
    got_annotation=args['got_annotation']
)

#new_dataset_path = librispeech_manifest()
librispeech_manifest()


# register ClearML Dataset
dataset = Dataset.create(
    dataset_project=PROJECT_NAME, dataset_name=DATASET_NAME
)

#dataset.add_files(new_dataset_path)
dataset.upload(output_url=OUTPUT_URL)
dataset.finalize()

print('Done')