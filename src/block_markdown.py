from htmlnode import HTMLnode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered_list"
block_type_ordered = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    lines_of_markdown = markdown.split("\n")
    blocks = []
    current_block = ""

    for line in lines_of_markdown:
        if line == "" and current_block.strip().strip("\n") != "":
            blocks.append(current_block.strip().strip("\n"))
            current_block = ""
        else:
            current_block += line + "\n"

    return blocks


def block_to_block_type(block: str) -> str:
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    elif len(block) > len("``````") and block[:3] == "```" and block[-3:] == "```":
        return block_type_code

    lines_of_block = block.split("\n")
    is_quote = True
    is_unordered = True
    is_ordereded = True
    current_line = 1

    for line in lines_of_block:
        if len(line) == 0:
            return block_type_paragraph
        if line[0] != ">":
            is_quote = False
        if line[:2] != "* " and line[:2] != "- ":
            is_unordered = False
        if not line[0].isnumeric() or int(line[0]) != current_line or line[1:3] != ". ":
            is_ordereded = False
        current_line += 1

    if is_quote:
        return block_type_quote
    elif is_unordered:
        return block_type_unordered
    elif is_ordereded:
        return block_type_ordered
    else:
        return block_type_paragraph


def markdown_to_html_node(markdown: str):
    type_to_html_function = {
        block_type_paragraph: paragraph_to_html,
        block_type_heading: heading_to_html,
        block_type_code: code_to_html,
        block_type_quote: quote_to_html,
        block_type_unordered: unordered_to_html,
        block_type_ordered: ordered_to_html,
    }
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = type_to_html_function[block_type](block)
        html_nodes.append(html_node)

    return ParentNode(html_nodes, "div")


def child_nodes_from_text(text: str) -> list[HTMLnode]:
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))

    return child_nodes


def paragraph_to_html(block: str):
    child_nodes = child_nodes_from_text(" ".join(block.split("\n")))

    return ParentNode(child_nodes, "p")


def heading_to_html(block: str):
    count = 0
    for letter in block:
        if letter != "#":
            break
        else:
            count += 1

    child_nodes = child_nodes_from_text(block[count + 1 :])
    return ParentNode(child_nodes, f"h{count}")


def code_to_html(block: str):
    child_nodes = child_nodes_from_text(block[3:-3])
    return ParentNode(child_nodes, "pre")


def quote_to_html(block: str):
    inner_text = []
    lines = block.split("\n")
    for line in lines:
        inner_text.append(line[1:])
    proper_text = "".join(inner_text)

    if proper_text[0] and proper_text[0] == " ":
        proper_text = proper_text[1:]
    child_nodes = child_nodes_from_text(proper_text)

    return ParentNode(child_nodes, "blockquote")


def unordered_to_html(block: str):
    child_nodes = []
    lines = block.split("\n")
    for line in lines:
        inner_child_nodes = child_nodes_from_text(line[2:])
        child_nodes.append(ParentNode(inner_child_nodes, "li"))

    return ParentNode(child_nodes, "ul")


def ordered_to_html(block: str):
    child_nodes = []
    lines = block.split("\n")
    for line in lines:
        inner_child_nodes = child_nodes_from_text(line[3:])
        child_nodes.append(ParentNode(inner_child_nodes, "li"))

    return ParentNode(child_nodes, "ol")
