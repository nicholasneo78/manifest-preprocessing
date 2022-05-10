#!/bin/bash

python3 ../task_generate_manifest.py \
    --project_name "audio_preproc_test" \
    --task_name "jtubespeech_small_manifest_generation" \
    --dataset_name "jtubespeech_small" \
    --output_url "s3://experiment-logging" \
    --dataset_project "datasets/jtubespeech" \
    --dataset_task_id "0fa205ad8cd2487aaebadd00e9d01667" \
    --manifest_filename "manifest.json" \
    --queue "cpu-only" \
    --got_annotation \