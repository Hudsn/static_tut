import os
import shutil

from page_gen import generate_pages_recursive


def main():
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")


def copy_static_to_public():
    # check that public dir exists
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    if not os.path.exists("static"):
        return
    recursive_copy("static", "public")

   

def recursive_copy(source_dir, dest_dir):
     for existing_item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, existing_item)
        if os.path.isfile(item_path):
            new_path = os.path.join(dest_dir, existing_item)
            shutil.copy(item_path, new_path)
        if os.path.isdir(item_path):
            new_dir = os.path.join(dest_dir, existing_item)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            recursive_copy(item_path, new_dir)
        


main()
