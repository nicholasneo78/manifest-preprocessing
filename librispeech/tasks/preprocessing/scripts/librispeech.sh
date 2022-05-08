#!/bin/bash

python3 ../generate_manifest.py \
    --dataset_folder "./librispeech_data/" \
    --manifest_filename "./librispeech_data/manifest.json" \
    --got_annotation