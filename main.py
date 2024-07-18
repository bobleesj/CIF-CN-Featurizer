import os
import time
from core.features import (
    coordination_handler,
    binary_wyc,
    binary_env_handler,
    binary_interatomic,
    ternary_interatomic,
    ternary_env_handler,
    ternary_wyc,
)
from core.utils import folder, prompt, check_file
import pandas as pd

# Process each file
from cifkit import Cif
from cifkit.utils.folder import get_file_paths

# Process folders sequentially


# Choose the folder
def main():
    script_path = os.path.dirname(os.path.abspath(__file__))
    dir_names_with_cif = folder.get_cif_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(dir_names_with_cif, ".cif")

    num_selected_dirs = len(selected_dirs)
    for idx, (_, dir_path) in enumerate(selected_dirs.items(), start=1):
        prompt.prompt_folder_progress(idx, dir_path, num_selected_dirs)
        process_folder(dir_path)


def process_folder(dir_path):
    file_paths = get_file_paths(dir_path)

    binary_data = []
    ternary_data = []
    uni_data = []

    for i, file_path in enumerate(file_paths, start=1):
        file_start_time = time.perf_counter()
        cif: Cif = Cif(file_path)
        prompt.prompt_progress_current(i, file_path, cif.supercell_atom_count, len(file_paths))
        cif.compute_connections()
        elements = list(cif.unique_elements)

        # Check the elements in the configuration
        try:
            check_file.check_availability_for_binary_ternary(file_path, elements)
        except ValueError as e:
            print(f"Error found for {file_path}. Reason: {e}")
            continue

        # Check if binary or ternary
        if len(elements) == 2:
            binary_int_data, uni_int_data = binary_interatomic.compute_binary_interatomic_features(cif)
            binary_wyc_data, uni_wyc_data = binary_wyc.compute_binary_wyc_features(cif)
            binary_env_data = binary_env_handler.compute_binary_env_features(cif)
            binary_CN_data = coordination_handler.get_CN_binary_features(cif)

            # Combine all features into a single dictionary
            binary_combined_data = {}
            binary_combined_data.update(binary_int_data)
            binary_combined_data.update(binary_wyc_data)
            binary_combined_data.update(binary_env_data)
            binary_combined_data.update(binary_CN_data)

            # Get universal features
            uni_combined_data = {}
            uni_combined_data.update(uni_int_data)
            uni_combined_data.update(uni_wyc_data)
            uni_combined_data.update(binary_CN_data)

            # Add the combined_data dictionary to your list
            binary_data.append(binary_combined_data)
            uni_data.append(uni_combined_data)

            # log.print_dict_pretty(binary_combined_data, "binary_data")
            # log.print_dict_pretty(uni_combined_data, "uni_data")

        if len(elements) == 3:
            ternary_int_data, uni_int_data = ternary_interatomic.compute_ternary_interatomic_features(cif)
            ternary_wyc_data, uni_wyc_data = ternary_wyc.compute_ternary_wyk_features(cif)
            ternary_env_data = ternary_env_handler.compute_ternary_env_features(cif)
            ternary_CN_data = coordination_handler.get_CN_ternary_features(cif)

            ternary_combined_data = {}
            ternary_combined_data.update(ternary_int_data)
            ternary_combined_data.update(ternary_wyc_data)
            ternary_combined_data.update(ternary_env_data)
            ternary_combined_data.update(ternary_CN_data)

            # Get universal features
            uni_combined_data = {}
            uni_combined_data.update(uni_int_data)
            uni_combined_data.update(uni_wyc_data)
            uni_combined_data.update(ternary_CN_data)

            # Add the combined_data dictionary to your list
            ternary_data.append(ternary_combined_data)
            uni_data.append(uni_combined_data)

            # log.print_dict_pretty(ternary_combined_data, "ternary_data")
            # log.print_dict_pretty(uni_combined_data, "uni_data")

        elapsed_time = time.perf_counter() - file_start_time
        prompt.prompt_progress_finished(cif.file_name, cif.supercell_atom_count, elapsed_time)

    # Make csv folder
    csv_folder_path = os.path.join(dir_path, "csv")
    binary_csv_path = os.path.join(csv_folder_path, "binary_features.csv")
    ternary_csv_path = os.path.join(csv_folder_path, "ternary_features.csv")
    universal_csv_path = os.path.join(csv_folder_path, "universal_features.csv")
    os.makedirs(csv_folder_path, exist_ok=True)

    # Save files
    if binary_data:
        pd.DataFrame(binary_data).round(3).to_csv(binary_csv_path, index=False)
        prompt.prompt_file_saved(binary_csv_path)
    if ternary_data:
        pd.DataFrame(ternary_data).round(3).to_csv(ternary_csv_path, index=False)
        prompt.prompt_file_saved(ternary_csv_path)

    if binary_data or ternary_data:
        pd.DataFrame(uni_data).round(3).to_csv(universal_csv_path, index=False)
        prompt.prompt_file_saved(universal_csv_path)


if __name__ == "__main__":
    main()
