import os
import time
from collections import defaultdict

import click
import pandas as pd
from click import style

from preprocess import cif_parser, supercell, supercell_handler
from feature import interatomic
from feature.output import (
    output_binary,
    output_ternary,
    output_universal,
    output_log,
    output_util,
)
from util import df_util, folder, data, prompt
from preprocess import format
import feature.environment_binary as env_featurizer_binary
import feature.environment_df as env_dataframe
import feature.environment_wyckoff as env_wychoff_featurizer
import feature.coordination_number_df as cn_df


def run_main(is_interactive_mode=True, cif_dir_path=None):
    prompt.print_intro_message()
    radii_data = data.get_radius_data()

    # Initialize DataFrames
    cn_universal_df = pd.DataFrame()
    cn_binary_max_df = pd.DataFrame()
    cn_binary_min_df = pd.DataFrame()
    cn_binary_avg_df = pd.DataFrame()
    cn_ternary_df = pd.DataFrame()
    cn_ternary_max_df = pd.DataFrame()
    cn_ternary_min_df = pd.DataFrame()
    cn_ternary_avg_df = pd.DataFrame()
    cn_binary_df = pd.DataFrame()

    interatomic_binary_df = pd.DataFrame()
    interatomic_ternary_df = pd.DataFrame()
    interatomic_universal_df = pd.DataFrame()
    atomic_env_wyckoff_binary_df = pd.DataFrame()
    atomic_env_wyckoff_ternary_df = pd.DataFrame()
    atomic_env_wyckoff_universal_df = pd.DataFrame()
    atomic_env_binary_df = pd.DataFrame()
    atomic_env_ternary_df = pd.DataFrame()

    # Output
    binary_merged_df = pd.DataFrame()
    ternary_merged_df = pd.DataFrame()
    universal_merged_df = pd.DataFrame()

    # Choose the CIF folder
    if is_interactive_mode:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        supercell_max_atom_count = prompt.get_user_input_on_file_skip()
        cif_dir_path = folder.choose_cif_directory(script_directory)
    else:
        supercell_max_atom_count = 1000

    # Get a list of all .cif files in the chosen directory
    file_path_list = [
        os.path.join(cif_dir_path, file)
        for file in os.listdir(cif_dir_path)
        if file.endswith(".cif")
    ]

    # PART 1: REFORMAT
    format.move_files_based_on_format_error(cif_dir_path)

    # Number of files
    total_file_count = len(file_path_list)

    property_list_excel = pd.read_excel(
        "./element_database/element_properties_for_ML-my elements.xlsx"
    )

    # Initialize DataFrames to store results
    num_files_processed = 0
    running_total_time = 0  # initialize running total execution time
    log_list = []

    # Loop through each CIF file
    for i, filename in enumerate(file_path_list, start=1):
        start_time = time.time()
        num_files_processed += 1
        filename_base = os.path.basename(filename)

        # Retrieve CIF data using the supercell handler
        (
            cif_id,
            cif_block,
            cell_lengths,
            cell_angles_rad,
            cif_loop_values,
            all_coords_list,
        ) = supercell_handler.read_and_prepare_cif_data(filename)
        # Extract points, labels, and unique atom tuples
        (
            supercell_points,
            unique_labels,
            unique_atoms_tuple,
        ) = supercell.get_points_and_labels(all_coords_list, cif_loop_values)

        prompt.print_progress_current(
            i, filename_base, supercell_points, total_file_count
        )
        # Check if the number of atoms exceeds the defined maximum
        if prompt.exceeds_atom_count_limit(
            supercell_points, supercell_max_atom_count
        ):
            click.echo(
                style(
                    f"Skipped - {filename_base} has {len(supercell_points)} atoms",
                    fg="yellow",
                )
            )
            continue

        # Extract formulas and unique atoms from cif block
        (
            unique_atoms_tuple,
            num_of_unique_atoms,
            formula,
        ) = cif_parser.extract_formula_and_atoms(cif_block)

        # Get all pair distances
        atomic_pair_list = supercell.get_atomic_pair_list(
            supercell_points, cell_lengths, cell_angles_rad
        )
        atom_pair_info_dict = supercell.get_atom_pair_info_dict(
            unique_labels, atomic_pair_list
        )
        cif_data = (
            cif_id,
            cell_lengths,
            cell_angles_rad,
            cif_loop_values,
            formula,
        )

        # Determine the compound type based on the number of unique atoms
        isBinary = num_of_unique_atoms == 2
        isTernary = num_of_unique_atoms == 3

        # Initialize a dictionary to count atom occurrences
        atom_counts = defaultdict(int)

        # Identify unique shortest labels for binary environment featurization
        (
            unique_shortest_labels,
            atom_counts,
        ) = env_featurizer_binary.get_unique_shortest_labels(
            atom_pair_info_dict, unique_labels, cif_parser
        )

        if isBinary:
            (
                interatomic_binary_df,
                interatomic_universal_df,
            ) = interatomic.get_interatomic_binary_df(
                filename,
                interatomic_binary_df,
                interatomic_universal_df,
                supercell_points,
                unique_atoms_tuple,
                atomic_pair_list,
                cif_data,
                radii_data,
            )

            (
                atomic_env_wyckoff_binary_df,
                atomic_env_wyckoff_universal_df,
            ) = env_wychoff_featurizer.get_env_wychoff_binary_df(
                filename,
                property_list_excel,
                atomic_env_wyckoff_binary_df,
                atomic_env_wyckoff_universal_df,
                unique_atoms_tuple,
                cif_loop_values,
                radii_data,
                cif_data,
                atomic_pair_list,
            )

            atomic_env_binary_df = env_dataframe.get_env_binary_df(
                atomic_env_binary_df,
                unique_atoms_tuple,
                unique_labels,
                unique_shortest_labels,
                atom_pair_info_dict,
                atom_counts,
                cif_data,
            )

            (
                cn_binary_df,
                cn_universal_df,
            ) = cn_df.get_coordinate_number_binary_df(
                isBinary,
                cn_binary_df,
                cn_universal_df,
                unique_atoms_tuple,
                unique_labels,
                atomic_pair_list,
                atom_pair_info_dict,
                cif_data,
                radii_data,
            )
            df_util.print_df_columns(cn_universal_df)

        if isTernary:
            (
                interatomic_ternary_df,
                interatomic_universal_df,
            ) = interatomic.get_interatomic_ternary_df(
                interatomic_ternary_df,
                interatomic_universal_df,
                unique_atoms_tuple,
                atomic_pair_list,
                cif_data,
                radii_data,
            )

            (
                atomic_env_wyckoff_ternary_df,
                atomic_env_wyckoff_universal_df,
            ) = env_wychoff_featurizer.get_env_wychoff_ternary_df(
                filename,
                property_list_excel,
                atomic_env_wyckoff_ternary_df,
                atomic_env_wyckoff_universal_df,
                unique_atoms_tuple,
                cif_loop_values,
                radii_data,
                cif_data,
                atomic_pair_list,
            )

            atomic_env_ternary_df = env_dataframe.get_env_ternary_df(
                atomic_env_ternary_df,
                unique_atoms_tuple,
                unique_labels,
                unique_shortest_labels,
                atom_pair_info_dict,
                atom_counts,
                cif_data,
            )

            (
                cn_ternary_df,
                cn_universal_df,
            ) = cn_df.get_coordinate_number_ternary_df(
                isBinary,
                cn_ternary_df,
                cn_universal_df,
                unique_atoms_tuple,
                unique_labels,
                atomic_pair_list,
                atom_pair_info_dict,
                cif_data,
                radii_data,
            )

            df_util.print_df_columns(cn_universal_df)

        # Finish the run
        end_time = time.time()
        execution_time = end_time - start_time
        running_total_time += execution_time

        click.echo(
            style(
                f"{execution_time:.2f}s to process {len(supercell_points)}"
                f" atoms (total time {running_total_time:.2f}s)",
                fg="green",
            )
        )

        log_list.append(
            {
                "Filename": filename_base,
                "Entry": cif_id,
                "Formula": formula,
                "Number of atoms": len(supercell_points),
                "Execution time (s)": execution_time,
                "Total time (s)": running_total_time,
            }
        )

    featurizer_log_df = pd.DataFrame(log_list)

    if num_files_processed != 0:
        cols_to_keep = ["Entry", "Formula", "central_atom"]
        click.echo(style(f"Saving csv files in the csv folder", fg="blue"))
        atomic_env_wyckoff_universal_df = df_util.join_columns_with_comma(
            atomic_env_wyckoff_universal_df
        )

        if not cn_binary_df.empty:
            cn_binary_df = df_util.remove_non_numeric_cols(
                cn_binary_df, cols_to_keep
            )

            dfs = df_util.get_avg_min_max_dfs(cn_binary_df, cols_to_keep)
            cn_binary_avg_df, cn_binary_min_df, cn_binary_max_df = dfs
            df_util.print_df_columns(atomic_env_wyckoff_binary_df)
            binary_merged_df = output_binary.postprocess_merge_dfs(
                interatomic_binary_df,
                interatomic_universal_df,
                atomic_env_wyckoff_binary_df,
                atomic_env_binary_df,
                cn_binary_avg_df,
                cn_binary_min_df,
                cn_binary_max_df,
            )

        if not cn_ternary_df.empty:
            cn_ternary_df = df_util.remove_non_numeric_cols(
                cn_ternary_df, cols_to_keep
            )

            dfs = df_util.get_avg_min_max_dfs(cn_ternary_df, cols_to_keep)
            cn_ternary_avg_df, cn_ternary_min_df, cn_ternary_max_df = dfs

            ternary_merged_df = output_ternary.postprocess_merge_dfs(
                interatomic_ternary_df,
                interatomic_universal_df,
                atomic_env_wyckoff_ternary_df,
                atomic_env_ternary_df,
                cn_ternary_avg_df,
                cn_ternary_min_df,
                cn_ternary_max_df,
            )

        # Save universal ouput
        universal_merged_df = output_universal.postprocess_merge_dfs(
            interatomic_universal_df,
            atomic_env_wyckoff_universal_df,
            cn_universal_df,
        )

        # Apply the renaming function to columns
        binary_merged_df.rename(
            columns=output_util.remove_col_prefix_for_formula_info,
            inplace=True,
        )
        ternary_merged_df.rename(
            columns=output_util.remove_col_prefix_for_formula_info,
            inplace=True,
        )

        universal_merged_df.rename(
            columns=output_util.remove_col_prefix_for_formula_info,
            inplace=True,
        )

        if not cn_binary_df.empty:
            folder.save_df_to_csv(
                cif_dir_path, binary_merged_df, "feature_binary"
            )
            df_util.print_df_columns(binary_merged_df)

        if not cn_ternary_df.empty:
            folder.save_df_to_csv(
                cif_dir_path, ternary_merged_df, "feature_ternary"
            )
            df_util.print_df_columns(ternary_merged_df)

        if not universal_merged_df.empty:
            df_util.print_df_columns(universal_merged_df)
            folder.save_df_to_csv(
                cif_dir_path, universal_merged_df, "feature_universal"
            )

        # Save log
        output_log.save_log_csv(
            is_interactive_mode, featurizer_log_df, cif_dir_path
        )


if __name__ == "__main__":
    run_main()
