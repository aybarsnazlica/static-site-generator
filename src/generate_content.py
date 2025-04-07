import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content: Path, template_path, dest_dir_path, base_path):
    for path in dir_path_content.iterdir():
        dest_path = dest_dir_path / path.name

        if path.is_file():
            dest_path = dest_path.with_suffix(".html")
            generate_page(path, template_path, dest_path, base_path)
        else:
            generate_pages_recursive(path, template_path, dest_path, base_path)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(template)


def extract_title(md):
    lines = md.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise ValueError("no title found")
