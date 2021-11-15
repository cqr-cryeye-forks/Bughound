#!/usr/bin/python3
from pathlib import Path

# Please don't change these options if you will use the docker image
PROJECT_DIR = Path(__file__).parents[1]

elastic_host = "http://localhost:9200/"

kibana_host = "http://localhost:5601/"

default_index = "findings"

data_file = PROJECT_DIR.joinpath("data", "data.json").absolute()


class Colors:
    YELLOW = '\33[33m'
    END_COLOR = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
