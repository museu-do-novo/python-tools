#!/bin/bash
env=./"env_starckfilmes"
python3 -m venv "${env}"
source $env/bin/activate
$env/bin/pip install requests beautifulsoup4 colorama

