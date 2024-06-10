import unittest
from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bolds")
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text nodes", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, None)")

    def test_node_to_html_text(self):
        text_node = TextNode("This is a text TextNode", "text")
        html_node = "This is a text TextNode"
        answer = text_node_to_html_node(text_node).to_html()

        self.assertEqual(answer, f"{html_node}")

    def test_node_to_html_bold(self):
        text_node = TextNode("This is a bold TextNode", "bold")
        html_node = "<b>This is a bold TextNode</b>"
        answer = text_node_to_html_node(text_node).to_html()

        self.assertEqual(answer, f"{html_node}")

    def test_node_to_html_italic(self):
        text_node = TextNode("This is a italic TextNode", "italic")
        html_node = "<i>This is a italic TextNode</i>"
        answer = text_node_to_html_node(text_node).to_html()

        self.assertEqual(answer, f"{html_node}")

    def test_node_to_html_code(self):
        text_node = TextNode("This is a code TextNode", "code")
        html_node = "<code>This is a code TextNode</code>"
        answer = text_node_to_html_node(text_node).to_html()

        self.assertEqual(answer, f"{html_node}")

    def test_node_to_html_link(self):
        text_node = TextNode("This is a link TextNode", "link", "www.google.ca")
        html_node = '<a href="www.google.ca">This is a link TextNode</a>'
        answer = text_node_to_html_node(text_node).to_html()

        self.assertEqual(answer, f"{html_node}")

    def test_node_to_html_image(self):
        text_node = TextNode("duck", "image", "gobta.jpg")
        html_node = '<img src="gobta.jpg" alt="duck"></img>'
        answer = text_node_to_html_node(text_node).to_html()

        self.assertEqual(answer, f"{html_node}")

    def test_node_invalid_tag(self):
        self.assertRaises(
            ValueError, text_node_to_html_node, TextNode("duck", "boofta", "abk")
        )

    def test_node_invalid_tag_close_match(self):
        self.assertRaises(
            ValueError, text_node_to_html_node, TextNode("duck", "Image", "abk")
        )

    if __name__ == "__main__":
        unittest.main()
