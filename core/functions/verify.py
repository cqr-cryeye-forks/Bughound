import json
import os

import requests

from core.config import elastic_host, default_index
from core.functions.print_output import print_error


def check_path(path):
    if os.path.exists(path) is not False:
        return True
    print_error("[-]path not exist")
    exit()


def check_project(project_name):
    full_url = elastic_host + default_index + "/_search"
    data = {
        "query": {
            "term": {
                "project": {
                    "value": project_name
                }
            }
        }
    }
    req = requests.get(full_url, json=data)
    response = req.text
    value = json.loads(response)["hits"]["total"]["value"]
    return value != 0