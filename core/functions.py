#!/usr/bin/python

import json
import os
import time

from termcolor import cprint

from core.shipper import *


def print_error(text):
    message = f"[-] {text}"
    cprint(message, "red")


def print_note(text):
    message = f"[!] {text}"
    cprint(message, "yellow")


def print_success(text):
    message = f"[+] {text}"
    cprint(message, "green")


def check_path(path):
    if os.path.exists(path) is not False:
        return True
    print_error("[-]path not exist")
    exit()


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


def check_extension(extension):
    return extension[0] == "."


def check_language(language):
    fi = open(data_file, "r")
    data = fi.read()
    json_data = dict(json.loads(data))
    languages = json_data.keys()
    return language in languages


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


def print_banner():
    banner = r'''{0}
.______    __    __    _______  __    __    ______    __    __  .__   __.  _______
|   _  \  |  |  |  |  /  _____||  |  |  |  /  __  \  |  |  |  | |  \ |  | |       \
|  |_)  | |  |  |  | |  |  __  |  |__|  | |  |  |  | |  |  |  | |   \|  | |  .--.  |
|   _  <  |  |  |  | |  | |_ | |   __   | |  |  |  | |  |  |  | |  . `  | |  |  |  |
|  |_)  | |  `--'  | |  |__| | |  |  |  | |  `--'  | |  `--'  | |  |\   | |  '--'  |
|______/   \______/   \______| |__|  |__|  \______/   \______/  |__| \__| |_______/

 {1}

          {2}\ /
          oVo
      \___XXX___/
       __XXXXX__
      /__XXXXX__\
      /   XXX   \
           V{1}                  {3}V1.0 Beta{1}
    '''
    print(banner.format(Colors.YELLOW, Colors.END_COLOR, Colors.RED, Colors.GREEN))


def print_help_message():
    print_success(
        "Example: ./bughound3.py --path vulnerable_code/ --language php --extension .php --name test_project\n")


def print_url(project, start_time, total):
    print_note("Scanning done!")
    end_time = time.time()
    total_time = str(end_time - start_time)[0:5]
    print_note("Total scan time is: %s seconds" % total_time)
    print_note("Total issues found : %s" % total)
    link = "http://localhost:5601/app/dashboards#/view/f2a02140-3b38-11eb-9206-9dc3fa02fbe6?_g=(filters:!()," \
           "refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(description:'',filters:!()," \
           "fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:'project:%22" \
           f"{project}%22'),timeRestore:!f,title:'Bughound%20Main%20Dashboard',viewMode:view)"
    print_success("You can access the project name using this link:")
    print(link)


def get_files(path, extension):
    files_list = []
    if check_path(path):
        print_success("Scanning started!")
        for root, dirs, files in os.walk(path, topdown=False):
            for item in files:
                path_to_file = os.path.join(root, item)
                if path_to_file.endswith(extension):
                    files_list.append(path_to_file)
    return files_list
