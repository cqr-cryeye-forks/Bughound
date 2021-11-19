import os
from typing import Union

from core import arguments
from core.functions.print_output import print_error, print_success
from core.functions.verify import check_path


def read_file(file_path):
    if check_path(file_path):
        with open(file_path, "r") as fi:
            data = fi.read()
        return data
    else:
        print_error("File not exist")
        return False


def read_file_lines(file_path):
    if check_path(file_path):
        with open(file_path, "r") as fi:
            file_lines = fi.readlines()
        return file_lines
    else:
        print_error("File not exist")
        return False


def clone_repo(repo_url, project_name):
    # check if git is installed
    check_git = os.popen("which git").read()
    if check_git == "":
        print("Git is not installed")
        exit()

    if not os.path.exists("projects"):
        os.mkdir("projects")
    # clone the repo using git
    command = "git clone %s projects/%s" % (repo_url, project_name)
    print_success("Cloning ..")
    os.system(command)
    print_success("Cloning Done!")


def get_files(path, extension) -> list[str]:
    files_list = []
    if check_path(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for item in files:
                path_to_file = os.path.join(root, item)
                if path_to_file.endswith(extension):
                    files_list.append(path_to_file)
    return files_list


def get_files_for_analyze(extension: str) -> list[str]:
    files = []
    if arguments.path:
        files = get_files(arguments.path, extension)

    if arguments.git:
        # Use git repo
        clone_repo(arguments.git, arguments.name)
        files = get_files("projects/%s" % arguments.name, extension)

    return files


def write_findings_to_file(findings: Union[str, list[dict]], file: str):
    try:
        with open(file, 'w') as path:
            path.write(str(findings))
        print_success(f'All data wrote to file {file}')
    except Exception as e:
        print_error(f'Cannot write data to file {file}: {Exception}')