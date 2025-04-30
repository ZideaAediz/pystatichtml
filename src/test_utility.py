import unittest
from utility import *

class TestUtility(unittest.TestCase):
    def test_split(self):
        ret = split_nodes_delimiter([TextNode("This _is_ fake", TextType.NORMAL)], "_")
        self.assertEqual(len(ret), 3)

    def test_split_multiple(self):
        input = [TextNode("This _is_ fake", TextType.NORMAL)
                 , TextNode("This is _fake_", TextType.NORMAL)
                 , TextNode("_This is fake_", TextType.NORMAL)
                 , TextNode("This is fake", TextType.NORMAL)
                 ]
        ret = split_nodes_delimiter(input, "_")
        self.assertEqual(len(ret), 7)

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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_all(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes            
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def ordered_is(self, block):
        ret = re.match(r"^[1-9]+\. ", block)
        if ret:
            print(ret)
        else:
            print("NOOO")

    def test_block(self):
        self.assertEqual(block_to_block_type("# One"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Two"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Three"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Four"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Five"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Six"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#None"), BlockType.PARAGRAPH)

        self.assertEqual(block_to_block_type("``` This is good ```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```Also Good ```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("`Bad```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```Also bd`"), BlockType.PARAGRAPH)
        
        self.assertEqual(block_to_block_type(">Good"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Also good"), BlockType.QUOTE)

        self.assertEqual(block_to_block_type("- Good"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("-Bad"), BlockType.PARAGRAPH)

        self.assertEqual(block_to_block_type("1. Good"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1, Bad"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.Bad"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()