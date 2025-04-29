import unittest

from blocks import BlockType, block_to_type
from helpers import markdown_to_html_node

class TestBlockToType(unittest.TestCase):
    def test_heading(self):
        block = "### MY HEADING"
        want = BlockType.HEADING
        got = block_to_type(block)
        self.assertEqual(want, got)

    def test_code(self):
        block = "``` print(hello world) ```"
        want = BlockType.CODE
        got = block_to_type(block)
        self.assertEqual(want, got)

    def test_quote(self):
        block = "> ishygddt"
        want = BlockType.QUOTE
        got = block_to_type(block)
        self.assertEqual(want, got)

    def test_ul(self):
        block = "- for my valentine"
        want = BlockType.UNORDERED_LIST
        got = block_to_type(block)
        self.assertEqual(want, got)

    def test_ol(self):
        block = "9001. scouter level"
        want = BlockType.ORDERED_LIST
        got = block_to_type(block)
        self.assertEqual(want, got)

    def test_p(self):
        block = "boring"
        want = BlockType.PARAGRAPH
        got = block_to_type(block)
        self.assertEqual(want, got) 



class TestMDToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is an unordered list item
- This is another with **bold** text

3. This is an ordered item starting at not one
4. This is another
5. This is a third (fifth?)
"""

        node = markdown_to_html_node(md)
        got = node.to_html()
        want = '<div><ul><li>This is an unordered list item</li><li>This is another with <b>bold</b> text</li></ul><ol start="3"><li>This is an ordered item starting at not one</li><li>This is another</li><li>This is a third (fifth?)</li></ol></div>'
        self.assertEqual(want, got)

    def test_headers(self):
        md = """
# this is an h1

### this is an h3
"""

        node = markdown_to_html_node(md)
        got = node.to_html()
        want = '<div><h1>this is an h1</h1><h3>this is an h3</h3></div>'
        self.assertEqual(want, got)

    def test_quotes(self):
        md = """
        > ISHYGDDT
"""

        node = markdown_to_html_node(md)
        got = node.to_html()
        want = '<div><blockquote>ISHYGDDT</blockquote></div>'
        self.assertEqual(want, got)

    def test_list_nested(self):
        md = """
1. abc
2. something about (`Valar` and `Maiar`)
"""
        node = markdown_to_html_node(md)
        got = node.to_html()
        want = '<div><ol><li>abc</li><li>something about (<code>Valar</code> and <code>Maiar</code>)</li></ol></div>'
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()