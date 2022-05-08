#!/bin/bash

python3 ../task_generate_manifest.py \
    --project_name "audio_preproc_test" \
    --task_name "librispeech_manifest_generationn" \
    --dataset_name "librispeech" \
    --output_url "s3://experiment-logging" \
    --dataset_project "datasets/librispeech" \
    --dataset_task_id "159b42223f4c46f89564ef51b251b2d2" \
    --manifest_filename "manifest.json" \
    --queue "cpu-only" \
    --got_annotation \
