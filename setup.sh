#!/bin/bash
env=./"env"
python3 -m venv "${env}"
source $env/bin/activate
$env/bin/pip install -r requirements.txt

