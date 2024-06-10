import unittest
from htmlnode import HTMLnode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLnode(
            "tag",
            "value",
            None,
            {"href": "https://www.google.com", "target": "_blank "},
        )
        self.assertEqual(
            node1.props_to_html(), ' href="https://www.google.com" target="_blank "'
        )

    def test_props_to_html_neq(self):
        node1 = HTMLnode(
            "tag",
            "value",
            None,
            {"href": "https://www.google.com", "target": "_blank "},
        )
        self.assertNotEqual(
            node1.props_to_html(), 'href="https://www.google.com" target="blank"'
        )

    def test_leaf_node_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )

    def test_parent_node(self):
        node = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            "p",
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
