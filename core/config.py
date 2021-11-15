#!/usr/bin/python3
from pathlib import Path

# Please don't change these options if you will use the docker image
PROJECT_DIR = Path(__file__).parents[1]

elastic_host = "http://localhost:9200/"

kibana_host = "http://localhost:5601/"

default_index = "findings"

data_file = PROJECT_DIR.joinpath("data", "data.json").absolute()
