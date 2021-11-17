from core import arguments
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
