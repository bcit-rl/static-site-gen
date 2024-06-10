from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    text_type_to_result = {
        text_type_text: LeafNode(tag=None, value=text_node.text),
        text_type_bold: LeafNode(tag="b", value=text_node.text),
        text_type_italic: LeafNode(tag="i", value=text_node.text),
        text_type_code: LeafNode(tag="code", value=text_node.text),
        text_type_link: LeafNode(
            tag="a", value=text_node.text, props={"href": text_node.url}
        ),
        text_type_image: LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        ),
    }

    if text_node.text_type not in text_type_to_result:
        raise ValueError("Invalide Text Node Type")

    return text_type_to_result[text_node.text_type]


def _split_node_with_delimiter(
    node: TextNode, delimiter: str, text_type
) -> list[TextNode]:
    sections = node.text.split(delimiter)
    formatted_nodes = []

    if len(sections) % 2 == 0:
        raise ValueError(
            f"Invalid Markdown, {text_type} must have an opening and closing {delimiter}"
        )

    for index, section in enumerate(sections):
        if section == "":
            continue
        if index % 2 == 0:
            formatted_nodes.append(TextNode(section, text_type_text))
        else:
            formatted_nodes.append(TextNode(section, text_type))

    return formatted_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            new_nodes += _split_node_with_delimiter(node, delimiter, text_type)

    return new_nodes
