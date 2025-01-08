#!/bin/sh
# run_dvc_pipeline.sh

set -e

# Run the DVC pipeline
dvc pull -r myremote --force
dvc repro
dvc push -r myremote
