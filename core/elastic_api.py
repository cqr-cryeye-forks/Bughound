import requests

from core import arguments
from core.config import elastic_host
from core.functions.print_output import print_error, print_success
from core.functions.verify import check_project
from core.shipper import fix_disk_read_only, verify_connection, check_index, create_index, create_index_pattern


def check_elastic_connection() -> None:
    if not arguments.name:
        print_error("please use -n/--name argument to specify Elasticsearch project name!")
        exit()
    if verify_connection():
        # Check if index existed
        if not check_index():
            create_index()
            create_index_pattern()
            print_success("Setup ELK stack configuration for you ..")
            # import_dashboards()
        else:
            # Check if the project name is already used
            if check_project(arguments.name):
                print_error(f"Project name {arguments.name} already used.\nPlease change it")
                exit()

            fix_disk_read_only()
            print_success("ELK is already configured!")
    else:
        print_error("please check connection to Elasticsearch")
        exit()


def ship_entry(project_name: str, entry: dict, verbose: bool):
    # print(entry)
    if not entry:
        print_error('No data for sending to Elasticsearch')
        return
    if verbose:
        filename = entry[project_name]["filename"]
        category = entry[project_name]["category"]
        function = entry[project_name]["function"]
        sha512_hash = entry[project_name]["sha512_hash"]
        timestamp = entry[project_name]["timestamp"]
        extension = entry[project_name]["extension"]
        line = entry[project_name]["line"]
        line_number = entry[project_name]["line_number"]

        data = {
            "project": project_name,
            "category": category,
            "filename": filename,
            "function": function,
            "extension": extension,
            "sha512_hash": sha512_hash,
            "timestamp": timestamp,
            "line": line,
            "line_number": line_number
        }
        request_url = elastic_host + "findings" + "/_doc"
        request = requests.post(request_url, json=data)
        print_success(request.text)
