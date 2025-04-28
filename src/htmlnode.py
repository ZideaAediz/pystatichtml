
class HTMLNode:
    def __init__(self, tag = None, value = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        retstr = ""
        for key, value in self.props:
            retstr += f' {key}="{value}"'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children})"
