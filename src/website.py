import os
import shutil
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_heading,
    markdown_to_html_node,
)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == block_type_heading and block.startswith("# "):
            return block[2:]

    raise ValueError("There needs to be at least one h1 block in the markdown")


def generate_page_recursive(from_path: str, template_path: str, dest_path: str):
    files = os.listdir(from_path)
    for file in files:
        new_from_path = os.path.join(from_path, file)
        file = file.replace(".md", ".html")
        new_dest_path = os.path.join(dest_path, file)
        if os.path.isfile(new_from_path):
            generate_page(new_from_path, template_path, new_dest_path)
        else:
            generate_page_recursive(new_from_path, template_path, new_dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = ""
    template_file = ""

    with open(from_path) as file:
        from_file = file.read()

    with open(template_path) as file:
        template_file = file.read()

    html = markdown_to_html_node(from_file).to_html()
    html_title = extract_title(from_file)
    filled_template = template_file.replace("{{ Title }}", html_title)
    filled_template = filled_template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "w+") as file:
        file.write(filled_template)

    return


def copy_static():
    STATIC_PATH = "static/"
    PUBLIC_PATH = "public/"
    copy_files(STATIC_PATH, PUBLIC_PATH)


def copy_files(dir1: str, dir2: str):
    if not os.path.exists(dir1):
        raise ValueError(f"{dir1} doesn't exist, can't copy contents")

    if os.path.exists(dir2):
        shutil.rmtree(dir2)
    os.mkdir(dir2)

    for file in os.listdir(dir1):
        dir1_path = os.path.join(dir1, file)
        dir2_path = os.path.join(dir2, file)

        if os.path.isfile(dir1_path):
            print(f"copying file {file} from {dir1_path} to {dir2_path}")
            shutil.copy(dir1_path, dir2_path)
        else:
            print(f"copying files from directory {dir1_path} to {dir2_path}")
            copy_files(dir1_path, dir2_path)

    print("done copying")
