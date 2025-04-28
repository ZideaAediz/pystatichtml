import unittest

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()