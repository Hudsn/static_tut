import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        tag = "p"
        value = "this is some paragraph text"
        children = []
        props = {"great":"googley moogley"}
        node = HTMLNode(tag, value, children, props)
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

        div = HTMLNode("div", children=[node])
        self.assertEqual(len(div.children), 1)
        child = div.children[0]
        self.assertEqual(child, node)


    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        want = 'href="https://www.google.com" target="_blank"'
        got = node.props_to_html()
        self.assertEqual(want, got)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_div_with_props(self):
        props = {"data":"exists"}
        node = LeafNode("div", "div text", props=props)
        self.assertEqual(node.to_html(), '<div data="exists">div text</div>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        props = {"data":"still exists"}
        main_node = ParentNode("div", [], props=props)
        self.assertEqual(
            main_node.to_html(),
            '<div data="still exists"></div>'
        )

