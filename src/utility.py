import re
import shutil
import os
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
        texts = node.text.split(delimiter, 2)
        if len(texts) <= 1:
            ret_nodes.append(node)
        else:
            while True:
                print(texts)
                if len(texts) > 0 and texts[0] != "":
                    ret_nodes.append(TextNode(texts[0], TextType.NORMAL))

                if len(texts) > 1 and texts[1] != "":
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
                    texts = texts[2].split(delimiter, 2)
                else:
                    break
                    # ret_nodes.append(TextNode(texts[2], TextType.NORMAL))

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

def block_to_html_node(block):
    ret = None
    match block_to_block_type(block):        
        case BlockType.PARAGRAPH:
            children = []
            print(text_to_textnodes(block))
            for text in text_to_textnodes(block):
                children.append(text_node_to_html_node(text))
            ret = ParentNode("p", children)

        case BlockType.QUOTE:
            children = []
            for text in text_to_textnodes(block[2:]):
                children.append(text_node_to_html_node(text))
            ret = ParentNode("blockquote", children)
        case BlockType.HEADING:
            headingnumber = 0
            for i in range(0, len(block[:6])):
                if block[i] != '#':
                    break
                headingnumber += 1
            children = []
            for text in text_to_textnodes(block[headingnumber + 1:]):
                children.append(text_node_to_html_node(text))
            ret = ParentNode(f"h{headingnumber}", children)
        case BlockType.CODE:
            ret = ParentNode("pre", [text_node_to_html_node(TextNode(block[3:-3], TextType.CODE))])
        case BlockType.UNORDERED_LIST:
            children = []
            for listitems in block.split("\n"):
                lis = []
                for text in text_to_textnodes(listitems[2:]):
                    lis.append(text_node_to_html_node(text))
                children.append(ParentNode("li", lis))
            ret = ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = []
            for listitems in block.split("\n"):
                lis = []
                for text in text_to_textnodes(listitems[3:]):
                    lis.append(text_node_to_html_node(text))
                children.append(ParentNode("li", lis))
            ret = ParentNode("ol", children)

    return ret

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        node = block_to_html_node(block)
        if node:
            children.append(node)
            
    return ParentNode("div", children)

def copy_to_public():
    shutil.rmtree("./public")
    shutil.copytree("./static/", "./public", dirs_exist_ok=True)

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            return line[2:]
        
    raise Exception("Missing header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_contents = ""
    with open(from_path) as fp:
        from_contents = fp.read()

    template_contents = ""
    with open(template_path) as tp:
        template_contents = tp.read()

    page = markdown_to_html_node(from_contents)
    title = extract_title(from_contents)

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", page.to_html())

    with open(dest_path, "w") as dp:
        dp.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs("./public/blog/glorfindel")
    generate_page("./content/blog/glorfindel/index.md", "template.html", "./public/blog/glorfindel/index.html")
    os.makedirs("./public/blog/majesty")
    generate_page("./content/blog/majesty/index.md", "template.html", "./public/blog/majesty/index.html")
    os.makedirs("./public/blog/tom")
    generate_page("./content/blog/tom/index.md", "template.html", "./public/blog/tom/index.html")
    os.makedirs("./public/contact")
    generate_page("./content/contact/index.md", "template.html", "./public/contact/index.html")
    generate_page("./content/index.md", "template.html", "./public/index.html")

