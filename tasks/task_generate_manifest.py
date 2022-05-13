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
    parser.add_argument("--docker_image",               type=str, help="the docker image used to load all the dependencies")
    parser.add_argument("--project_name",               type=str, help="the clearml project name")
    parser.add_argument("--task_name",                  type=str, help="clearml task name")
    parser.add_argument("--dataset_name",               type=str, help="name of the output dataset produced")
    parser.add_argument("--output_url",                 type=str, help="the clearml url that the task will be output at")
    parser.add_argument("--dataset_project",            type=str, help="the clearml path which the datasets resides")
    
    parser.add_argument("--dataset_task_id",            type=str, help="the task id to retrieve the dataset")
    parser.add_argument("--train_manifest_filename",    type=str, help="the train manifest filename and directory to store it")
    parser.add_argument("--dev_manifest_filename",      type=str, help="the dev manifest filename and directory to store it")
    parser.add_argument("--test_manifest_filename",     type=str, help="the test manifest filename and directory to store it")
    parser.add_argument("--got_annotation",             action='store_true', default=False, help="if annotation is needed in the .json file")
    
    parser.add_argument("--queue",                      type=str, help="the manifest filename and directory to store it")

    return parser.parse_args(sys.argv[1:])

arg = parse_args()

task = Task.init(project_name=arg.project_name,
                 task_name=arg.task_name, 
                 output_uri=arg.output_url)

task.set_base_docker(
    docker_image=arg.docker_image
)

# set to run
task.execute_remotely(queue_name=arg.queue, exit_process=True)

from preprocessing.generate_manifest import GenerateManifest

# create a new dataset
dataset = Dataset.create(
    dataset_project=arg.dataset_project, 
    dataset_name=arg.dataset_name, 
    parent_datasets=[arg.dataset_task_id]
)

dataset_path = dataset.get_local_copy()


train_manifest = GenerateManifest(root_folder=f'{dataset_path}/train',
                                  manifest_filename=f'train/{arg.train_manifest_filename}',
                                  got_annotation=arg.got_annotation)

dev_manifest = GenerateManifest(root_folder=f'{dataset_path}/dev',
                                manifest_filename=f'dev/{arg.dev_manifest_filename}',
                                got_annotation=arg.got_annotation)
                                
test_manifest = GenerateManifest(root_folder=f'{dataset_path}/test',
                                 manifest_filename=f'test/{arg.test_manifest_filename}',
                                 got_annotation=arg.got_annotation)

train_manifest_path = train_manifest()
dev_manifest_path = dev_manifest()
test_manifest_path = test_manifest()

dataset.add_files(train_manifest_path)
dataset.add_files(dev_manifest_path)
dataset.add_files(test_manifest_path)

dataset.upload(output_url=arg.output_url)
dataset.finalize()

print('Done')
