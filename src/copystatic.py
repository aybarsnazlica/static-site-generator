import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not source_dir_path.is_dir():
        return
    if not dest_dir_path.exists():
        dest_dir_path.mkdir(parents=True, exist_ok=True)

    for filename in source_dir_path.iterdir():
        from_path = source_dir_path / filename.name
        dest_path = dest_dir_path / filename.name

        print(f" * {from_path} -> {dest_path}")

        if from_path.is_file():
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
