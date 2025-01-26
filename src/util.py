from pathlib import Path
import shutil


def copy_content(src, dst):
    dst = Path(dst)
    src = Path(src)

    if not src.exists():
        raise Exception(f"{src} does not exist")

    if dst.exists():
        shutil.rmtree(dst)

    # base case: src is a file, copy it directly
    if src.is_file():
        if not dst.parent.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
    else:
        # src is a directory, iterate through its contents
        if not dst.exists():
            dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            copy_content(item, dst / item.name)
