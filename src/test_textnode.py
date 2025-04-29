import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from helpers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes, markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_type_neq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("this is a link node", TextType.LINK)
        node2 = TextNode("this is a link node", TextType.LINK, "example.com")
        self.assertNotEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("this is a link node", TextType.LINK)
        node2 = TextNode("this is also link node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def text_text_to_html_link(self):
        node = TextNode("This is a link node", TextType.LINK, "example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "example.com")

class TestSplitDelim(unittest.TestCase):
    def base_case(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )
    def test_italics(self):
        node = TextNode("This is text with a __italic__ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )
    def test_none(self):
        node = TextNode("This is text with a word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a word", TextType.TEXT)
            ]
        )

class TestRegex(unittest.TestCase):
    def test_images_pos(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        got = extract_markdown_images(text)
        want = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(want, got)

    def test_images_neg(self):
        text = "This is text with a !~rick roll~(https://i.imgur.com/aKaOqIh.gif) and ![obi wan][https://i.imgur.com/fJRm4Vk.jpeg]"
        got = extract_markdown_images(text)
        want = []
        self.assertEqual(want, got)

    def test_links_pos(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        got = extract_markdown_links(text)
        want = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(want, got)

    def test_links_neg(self):
        text = "This is text with a link (to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        got = extract_markdown_links(text)
        want = []
        self.assertEqual(want, got)

class TestSplitNodesLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        got = split_nodes_link([node])
        want = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(want, got)

    def test_no_split(self):
        node = TextNode(
            "This is text with NO LINKS",
            TextType.TEXT,
        )
        got = split_nodes_link([node])
        self.assertEqual(got, [node])
    
    def test_mixed(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and ![an image](https://www.myimage.link)",
                TextType.TEXT,
        )
        got = split_nodes_link([node])
        want = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ![an image](https://www.myimage.link)", TextType.TEXT),
        ]
        self.assertEqual(want, got)

class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        def test_no_split(self):
            node = TextNode(
                "This is text with NO IMAGES",
                TextType.TEXT,
            )
            got = split_nodes_image([node])
            self.assertEqual(got, [node])

    def test_mixed(self):
        node = TextNode(
            "This is text with ![an image](https://www.myimage.link) and [a link!](example.com)",
            TextType.TEXT,
        )
        got = split_nodes_image([node])
        want = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://www.myimage.link"),
            TextNode(" and [a link!](example.com)", TextType.TEXT),
        ]
        self.assertEqual(want, got)

class TestTextToNodes(unittest.TestCase):
    def test_node_gen(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        want = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        got = text_to_textnodes(text)
        self.assertEqual(want, got)

    def test_node_gen_text_only(self):
        text = "This is just some good old text"
        want = [
            TextNode("This is just some good old text", TextType.TEXT),
        ]
        got = text_to_textnodes(text)
        self.assertEqual(want, got)

    def test_node_gen_empty(self):
        text = ""
        want = []
        got = text_to_textnodes(text)
        
        self.assertEqual(want, got)

class TestBlockParser(unittest.TestCase):
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
    def test_markdown_to_block_single_block_with_space(self):
        md = """





      This is **bolded** paragraph       







"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph"
            ],
        )


if __name__ == "__main__":
    unittest.main()