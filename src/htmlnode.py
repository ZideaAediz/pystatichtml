from textnode import *

class HTMLNode:
    def __init__(self, tag = None, value = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        if not children:
            self.children = []
        else:
            self.children = children

        if not props:
            self.props = {}
        else:
            self.props = props
    
    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        retstr = ""
        for (key, value) in self.props.items():
            retstr += f' {key}="{value}"'
        return retstr

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        
        if not self.children:
            raise ValueError("missing children")
        
        retstr = f"<{self.tag}>"
        for child in self.children:
            retstr += child.to_html()
        retstr += f"</{self.tag}>"
        return retstr

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
