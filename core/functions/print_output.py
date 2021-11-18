from termcolor import cprint

from core.config import Colors


def print_error(text):
    message = f"[-] {text}"
    cprint(message, "red")


def print_note(text):
    message = f"[!] {text}"
    cprint(message, "yellow")


def print_success(text):
    message = f"[+] {text}"
    cprint(message, "green")


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
           V{1}                  {3}V1.1 By Zeinlol Beta{1}
    '''
    print(banner.format(Colors.YELLOW, Colors.END_COLOR, Colors.RED, Colors.GREEN))
    # print_help_message()


def print_help_message():
    print_success(
        "Example: ./bughound3.py --path vulnerable_code/ --language php --extension .php --name test_project\n")


def print_url(project):
    link = "http://localhost:5601/app/dashboards#/view/f2a02140-3b38-11eb-9206-9dc3fa02fbe6?_g=(filters:!()," \
           "refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(description:'',filters:!()," \
           "fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:'project:%22" \
           f"{project}%22'),timeRestore:!f,title:'Bughound%20Main%20Dashboard',viewMode:view)"
    print_success("You can access the project name using this link:")
    print(link)


def print_results(results: list[dict]) -> None:

    def process_code(code: str):
        lines = code.split('\n')
        middle_of_lines = float(len(lines)) / 2
        if middle_of_lines % 2 != 0:
            lines_to_color = [lines[int(middle_of_lines - .5)]]
        else:
            lines_to_color = [lines[int(middle_of_lines)], lines[int(middle_of_lines-1)]]
        output_lines = [f'{Colors.RED}{line}{Colors.END_COLOR}' if line in lines_to_color else line for line in lines]
        return '\n'.join(output_lines)

    for result in results:
        finding = list(result.items())[0][1]  # [[project_name],[finding]]
        problem_text = f"Found {Colors.YELLOW}{finding['category']}{Colors.END_COLOR}\n" \
                       f"File: {finding['filename']}\n" \
                       f"Line: {finding['line_number']}\n" \
                       f"Code:\n{process_code(finding['line'])}"
        print(problem_text)
        print('-'*100)
