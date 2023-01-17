import argparse

parser = argparse.ArgumentParser(description="Example: ./bughound3.py --path vulnerable_code/ --language php "
                                             "--extension .php --name test_project")
parser.add_argument("-p", "--path", help="Local path of the source code")
parser.add_argument("-g", "--git", help="GitHub repository URL")
parser.add_argument("-elk", "--use-elastic", action="store_true",
                    help="initialize Elastic and Kibanna requirements. -n/--name argument required")
parser.add_argument("-l", "--language", required=True, help="Used programming language")
parser.add_argument("-e", "--extension",
                    help="File extension for analyze. Default for Java - .java Default fpr PHP - .php")
parser.add_argument("-n", "--name", help="Project name to use in Elasticsearch and Kibanna")
parser.add_argument("-b", "--branch", help="Git Branch for scan")
parser.add_argument("-v", "--verbose", help="show debugging messages", default=False, required=False,
                    action="store_true")
parser.add_argument("-j", "--json", help="Print found data in json format", default=False, required=False,
                    action="store_true")
parser.add_argument("-o", "--output", help="Print found data to file")
parser.add_argument("-d", "--dispersion", type=int, default=3,
                    help="Number of lines around vulnerable line. Default is 3")


arguments = parser.parse_args()
