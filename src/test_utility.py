import unittest
from utility import *

class TestUtility(unittest.TestCase):
    def test_split(self):
        ret = split_nodes_delimiter([TextNode("This _is_ fake", TextType.NORMAL)], "_", TextType.ITALIC)
        self.assertEqual(len(ret), 3)

    def test_split_multiple(self):
        input = [TextNode("This _is_ fake", TextType.NORMAL)
                 , TextNode("This is _fake_", TextType.NORMAL)
                 , TextNode("_This is fake_", TextType.NORMAL)
                 ]
        ret = split_nodes_delimiter(input, "_", TextType.ITALIC)
        self.assertEqual(len(ret), 9)

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        ret = extract_markdown_images(text)
        self.assertEqual(len(ret), 2)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        ret = extract_markdown_links(text)
        self.assertEqual(len(ret), 2)

if __name__ == "__main__":
    unittest.main()