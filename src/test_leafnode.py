import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaftagless(self):
        node = LeafNode(None, "paragraph", None)
        self.assertEqual(node.to_html(), "paragraph")

    def test_leafsimple(self):
        node = LeafNode("p", "paragraph", None)
        self.assertEqual(node.to_html(), "<p>paragraph</p>")

    def test_leafnotsimple(self):
        node = LeafNode("a", "paragraph", {"href":"someurl"})
        self.assertEqual(node.to_html(), '<a href="someurl">paragraph</a>')

    def test_leafvalueless(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
