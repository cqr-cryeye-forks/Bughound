import json

from core import arguments
from core.config import data_file, Colors


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
                       f'\n{"-"*100}\n'
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


def get_code_with_dispersion(lines: list, line_number: int) -> str:
    dispersion = arguments.dispersion
    line_number -= 1  # lines from 0...n  line_number from 1... n+1 -> Index Error
    code_snippet = lines[line_number]
    for _ in range(dispersion):
        try:
            upper_line = lines[line_number - dispersion]
            under_line = lines[line_number + dispersion]
            code_snippet = f'{upper_line}{code_snippet}{under_line}'
        except IndexError:
            pass
    return code_snippet
