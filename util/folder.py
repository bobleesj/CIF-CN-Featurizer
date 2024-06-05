import glob
import os
from os.path import join


def choose_cif_directory(script_directory):
    """
    Allows the user to select a directory from the given path.
    """
    directories = [
        d
        for d in os.listdir(script_directory)
        if os.path.isdir(os.path.join(script_directory, d))
        and any(
            file.endswith(".cif")
            for file in os.listdir(os.path.join(script_directory, d))
        )
    ]

    if not directories:
        print(
            "No directories found in the current path containing .cif files!"
        )
        return None
    print("\nAvailable folders containing CIF files:")
    for idx, dir_name in enumerate(directories, start=1):
        num_of_cif_files = get_cif_file_count_from_directory(dir_name)
        print(f"{idx}. {dir_name}, {num_of_cif_files} files")
    while True:
        try:
            choice = int(
                input(
                    "\nEnter the number corresponding to the folder containing .cif files: "
                )
            )
            if 1 <= choice <= len(directories):
                return os.path.join(script_directory, directories[choice - 1])
            else:
                print(
                    f"Please enter a number between 1 and {len(directories)}."
                )
        except ValueError:
            print("Invalid input. Please enter a number.")



def save_df_to_csv(folder_path, df, base_filename):
    """
    Saves the dataframe as a CSV inside a 'csv' sub-directory
    of the provided folder.
    """
    # Create the sub-directory for CSVs if it doesn't exist
    csv_directory = os.path.join(folder_path, "csv")
    if not os.path.exists(csv_directory):
        os.mkdir(csv_directory)

    # Set the name for the CSV file based on the chosen folder
    csv_filename = f"{base_filename}.csv"
    # Round numeric columns to three decimal places
    df_rounded = df.round(3)

    # Save the DataFrame to the desired location (within the 'csv' sub-directory)
    df_rounded.to_csv(os.path.join(csv_directory, csv_filename), index=False)

    print(csv_filename, "saved in the chosen folder.")


def get_cif_file_count_from_directory(directory):
    """Helper function to count .cif files in a given directory."""
    return len(glob.glob(join(directory, "*.cif")))
