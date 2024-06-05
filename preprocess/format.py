import os
import pandas as pd
import glob
from util import folder
from preprocess import cif_parser, cif_editor, supercell


def move_files_based_on_format_error(dir_path):
    print("\nCIF Preprocessing has begun...\n")

    dir_name = os.path.basename(dir_path)

    # Define the directory paths for different error types
    dir_path_bad_cif = os.path.join(dir_path, f"{dir_name}_error_format")
    dir_path_bad_op = os.path.join(dir_path, f"{dir_name}_error_op")
    dir_path_bad_coords = os.path.join(dir_path, f"{dir_name}_error_coords")
    dir_path_bad_label = os.path.join(dir_path, f"{dir_name}_error_label")
    dir_path_bad_third_line = os.path.join(
        dir_path, f"{dir_name}_error_third_line"
    )
    dir_path_bad_other_error = os.path.join(
        dir_path, f"{dir_name}_error_others"
    )

    # Initialize counters for each error directory
    num_files_bad_op = 0
    num_files_bad_cif = 0
    num_files_bad_coords = 0
    num_files_bad_label = 0
    num_files_bad_third_line = 0
    num_files_bad_others = 0

    # Get the list of all CIF files in the directory
    files = glob.glob(os.path.join(dir_path, "*.cif"))
    total_files = len(files)
    file_errors = []

    for idx, file_path in enumerate(
        files, start=1
    ):  # Use enumerate to get the index
        filename = os.path.basename(file_path)

        try:
            cif_editor.preprocess_cif_file_by_removing_author_loop(file_path)
            cif_editor.preprocess_cif_file_on_label_element(file_path)
            
            print(f"Preprocessing {filename} ({idx} out of {total_files})")
            # Apply operations that would be done in practice
            cif_block = cif_parser.get_cif_block(file_path)
            cif_loop_values = cif_parser.get_loop_values(
                cif_block, cif_parser.get_loop_tags()
            )
            all_coords_list = supercell.get_coords_list(
                cif_block, cif_loop_values
            )
            supercell.get_points_and_labels(all_coords_list, cif_loop_values)

        except Exception as e:
            error_message = str(e)
            print(error_message)

            # Append file and error details to the list
            file_errors.append(
                {"filename": file_path, "error_message": error_message}
            )

            if (
                "An error occurred while processing symmetry operation"
                in error_message
            ):
                os.makedirs(dir_path_bad_op, exist_ok=True)
                debug_filename = os.path.join(dir_path_bad_op, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_op += 1
            elif "Wrong number of values in the loop" in error_message:
                os.makedirs(dir_path_bad_cif, exist_ok=True)
                debug_filename = os.path.join(dir_path_bad_cif, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_cif += 1
            elif "Missing atomic coordinates" in error_message:
                os.makedirs(dir_path_bad_coords, exist_ok=True)
                debug_filename = os.path.join(dir_path_bad_coords, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_coords += 1
            elif (
                "Different elements found in atom site and label"
                in error_message
            ):
                os.makedirs(dir_path_bad_label, exist_ok=True)
                debug_filename = os.path.join(dir_path_bad_label, filename)
                os.rename(file_path, debug_filename)
                num_files_bad_label += 1
            elif (
                "The CIF file is wrongly formatted in the third line"
                in error_message
            ):
                os.makedirs(dir_path_bad_third_line, exist_ok=True)
                debug_filename = os.path.join(
                    dir_path_bad_third_line, filename
                )
                os.rename(file_path, debug_filename)
                num_files_bad_third_line += 1
            else:
                os.makedirs(dir_path_bad_other_error, exist_ok=True)
                debug_filename = os.path.join(
                    dir_path_bad_other_error, filename
                )
                os.rename(file_path, debug_filename)
                num_files_bad_others += 1
            print()

    # Display the number of files moved to each folder
    print("\nSUMMARY")
    print(f"# of files moved to 'error_op' folder: {num_files_bad_op}")
    print(f"# of files moved to 'error_format' folder: {num_files_bad_cif}")
    print(f"# of files moved to 'error_coords' folder: {num_files_bad_coords}")
    print(f"# of files moved to 'error_label' folder: {num_files_bad_label}")
    print(
        f"# of files moved to 'error_third_line' folder: {num_files_bad_third_line}"
    )
    print(f"# of files moved to 'error_others' folder: {num_files_bad_others}")

    df_errors = pd.DataFrame(file_errors)

    # Check if the DataFrame has more than one column
    if df_errors.shape[1] > 1:
        # Use the save_to_csv_directory function to save the DataFrame
        folder.save_df_to_csv(dir_path, df_errors, "error_log")
    else:
        print("All files are propertly formatted.")
