import re
from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})
        
        case _:
            raise Exception("unknown text node")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_nodes = []
    for node in old_nodes:
        texts = node.text.split(delimiter)
        if not texts or len(texts) <= 1:
            ret_nodes.append(node)
        else:
            ret_nodes.append(TextNode(texts[0], TextType.NORMAL))
            match delimiter:
                case "**":
                    ret_nodes.append(TextNode(texts[1], TextType.BOLD))
                case "_":
                    ret_nodes.append(TextNode(texts[1], TextType.ITALIC))
                case "`":
                    ret_nodes.append(TextNode(texts[1], TextType.CODE))
                case _:
                    ret_nodes.append(TextNode(texts[1], TextType.NORMAL))

            ret_nodes.append(TextNode(texts[2], TextType.NORMAL))

    return ret_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
