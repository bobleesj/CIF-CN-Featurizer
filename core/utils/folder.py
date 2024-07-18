import glob
import os


def get_file_paths(dir_path: str, ext=".cif") -> list[str]:
    """
    Return a list of file paths with a given extension from a directory.
    """
    return glob.glob(os.path.join(dir_path, f"*{ext}"))


def make_output_folder(dir_path: str, new_folder_name: str) -> str:
    """
    Create an output folder
    """
    full_path = os.path.join(dir_path, new_folder_name)

    # Check if the directory already exists
    if not os.path.exists(full_path):
        # Create the directory
        os.makedirs(full_path)
        print(f"Folder '{new_folder_name}' created at '{dir_path}'.")
    else:
        print(f"Folder '{new_folder_name}' already exists at '{dir_path}'.")
    return full_path


def get_cif_dir_names(script_path):
    """
    Return a list of directory names containing .cif files, excluding those
    starting with 'tests'. Directory names are relative to the script_path.
    """
    dir_names = [
        os.path.basename(d)
        for d in os.listdir(script_path)
        if os.path.isdir(os.path.join(script_path, d))
        and not d.startswith("tests")  # Exclude directories starting with 'tests'
        and contains_cif_files(os.path.join(script_path, d))
    ]

    if not dir_names:
        print("No directories found in the current path containing .cif files.")
        return []  # Return an empty list instead of None

    return dir_names


def contains_cif_files(directory):
    """
    Check if the specified directory contains any .cif files.
    """
    for file in os.listdir(directory):
        if file.endswith(".cif") and os.path.isfile(os.path.join(directory, file)):
            return True
    return False
