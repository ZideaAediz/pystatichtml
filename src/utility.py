import re
from textnode import *
from htmlnode import *
from blocktype import *

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

def split_nodes_delimiter(old_nodes, delimiter):
    ret_nodes = []
    for node in old_nodes:        
        texts = node.text.split(delimiter)
        if len(texts) <= 1:
            ret_nodes.append(node)
        else:
            if texts[0] != "":
                ret_nodes.append(TextNode(texts[0], TextType.NORMAL))

            if texts[1] != "":
                match delimiter:
                    case "**":
                        ret_nodes.append(TextNode(texts[1], TextType.BOLD))
                    case "_":
                        ret_nodes.append(TextNode(texts[1], TextType.ITALIC))
                    case "`":
                        ret_nodes.append(TextNode(texts[1], TextType.CODE))
                    case _:
                        ret_nodes.append(TextNode(texts[1], TextType.NORMAL))
            
            if len(texts) > 2 and texts[2] != "":
                ret_nodes.append(TextNode(texts[2], TextType.NORMAL))

    return ret_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    ret_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) < 1:
            ret_nodes.append(node)
        else:
            string = node.text
            for image in images:
                sections = string.split(f"![{image[0]}]({image[1]})", 1)
                if len(sections) <= 1:
                    ret_nodes.append(TextNode(string, TextType.NORMAL))
                else:
                    if sections[0] != "":
                        ret_nodes.append(TextNode(sections[0], TextType.NORMAL))

                    ret_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

                    if len(sections) > 1:
                        string = sections[1]
                    else:
                        string = ""

            if string != "":
                ret_nodes.append(TextNode(string, TextType.NORMAL))

    return ret_nodes

def split_nodes_link(old_nodes):
    ret_nodes = []
    for node in old_nodes:
        images = extract_markdown_links(node.text)
        if len(images) < 1:
            ret_nodes.append(node)
        else:
            string = node.text
            for image in images:
                sections = string.split(f"[{image[0]}]({image[1]})", 1)
                if len(sections) <= 1:
                    ret_nodes.append(TextNode(string, TextType.NORMAL))
                else:
                    if sections[0] != "":
                        ret_nodes.append(TextNode(sections[0], TextType.NORMAL))

                    ret_nodes.append(TextNode(image[0], TextType.LINK, image[1]))

                    if len(sections) > 1:
                        string = sections[1]
                    else:
                        string = ""

            if string != "":
                ret_nodes.append(TextNode(string, TextType.NORMAL))

    return ret_nodes

def text_to_textnodes(text):
    return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.NORMAL)], "**"), "`"), "_")))

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            blocks.append(block.strip())
    return blocks

def block_to_block_type(block: BlockType):
    if not block or len(block) <= 0:
        return BlockType.PARAGRAPH
    
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^`{3}.*`{3}$", block):
        return BlockType.CODE
    elif re.match(r"^>", block):
        return BlockType.QUOTE
    elif re.match(r"^- ", block):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^[0-9]+\. ", block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
