from textnode import *

def main():
    tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(tn)

main()