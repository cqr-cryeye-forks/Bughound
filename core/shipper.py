#!/usr/bin/python

import requests

from core.config import *

# Create findings index

# Map findings index fields

# Import the dashboards

# Ship the findings


def verify_connection():
    # Check connection to elastic search
    try:
        req = requests.get(elastic_host)
        return req.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def check_index():
    # Check if index exists
    # True if index exists
    # False if index not exists

    request_url = elastic_host + default_index
    request = requests.get(request_url)
    return request.status_code == 200


# curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d
# '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'


# curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d
# '{"index.blocks.read_only_allow_delete": null}'

def fix_disk_read_only():
    data1 = {"transient": {"cluster.routing.allocation.disk.threshold_enabled": "false"}}
    data2 = {"index.blocks.read_only_allow_delete": None}

    request1_url = elastic_host + "_cluster/settings"
    request2_url = elastic_host + "_all/_settings"

    request1 = requests.put(request1_url, json=data1)
    request2 = requests.put(request2_url, json=data2)


def create_index():
    # Create new index
    # Map index files types
    request_url = elastic_host + default_index

    mapping = {
        "settings": {"number_of_shards": 1},
        "mappings": {"properties": {
            "category": {"type": "keyword"},
            "project": {"type": "keyword"},
            "filename": {"type": "keyword"},
            "function": {"type": "keyword"},
            "line": {"type": "text"},
            "timestamp": {"type": "keyword"},
            "extension": {"type": "keyword"},
            "sha512_hash": {"type": "keyword"},
            "line_number": {"type": "keyword"}
        }
        }
    }
    index_request = requests.put(request_url, json=mapping)
    # print(index_request.text)


def create_index_pattern():
    index_pattern_url = "api/saved_objects/index-pattern/" + default_index
    full_index_pattern_url = kibana_host + index_pattern_url
    print(full_index_pattern_url)

    headers = {
        "kbn-xsrf": "true",
        "Content-Type": "application/json"
    }

    data = {
        "attributes": {
            "title": default_index,
        }
    }

    request = requests.post(full_index_pattern_url, json=data, headers=headers)
    print(request.text)

