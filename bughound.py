#!/usr/bin/python

import time

from core import arguments
from core.functions import print_banner, print_help_message, check_language, print_error, check_extension, \
    print_success, check_project, get_files, print_url, clone_repo
from core.parser import Parser
from core.shipper import verify_connection, check_index, create_index, create_index_pattern, fix_disk_read_only, \
    get_total_findings

print_banner()
print_help_message()


local_path = arguments.path
git_repo = arguments.git
language = arguments.language
extension = arguments.extension
project_name = arguments.name
verbose = arguments.verbose

start_time = time.time()

if not check_language(language):
    print_error("Language %s not supported!" % language)
    exit()

if not check_extension(extension):
    print_error("Extension should start with .")
    print_error("Example : .java, .php")
    exit()

# Check connection to Elastic
if verify_connection():
    # Check if index existed
    if not check_index():
        create_index()
        create_index_pattern()
        print_success("Setup ELK stack configuration for you ..")
        # import_dashboards()
    else:
        # Check if the project name is already used
        if check_project(project_name):
            print_error("Project name %s already used" % project_name)
            print_error("Please change it")
            exit()

        fix_disk_read_only()
        print_success("ELK is already configured!")
else:
    print_error("please check connection to Elasticsearch")
    exit()

if git_repo is None and local_path:
    files = get_files(local_path, extension)
    for file in files:
        p = Parser(file, project_name, language)
        file_metadata = p.calculate_meta_data()
        findings = p.get_functions(verbose)

    total_findings_to_print = get_total_findings()
    print_url(project_name, start_time, total_findings_to_print)

if local_path is None and git_repo:
    # Use git repo
    clone_repo(git_repo, project_name)
    files = get_files("projects/%s" % project_name, extension)
    for file in files:
        p = Parser(file, project_name, language)
        file_metadata = p.calculate_meta_data()
        functions = p.get_functions(verbose)

    total_findings_to_print = get_total_findings()
    print_url(project_name, start_time, total_findings_to_print)

if local_path is None and git_repo is None:
    print_error("please specify the git repo or local path to scan")
    exit()
