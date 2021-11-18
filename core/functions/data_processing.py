import json
import os
from typing import Union

from core import arguments
from core.config import data_file, Colors
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


def get_regex(language):
    fi = open(data_file, "r")
    data = fi.read()
    json_data = dict(json.loads(data))
    return json_data[language]["regex"]


def get_language_data(language):
    fi = open(data_file, "r")
    data = fi.read()
    json_data = dict(json.loads(data))
    return json_data[language]["category"]


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


def convert_findings_to_json(results: list[dict]) -> str:
    findings = [list(result.items())[0][1] for result in results]
    return json.dumps(findings, indent=2)


def convert_findings_to_str(results: list[dict]) -> str:
    findings = ''
    for result in results:
        finding = list(result.items())[0][1]  # [[project_name],[finding]]
        problem_text = f"Found {Colors.YELLOW}{finding['category']}{Colors.END_COLOR}\n" \
                       f"File: {finding['filename']}\n" \
                       f"Line: {finding['line_number']}\n" \
                       f"Code:\n{process_code(finding['line'])}" \
                       '-' * 100
        findings += problem_text
    return findings


def process_code(code: str) -> str:
    lines = code.split('\n')
    middle_of_lines = float(len(lines)) / 2
    if middle_of_lines % 2 != 0:
        lines_to_color = [lines[int(middle_of_lines - .5)]]
    else:
        lines_to_color = [lines[int(middle_of_lines)], lines[int(middle_of_lines - 1)]]
    output_lines = [f'{Colors.RED}{line}{Colors.END_COLOR}' if line in lines_to_color else line for line in lines]
    return '\n'.join(output_lines)


def write_findings_to_file(findings: Union[str, list[dict]], file: str):
    try:
        with open(file, 'w') as path:
            path.write(str(findings))
        print_success(f'All data wrote to file {file}')
    except Exception as e:
        print_error(f'Cannot write data to file {file}: {Exception}')
