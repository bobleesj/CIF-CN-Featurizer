import pandas as pd
import feature.distance as distance
import preprocess.optimize as optimize
import util.data as data
from util import df_util
import feature.coordination_number as cn_featurizer
import os
import time


def get_coordinate_number_binary_df(
    isBinary,
    cn_binary_df,
    cn_universal_df,
    unique_atoms_tuple,
    unique_labels,
    atomic_pair_list,
    atom_pair_info_dict,
    CIF_data,
    radii_data,
):
    (
        CIF_id,
        cell_lengths,
        cell_angles_rad,
        CIF_loop_values,
        formula_string,
    ) = CIF_data

    A, B = unique_atoms_tuple[0][0], unique_atoms_tuple[1][0]
    R = M = X = ""

    atoms_for_radii = [
        unique_atoms_tuple[0][0],
        unique_atoms_tuple[1][0],
    ]  # [A, B]
    atom_radii = data.get_atom_radii(atoms_for_radii, radii_data)
    A_CIF_rad, A_Pauling_rad = atom_radii[A]["CIF"], atom_radii[A]["Pauling"]
    B_CIF_rad, B_Pauling_rad = atom_radii[B]["CIF"], atom_radii[B]["Pauling"]

    (
        shortest_AA,
        shortest_BB,
        shortest_AB,
    ) = distance.find_shortest_pair_distances(
        isBinary, unique_atoms_tuple, atomic_pair_list
    )
    shortest_distances_pair = {
        "AA": shortest_AA,
        "BB": shortest_BB,
        "AB": shortest_AB,
    }
    A_CIF_rad_refined, B_CIF_rad_refined = optimize.optimize_CIF_rad_binary(
        A_CIF_rad, B_CIF_rad, shortest_distances_pair
    )
    rad_sum_binary = data.compute_rad_sum_binary(
        A_CIF_rad,
        B_CIF_rad,
        A_CIF_rad_refined,
        B_CIF_rad_refined,
        A_Pauling_rad,
        B_Pauling_rad,
    )

    # Insert values for unique_labels, output_dict
    CN_counts = cn_featurizer.calculate_diff_counts_per_label(
        unique_labels, atom_pair_info_dict, rad_sum_binary, A, B, R, M, X
    )
    atom_labels = {"A": A, "B": B, "R": R, "M": M, "X": X}

    for label in unique_labels:
        df = cn_featurizer.process_labels(
            label,
            atom_pair_info_dict,
            CN_counts,
            cell_lengths,
            cell_angles_rad,
            atom_labels,
            rad_sum_binary,
            CIF_id,
            formula_string,
        )
        cn_binary_df = pd.concat([cn_binary_df, df], ignore_index=True)

        columns_to_drop = [
            "A_atom_count",
            "B_atom_count",
            "Formula",
        ]
        cn_universal_df = pd.concat(
            [cn_universal_df, df.drop(columns=columns_to_drop)],
            ignore_index=True,
        )

    return cn_binary_df, cn_universal_df


def get_coordinate_number_ternary_df(
    isBinary,
    cn_ternary_df,
    cn_universal_df,
    unique_atoms_tuple,
    unique_labels,
    atomic_pair_list,
    atom_pair_info_dict,
    CIF_data,
    radii_data,
):
    R, M, X = (
        unique_atoms_tuple[0][0],
        unique_atoms_tuple[1][0],
        unique_atoms_tuple[2][0],
    )
    A = B = ""

    (
        CIF_id,
        cell_lengths,
        cell_angles_rad,
        CIF_loop_values,
        formula_string,
    ) = CIF_data

    atoms = [R, M, X]
    atom_radii = data.get_atom_radii(atoms, radii_data)
    R_CIF_rad, R_Pauling_rad = atom_radii[R]["CIF"], atom_radii[R]["Pauling"]
    M_CIF_rad, M_Pauling_rad = atom_radii[M]["CIF"], atom_radii[M]["Pauling"]
    X_CIF_rad, X_Pauling_rad = atom_radii[X]["CIF"], atom_radii[X]["Pauling"]

    # Initialize the shortest distances with a large number
    (
        shortest_RR,
        shortest_MM,
        shortest_XX,
        shortest_RM,
        shortest_MX,
        shortest_RX,
    ) = distance.find_shortest_pair_distances(
        isBinary, unique_atoms_tuple, atomic_pair_list
    )

    # Put distances into a dictionary
    shortest_distances_pair = {
        "RR": shortest_RR,
        "MM": shortest_MM,
        "XX": shortest_XX,
        "RM": shortest_RM,
        "MX": shortest_MX,
        "RX": shortest_RX,
    }

    (
        R_CIF_rad_refined,
        M_CIF_rad_refined,
        X_CIF_rad_refined,
    ) = optimize.optimize_CIF_rad_ternary(
        R_CIF_rad, M_CIF_rad, X_CIF_rad, shortest_distances_pair
    )
    rad_sum_ternary = data.compute_rad_sum_ternary(
        R_CIF_rad,
        M_CIF_rad,
        X_CIF_rad,
        R_CIF_rad_refined,
        M_CIF_rad_refined,
        X_CIF_rad_refined,
        R_Pauling_rad,
        M_Pauling_rad,
        X_Pauling_rad,
    )

    # Insert values for unique_labels, output_dict
    CN_counts = cn_featurizer.calculate_diff_counts_per_label(
        unique_labels, atom_pair_info_dict, rad_sum_ternary, A, B, R, M, X
    )
    atom_labels = {"A": A, "B": B, "R": R, "M": M, "X": X}

    columns_to_drop = [
        "R_atom_count",
        "M_atom_count",
        "X_atom_count",
        "Formula",
    ]

    for label in unique_labels:
        df = cn_featurizer.process_labels(
            label,
            atom_pair_info_dict,
            CN_counts,
            cell_lengths,
            cell_angles_rad,
            atom_labels,
            rad_sum_ternary,
            CIF_id,
            formula_string,
            isTernary=True,
        )
        cn_ternary_df = pd.concat([cn_ternary_df, df], ignore_index=True)
        cn_universal_df = pd.concat(
            [cn_universal_df, df.drop(columns=columns_to_drop)],
            ignore_index=True,
        )

    return cn_ternary_df, cn_universal_df


def get_coordniate_number_df(
    metrics, atom_counts, atom_labels, formula_string, label, dist_type, CIF_id
):
    """
    Generates a DataFrame containing information
    derived from metrics, atom_counts, and other provided arguments.
    """
    data = {
        "Entry": [CIF_id],
        "Formula": [formula_string],
        "central_atom": [label],
        "CN_method": [dist_type],
        "coordination_number": [metrics["number_of_vertices"]],
    }

    # Insert atom counts after CN_number
    for atom, count in zip(atom_labels, atom_counts):
        data[f"{atom}_atom_count"] = [count]

    # Append the remaining columns
    data.update(
        {
            "polyhedron_volume": [metrics["Volume_of_polyhedron"]],
            "central_atom_to_center_of_mass_dist": [
                metrics["distance_to_center"]
            ],
            "number_of_edges": [metrics["number_of_edges"]],
            "number_of_faces": [metrics["number_of_faces"]],
            "shortest_distance_to_face": [
                metrics["shortest_distance_to_face"]
            ],
            "shortest_distance_to_edge": [
                metrics["shortest_distance_to_edge"]
            ],
            "volume_of_inscribed_sphere": [
                metrics["volume_of_inscribed_sphere"]
            ],
            "packing_efficiency": [metrics["packing_efficiency"]],
        }
    )

    return pd.DataFrame(data)


def calculate_execution_time(start_time, running_total_time):
    """
    Calculatse execution time based on the
    provided start time and update the running total time.
    """
    end_time = time.time()
    execution_time = end_time - start_time
    running_total_time += execution_time

    return execution_time, running_total_time
