import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_code,
    text_type_bold,
    text_type_italic,
)


def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


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


def _split_node_image_link_helper(
    old_node: TextNode, delimiters: list[tuple], text_type: str
) -> list[TextNode]:
    split_nodes = []
    string_mappings = {text_type_image: "![x1](x2)", text_type_link: "[x1](x2)"}
    current_text = [old_node.text]

    for delimiter in delimiters:
        delimiter_str = string_mappings[text_type].replace("x1", delimiter[0])
        delimiter_str = delimiter_str.replace("x2", delimiter[1])
        split_text = current_text[0].split(delimiter_str, 1)

        if split_text[0] != "":
            split_nodes.append(TextNode(split_text[0], text_type_text))

        split_nodes.append(TextNode(delimiter[0], text_type, delimiter[1]))
        current_text = split_text[1:]

    if len(current_text) != 0 and current_text[0] != "":
        split_nodes.append(TextNode(current_text[0], text_type_text))

    return split_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for old_node in old_nodes:
        delimiters = extract_markdown_images(old_node.text)
        if len(delimiters) != 0:
            split_nodes += _split_node_image_link_helper(
                old_node, delimiters, text_type_image
            )
        else:
            split_nodes.append(old_node)

    return split_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for old_node in old_nodes:
        delimiters = extract_markdown_links(old_node.text)
        if len(delimiters) != 0:
            split_nodes += _split_node_image_link_helper(
                old_node, delimiters, text_type_link
            )
        else:
            split_nodes.append(old_node)

    return split_nodes


def text_to_textnodes(text):
    text_nodes = [TextNode(text, text_type_text)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, "*", text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, "`", text_type_code)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes


if __name__ == "__main__":
    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    print(extract_markdown_links(text))
