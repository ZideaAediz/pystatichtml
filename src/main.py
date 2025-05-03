from utility import *
from textnode import *

def main():
    copy_to_public()
    generate_pages_recursive("./content", ".", "./public")

main()