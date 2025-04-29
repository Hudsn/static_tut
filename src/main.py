import os
import sys
import shutil

from page_gen import generate_pages_recursive


def main():
    base_path = "/"
    if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
        base_path = sys.argv[1]
    target_dir = "docs"
    copy_static_to_target(target_dir)
    generate_pages_recursive("content", "template.html", target_dir, base_path)


def copy_static_to_target(target_dir):
    # check that public dir exists
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.mkdir(target_dir)
    if not os.path.exists("static"):
        return
    recursive_copy("static", target_dir)

   

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
