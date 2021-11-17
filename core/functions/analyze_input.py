import json

from core import arguments
from core.config import data_file
from core.functions.print_output import print_error, print_note


def check_extension(extension: str):
    return extension[0] == "."


def get_lang_extension():
    if arguments.language == 'php':
        print_note('Use default extension for php: .php')
        return '.php'
    elif arguments.language == 'java':
        print_note('Use default extension for java: .java')
        return '.java'
    else:
        print_error("Unknown extension! PHP and Java are supported")


def get_extension() -> str:
    if arguments.extension:
        if check_extension(arguments.extension):
            return arguments.extension
        print_error("Extension should start with .")
        print_error("Example : .java, .php")
        exit()
    return get_lang_extension()


def check_language(language):
    fi = open(data_file, "r")
    data = fi.read()
    json_data = dict(json.loads(data))
    languages = json_data.keys()
    return language in languages


def get_project_name() -> str:
    if arguments.name:
        return arguments.name
    else:
        return ''
