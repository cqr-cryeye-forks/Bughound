import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="local path of the source code")
parser.add_argument("--git", help="git repository URL")
# parser.add_argument("--init", help="initialize Elastic and Kibanna requirements", action="store_true")
parser.add_argument("--language", help="the used programming language", required=True)
parser.add_argument("--extension", help="extension to search for", required=True)
parser.add_argument("--name", help="project name to use", required=True)
parser.add_argument("--verbose", help="show debugging messages", default=False, required=False, const=True,
                    nargs='?')

arguments = parser.parse_args()
