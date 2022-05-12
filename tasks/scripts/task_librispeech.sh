#!/bin/bash

python3 ../task_generate_manifest.py \
    --project_name "audio_preproc_test" \
    --task_name "librispeech_manifest_generationn" \
    --dataset_name "librispeech" \
    --output_url "s3://experiment-logging" \
    --dataset_project "datasets/librispeech" \
    --dataset_task_id "8efc2eb60e954b07857af7e9533f1639" \
    --train_manifest_filename "train_manifest.json" \
    --dev_manifest_filename "dev_manifest.json" \
    --test_manifest_filename "test_manifest.json" \
    --queue "compute" \
    --got_annotation \
