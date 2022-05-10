from clearml import Task, Dataset
import sys
import argparse

# parsing arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess data to generate pickle data files from the data manifest",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # arguments corresponding to the task initialisation
    parser.add_argument("--project_name",       type=str, help="the clearml project name")
    parser.add_argument("--task_name",          type=str, help="clearml task name")
    parser.add_argument("--dataset_name",       type=str, help="name of the output dataset produced")
    parser.add_argument("--output_url",         type=str, help="the clearml url that the task will be output at")
    parser.add_argument("--dataset_project",    type=str, help="the clearml path which the datasets resides")
    parser.add_argument("--dataset_task_id",    type=str, help="the task id to retrieve the dataset")
    parser.add_argument("--manifest_filename",  type=str, help="the manifest filename and directory to store it")
    parser.add_argument("--got_annotation",     action='store_true', default=False, help="if annotation is needed in the .json file")
    parser.add_argument("--queue",              type=str, help="the manifest filename and directory to store it")

    return parser.parse_args(sys.argv[1:])

arg = parse_args()

PROJECT_NAME = arg.project_name
TASK_NAME = arg.task_name
DATASET_NAME = arg.dataset_name
OUTPUT_URL = arg.output_url
DATASET_PROJECT = arg.dataset_project

task = Task.init(project_name=PROJECT_NAME,
                 task_name=TASK_NAME, output_uri=OUTPUT_URL)
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

args = {
    'dataset_task_id': arg.dataset_task_id,
    'manifest_filename': arg.manifest_filename,
    'got_annotation': arg.got_annotation,
}

task.connect(args)

# set to run
task.execute_remotely(queue_name=arg.queue, exit_process=True)

from preprocessing.generate_manifest import GenerateManifest

# register ClearML Dataset
dataset = Dataset.create(
    dataset_project=DATASET_PROJECT, dataset_name=DATASET_NAME, parent_datasets=[
        args['dataset_task_id']]
)

dataset_path = dataset.get_local_copy()

# process
librispeech_manifest = GenerateManifest(
    root_folder=dataset_path,
    manifest_filename=args['manifest_filename'],
    got_annotation=args['got_annotation']
)

new_manifest_path = librispeech_manifest()

dataset.add_files(new_manifest_path)
dataset.upload(output_url=OUTPUT_URL)
dataset.finalize()

print('Done')
