import shutil
import sys
from pathlib import Path
from copystatic import copy_files_recursive
from generate_content import generate_pages_recursive

default_base_path = Path("/")
dir_path_static = Path("static")
dir_path_public = Path("public")
dir_path_content = Path("content")
template_path = Path("template.html")


def main():
    base_path = default_base_path

    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])

    print("Deleting public directory...")
    if dir_path_public.exists():
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursive(str(dir_path_content), str(template_path), str(dir_path_public), str(base_path))


if __name__ == "__main__":
    main()
