import re
import os

from helpers import markdown_to_html_node

def extract_title(markdown):
    md_split = markdown.split("\n")
    lines = list(filter(lambda md_line: md_line.startswith("# "), md_split))
    if len(lines) == 0:
        raise Exception("unable to extract title")
    return lines[0].replace("# ", "").strip()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for existing_item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, existing_item)
        if os.path.isfile(item_path) and item_path.endswith(".md"):
            new_file = os.path.join(dest_dir_path, existing_item)[:-3] + ".html"
            generate_page(item_path, template_path, new_file, base_path)
        if os.path.isdir(item_path):
            new_dir = os.path.join(dest_dir_path, existing_item)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            generate_pages_recursive(item_path, template_path, new_dir, base_path)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    from_content = None
    with open(from_path, 'r') as from_file:
        from_content = from_file.read()

    template_content = None
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    md_as_html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    out_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", md_as_html).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    with open(dest_path, 'w') as dest_file:
        print(out_content, file=dest_file)


    