import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_noprop(self):
        node = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_oneprop(self):
        node = HTMLNode(None, None, None, {"one":"something"})
        self.assertEqual(node.props_to_html(), ' one="something"')

    def test_twoprop(self):
        node = HTMLNode(None, None, None, {"one":"something","two":"somethingelse"})
        self.assertEqual(node.props_to_html(), ' one="something" two="somethingelse"')

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()