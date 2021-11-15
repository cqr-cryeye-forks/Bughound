#!/usr/bin/python3

import re
import time
from hashlib import sha512

from core.functions import get_regex, get_language_data, read_file_lines, print_success
from core.shipper import ship_entry

php_final_findings = []
previous_findings = []


class Parser:
    def __init__(self, file, project_name, language):
        self.metadata = {}
        self.project_name = project_name
        self.file = file
        self.language = language

    def calculate_meta_data(self):
        sha512_hash = sha512(self.file.encode()).hexdigest()
        timestamp = time.time()
        extension = self.file.split(".")[1]
        metadata = {
            self.project_name: {
                "filename": self.file,
                "sha512_hash": sha512_hash,
                "timestamp": timestamp,
                "extension": extension,
                "language": self.language
            }
        }
        self.metadata = metadata
        return self.metadata

    # Get unsafe functions from a file
    def get_functions(self, verbose):
        final_findings = []
        metadata_existed = False

        # regex to get all function calls for languages such as php
        # debugging
        # global_regex = "\w+\(.*?\)"

        metadata = self.metadata
        line_number = 0
        # Get the extension based on line #28
        extension = metadata[self.project_name]["extension"]
        language = metadata[self.project_name]["language"]
        regex = get_regex(language)
        categories = get_language_data(language)
        file = self.file
        line_number = 0
        lines = read_file_lines(file)
        data = get_language_data(language)
        # Check if we regex is None == Java
        if regex == "None":
            final_findings = []
            code_snippet = ""
            for line in lines:
                line_number += 1
                for category in data:
                    for function in data[category]:
                        if function in line:
                            self.update_result_data(metadata=metadata,
                                                    category=category,
                                                    function=function,
                                                    line_number=line_number,
                                                    lines=lines,
                                                    verbose=verbose)

        else:
            for line in lines:
                line_number += 1
                for category in data:
                    for function in data[category]:
                        new_regex = regex.format(function)
                        results = re.findall(new_regex, line)
                        if results:
                            self.update_result_data(metadata=metadata,
                                                    category=category,
                                                    function=function,
                                                    line_number=line_number,
                                                    lines=lines,
                                                    verbose=verbose)

    def update_result_data(self, metadata, category, function, line_number: int, lines, verbose):
        metadata[self.project_name]["category"] = category
        metadata[self.project_name]["function"] = function
        if line_number > 3:
            line_number -= 1
            code_snippet = lines[line_number - 3]
            code_snippet += lines[line_number - 2]
            code_snippet += lines[line_number - 1]
            code_snippet += lines[line_number]
            try:
                code_snippet += lines[line_number + 1]
            except IndexError:
                pass
            try:
                code_snippet += lines[line_number + 2]
            except IndexError:
                pass
            try:
                code_snippet += lines[line_number + 3]
            except IndexError:
                pass
        else:
            code_snippet = lines[line_number]

        # print(code_snippet)
        metadata[self.project_name]["line_number"] = line_number
        metadata[self.project_name]["line"] = code_snippet
        if verbose:
            print_success("Shipping entry")
        ship_entry(self.project_name, metadata, verbose)
