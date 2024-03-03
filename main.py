# Standard library imports
import os
import time
from collections import defaultdict

# Related third-party imports
import click
import pandas as pd
from click import style

# Local application/library specific imports
import preprocess.cif_parser as cif_parser
import preprocess.supercell as supercell
import preprocess.supercell_handler as supercell_handler
import featurizer.interatomic as interatomic_featurizer
import featurizer.environment_binary as env_featurizer_binary
import featurizer.environment_dataframe as env_dataframe
import featurizer.environment_ternary as env_featurizer_ternary
import featurizer.environment_wyckoff as env_wychoff_featurizer
import featurizer.coordinate_number_dataframe as coordinate_number_dataframe
import util.data as db
import util.dataframe as df
from util.folder import choose_CIF_directory, save_to_csv_directory
import util.prompt as prompt
from util.unit import round_df


def run_main():
    
    # Configurations and initializations
    radii_data = db.get_radii_data()

    # Initialize DataFrames
    cn_binary_df = pd.DataFrame()
    cn_binary_max_df = pd.DataFrame()
    cn_binary_min_df = pd.DataFrame()
    cn_binary_avg_df = pd.DataFrame()
    cn_ternary_df = pd.DataFrame()
    cn_ternary_max_df = pd.DataFrame()
    cn_ternary_min_df = pd.DataFrame()
    cn_ternary_avg_df = pd.DataFrame()
    interatomic_binary_df = pd.DataFrame()
    interatomic_ternary_df = pd.DataFrame()
    interatomic_universal_df = pd.DataFrame()
    atomic_env_wyckoff_binary_df = pd.DataFrame()
    atomic_env_wyckoff_ternary_df = pd.DataFrame()
    atomic_env_wyckoff_universal_df = pd.DataFrame()
    atomic_env_binary_df = pd.DataFrame()
    atomic_env_ternary_df = pd.DataFrame()

    # Get user input on skipping file based on supercell size
    supercell_max_atom_count = prompt.get_user_input_on_file_skip()
    
    # Get current main.py directory
    script_directory = os.path.dirname(os.path.abspath(__file__))  

    # Choose the CIF folder  
    cif_folder_dir = choose_CIF_directory(script_directory)

    # Get a list of all .cif files in the chosen directory
    file_path_list = [os.path.join(cif_folder_dir, file) for file in os.listdir(cif_folder_dir) if file.endswith('.cif')]
    
    # Number of files
    total_files = len(file_path_list)

    property_list_excel = pd.read_excel('./element_database/element_properties_for_ML-my elements.xlsx') 
    
    # Initialize DataFrames to store results
    num_files_processed = 0
    running_total_time = 0  # initialize running total execution time
    log_list = []
    
    # Loop through each CIF file
    for idx, filename in enumerate(file_path_list, start=1):
        start_time = time.time()
        num_files_processed += 1
        filename_base = os.path.basename(filename)
        print(f"\n({idx}/{total_files}) Processing {filename_base}...")
    
        # Retrieve CIF data using the supercell handler
        CIF_id, CIF_block, cell_lengths, cell_angles_rad, CIF_loop_values, all_coords_list = supercell_handler.read_and_prepare_cif_data(filename)        
        # Extract points, labels, and unique atom tuples from the coordinates list and loop values
        all_points, unique_labels, unique_atoms_tuple = supercell.get_points_and_labels(all_coords_list, CIF_loop_values)
        
        # Check if the number of atoms exceeds the defined maximum, skipping the file if so
        if prompt.exceeds_atom_count_limit(all_points, supercell_max_atom_count):
            click.echo(style(f"Skipped - {filename_base} has {len(all_points)} atoms", fg="yellow"))
            continue

        # Calculate interatomic distances and organize into a list and dictionary
        unique_atoms_tuple, num_of_unique_atoms, formula_string = cif_parser.extract_formula_and_atoms(CIF_block)
        atomic_pair_list = supercell.get_atomic_pair_list(all_points, cell_lengths, cell_angles_rad)
        atom_pair_info_dict = supercell.get_atom_pair_info_dict(unique_labels, atomic_pair_list)
        CIF_data = (CIF_id, cell_lengths, cell_angles_rad, CIF_loop_values, formula_string)

        # Determine the compound type based on the number of unique atoms
        isBinary = num_of_unique_atoms == 2
        isTernary = num_of_unique_atoms == 3

        # Initialize a dictionary to count atom occurrences
        atom_counts = defaultdict(int)

        # Identify unique shortest labels for binary environment featurization
        unique_shortest_labels, atom_counts = env_featurizer_binary.get_unique_shortest_labels(
            atom_pair_info_dict,
            unique_labels,
            cif_parser
        )
            
        if isBinary:
            interatomic_binary_df, interatomic_universal_df = interatomic_featurizer.get_interatomic_binary_df(
                filename,
                interatomic_binary_df,
                interatomic_universal_df,
                all_points,
                unique_atoms_tuple,
                atomic_pair_list,
                CIF_data,
                radii_data
            )
            
            atomic_env_wyckoff_binary_df, atomic_env_wyckoff_universal_df = env_wychoff_featurizer.get_env_wychoff_binary_df(
                filename,
                property_list_excel,
                atomic_env_wyckoff_binary_df,
                atomic_env_wyckoff_universal_df,
                unique_atoms_tuple,
                CIF_loop_values,
                radii_data,
                CIF_data,
                atomic_pair_list
            )
                        

            atomic_env_binary_df = env_dataframe.get_env_binary_df(
                atomic_env_binary_df,
                unique_atoms_tuple,
                unique_labels,
                unique_shortest_labels,
                atom_pair_info_dict,
                atom_counts,
                CIF_data
            )
            
            cn_binary_df = coordinate_number_dataframe.get_coordinate_number_binary_df(
                isBinary,
                cn_binary_df,
                unique_atoms_tuple,
                unique_labels,
                atomic_pair_list,
                atom_pair_info_dict,
                CIF_data,
                radii_data
            )
                        
        if isTernary:
            interatomic_ternary_df, interatomic_universal_df = interatomic_featurizer.get_interatomic_ternary_df(
                interatomic_ternary_df,
                interatomic_universal_df,
                unique_atoms_tuple,
                atomic_pair_list,
                CIF_data,
                radii_data
            )

            atomic_env_wyckoff_ternary_df, atomic_env_wyckoff_universal_df = env_wychoff_featurizer.get_env_wychoff_ternary_df(
                filename,
                property_list_excel,
                atomic_env_wyckoff_ternary_df,
                atomic_env_wyckoff_universal_df,
                unique_atoms_tuple,
                CIF_loop_values,
                radii_data,
                CIF_data,
                atomic_pair_list
            )

            atomic_env_ternary_df = env_dataframe.get_env_ternary_df(
                atomic_env_ternary_df,
                unique_atoms_tuple,
                unique_labels,
                unique_shortest_labels,
                atom_pair_info_dict,
                atom_counts,
                CIF_data
            )      
            
            cn_ternary_df = coordinate_number_dataframe.get_coordinate_number_ternary_df(
                isBinary,
                cn_ternary_df,
                unique_atoms_tuple,
                unique_labels,
                atomic_pair_list,  # Added the missing comma
                atom_pair_info_dict,
                CIF_data,
                radii_data)

        # Finish the run
        end_time = time.time()
        execution_time = end_time - start_time
        running_total_time += execution_time
        click.echo(style(f"{execution_time:.2f}s to process {len(all_points)} atoms (total time {running_total_time:.2f}s)", fg="green"))

        log_list.append({
            "Filename": filename_base,
            "CIF": CIF_id,
            "Compound": formula_string,
            "Number of atoms": len(all_points),
            "Execution time (s)": execution_time,
            "Total_time (s)": running_total_time
        })

    featurizer_log_df = pd.DataFrame(log_list)
    featurizer_log_df = featurizer_log_df.round(3)

    # Note: Save csv file using an individual function for ease of debugging purposes
    if num_files_processed != 0:
        cols_to_keep = ['CIF_id', 'Compound', 'Central atom']
        click.echo(style(f"Saving csv files in the csv folder", fg="blue"))
        atomic_env_wyckoff_universal_df = df.join_columns_with_comma(atomic_env_wyckoff_universal_df)

        if not cn_binary_df.empty:
            binary_non_numeric_cols_to_remove = cn_binary_df.select_dtypes(include=['object']).columns.difference(cols_to_keep)
            cn_binary_df = cn_binary_df.drop(binary_non_numeric_cols_to_remove, axis=1)                        
            atomic_env_wyckoff_binary_df = df.wyckoff_mapping_to_number_binary(atomic_env_wyckoff_binary_df)
            cn_binary_avg_df = cn_binary_df.groupby(cols_to_keep).mean().reset_index()
            cn_binary_min_df = cn_binary_df.groupby(cols_to_keep).min().reset_index()
            cn_binary_max_df = cn_binary_df.groupby(cols_to_keep).max().reset_index()
            save_to_csv_directory(cif_folder_dir, round_df(cn_binary_df), "coordination_number_binary_all")
            save_to_csv_directory(cif_folder_dir, round_df(cn_binary_avg_df), "coordination_number_binary_avg")
            save_to_csv_directory(cif_folder_dir, round_df(cn_binary_min_df), "coordination_number_binary_min")
            save_to_csv_directory(cif_folder_dir, round_df(cn_binary_max_df), "coordination_number_binary_max")
            save_to_csv_directory(cif_folder_dir, round_df(interatomic_binary_df), "interatomic_features_binary")
            save_to_csv_directory(cif_folder_dir, round_df(atomic_env_binary_df), "atomic_environment_features_binary")
            save_to_csv_directory(cif_folder_dir, round_df(atomic_env_wyckoff_binary_df), "atomic_environment_wyckoff_multiplicity_features_binary")

        if not cn_ternary_df.empty:
            ternary_non_numeric_cols_to_remove = cn_ternary_df.select_dtypes(include=['object']).columns.difference(cols_to_keep)
            cn_ternary_df = cn_ternary_df.drop(ternary_non_numeric_cols_to_remove, axis=1)   
            cn_ternary_avg_df = cn_ternary_df.groupby(cols_to_keep).mean().reset_index()
            cn_ternary_min_df = cn_ternary_df.groupby(cols_to_keep).min().reset_index()
            cn_ternary_max_df = cn_ternary_df.groupby(cols_to_keep).max().reset_index()
            atomic_env_wyckoff_ternary_df = df.wyckoff_mapping_to_number_ternary(atomic_env_wyckoff_ternary_df)            
            save_to_csv_directory(cif_folder_dir, round_df(cn_ternary_df), "coordination_number_ternary_all")
            save_to_csv_directory(cif_folder_dir, round_df(cn_ternary_avg_df), "coordination_number_ternary_avg")
            save_to_csv_directory(cif_folder_dir, round_df(cn_ternary_min_df), "coordination_number_ternary_min")
            save_to_csv_directory(cif_folder_dir, round_df(cn_ternary_max_df), "coordination_number_ternary_max")
            save_to_csv_directory(cif_folder_dir, round_df(interatomic_ternary_df), "interatomic_features_ternary")
            save_to_csv_directory(cif_folder_dir, round_df(atomic_env_ternary_df), "atomic_environment_features_ternary")
            save_to_csv_directory(cif_folder_dir, round_df(atomic_env_wyckoff_ternary_df), "atomic_environment_wyckoff_multiplicity_features_tenary")
    
        save_to_csv_directory(cif_folder_dir, round_df(interatomic_universal_df), "interatomic_features_universal")
        save_to_csv_directory(cif_folder_dir, round_df(atomic_env_wyckoff_universal_df), "atomic_environment_wyckoff_multiplicity_features_universal")
        save_to_csv_directory(cif_folder_dir, round_df(featurizer_log_df), "featurizer_log")

if __name__ == "__main__":
    run_main()