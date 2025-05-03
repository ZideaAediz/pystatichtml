import sys
from utility import *
from textnode import *

def main():
    basepath = "/"
    if len(sys.argv) > 1 and basepath != "":
        basepath = sys.argv[1]

    copy_to_public()
    generate_pages_recursive("./content", ".", "./docs")

main()