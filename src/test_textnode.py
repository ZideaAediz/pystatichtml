import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        node_dtext = TextNode("no match", TextType.NORMAL)
        self.assertNotEqual(node, node_dtext)

    def test_neq_type(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        node_dtype = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node_dtype)

    def test_neq_url(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        node_durl = TextNode("this is a text node", TextType.NORMAL, "someurl")
        self.assertNotEqual(node, node_durl)


if __name__ == "__main__":
    unittest.main()