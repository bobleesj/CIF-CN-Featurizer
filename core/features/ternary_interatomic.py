from core.optimize import radius as radius_opt
from cifkit import Cif
from core.utils import log, packing, bond_distance
from core.utils import element_parser
from core.data.radius_handler import (
    get_radius_values_per_element,
)


def compute_ternary_interatomic_features(cif: Cif):
    elements = list(cif.unique_elements)
    R, M, X = element_parser.get_ternary_RMX_elements(elements)

    # Get Asize_ref, Bsize_ref
    combined_radii = get_radius_values_per_element(elements, cif.shortest_bond_pair_distance)
    R_CIF_rad = combined_radii[R]["CIF_radius"]
    M_CIF_rad = combined_radii[M]["CIF_radius"]
    X_CIF_rad = combined_radii[X]["CIF_radius"]

    shortest_distances_pair_sorted = bond_distance.get_shortest_bond_distances_by_RMX(
        cif.shortest_bond_pair_distance, R, M, X
    )

    distRR, distMM, distXX, distRM, distRX, distMX = bond_distance.get_RR_MM_XX_RM_RX_MX_dists(
        shortest_distances_pair_sorted
    )

    radii, obj_value = radius_opt.optimize_CIF_rad_ternary(
        R_CIF_rad,
        M_CIF_rad,
        X_CIF_rad,
        shortest_distances_pair_sorted,
        True,
    )
    R_CIF_rad_refined, M_CIF_rad_refined, X_CIF_rad_refined = radii

    # # Distances
    distRM_by_byRsizebyMsize = distRM / (R_CIF_rad + M_CIF_rad)
    distRX_by_byRsizebyXsize = distRX / (R_CIF_rad + X_CIF_rad)
    distMX_by_byMsizebyXsize = distMX / (M_CIF_rad + X_CIF_rad)

    distR_R_rad = distRR / 2
    distM_M_rad = distMM / 2
    distX_X_rad = distXX / 2

    RR_radius_sum = 2 * R_CIF_rad_refined
    MM_radius_sum = 2 * M_CIF_rad_refined
    XX_radius_sum = 2 * X_CIF_rad_refined
    RM_radius_sum = R_CIF_rad_refined + M_CIF_rad_refined
    RX_radius_sum = R_CIF_rad_refined + X_CIF_rad_refined
    MX_radius_sum = M_CIF_rad_refined + X_CIF_rad_refined

    percent_diff_R = (R_CIF_rad_refined - R_CIF_rad) / R_CIF_rad
    percent_diff_M = (M_CIF_rad_refined - M_CIF_rad) / M_CIF_rad
    percent_diff_X = (X_CIF_rad_refined - X_CIF_rad) / X_CIF_rad

    # Interatomic distance features
    Rsize_by_Msize = R_CIF_rad / M_CIF_rad
    Msize_by_Xsize = M_CIF_rad / X_CIF_rad
    Rsize_by_Xsize = R_CIF_rad / X_CIF_rad

    distRR_by_byRsize = distR_R_rad / R_CIF_rad
    distMM_by_byMsize = distM_M_rad / M_CIF_rad
    distXX_by_byXsize = distX_X_rad / X_CIF_rad
    distRM_by_byRsizebyMsize = distRM / (R_CIF_rad + M_CIF_rad)
    distMX_by_byMsizebyXsize = distMX / (M_CIF_rad + X_CIF_rad)

    RR_minus_ref_diff = (distRR - RR_radius_sum) / distRR
    MM_minus_ref_diff = (distMM - MM_radius_sum) / distMM
    XX_minus_ref_diff = (distXX - XX_radius_sum) / distXX
    RM_minus_ref_diff = (distRM - RM_radius_sum) / distRM
    RX_minus_ref_diff = (distRX - RX_radius_sum) / distRX
    MX_minus_ref_diff = (distMX - MX_radius_sum) / distMX

    CIF_rad_refined_dict = {
        R: R_CIF_rad_refined,
        M: M_CIF_rad_refined,
        X: X_CIF_rad_refined,
    }

    # Packing efficiency
    packing_efficiency = packing.compute_packing_efficiency(
        (R, M, X),
        cif._loop_values,
        CIF_rad_refined_dict,
        cif.unitcell_lengths,
        cif.unitcell_angles,
    )

    # Get the shortest homo/hetroatomic distance
    homoatomic_distances = {key: shortest_distances_pair_sorted[key] for key in ["RR", "MM", "XX"]}
    heteroatomic_distances = {key: shortest_distances_pair_sorted[key] for key in ["RM", "MX", "RX"]}
    shortest_homoatomic_distance = min(homoatomic_distances.values())
    shortest_heteroatomic_distance = min(heteroatomic_distances.values())

    # Parse the CIF radis based on the shortest homo/heteroatomic distance
    cif_radii = {
        "RR": R_CIF_rad,
        "MM": M_CIF_rad,
        "XX": X_CIF_rad,
        "RM": (R_CIF_rad + M_CIF_rad),
        "MX": (M_CIF_rad + X_CIF_rad),
        "RX": (R_CIF_rad + X_CIF_rad),
    }

    refined_radii = {
        "RR": R_CIF_rad_refined,
        "MM": M_CIF_rad_refined,
        "XX": X_CIF_rad_refined,
        "RM": (R_CIF_rad_refined + M_CIF_rad_refined),
        "MX": (M_CIF_rad_refined + X_CIF_rad_refined),
        "RX": (R_CIF_rad_refined + X_CIF_rad_refined),
    }

    percent_diffs = [percent_diff_R, percent_diff_M, percent_diff_X]

    shortest_homo_key = [k for k, v in shortest_distances_pair_sorted.items() if v == shortest_homoatomic_distance][0]
    shortest_hetero_key = [k for k, v in shortest_distances_pair_sorted.items() if v == shortest_heteroatomic_distance][
        0
    ]

    # Extract 9 universal features for Ternary
    shortest_homoatomic_distance_by_2_by_atom_size = (shortest_homoatomic_distance / 2) / cif_radii[shortest_homo_key]
    shortest_heteroatomic_distance_by_sum_of_atom_sizes = (
        shortest_heteroatomic_distance / cif_radii[shortest_hetero_key]
    )
    shortest_homoatomic_distance_by_2_by_refined_atom_sizes = (shortest_homoatomic_distance / 2) / refined_radii[
        shortest_homo_key
    ]
    shortest_heteroatomic_distance_by_refined_atom_sizes = (
        shortest_heteroatomic_distance / refined_radii[shortest_hetero_key]
    )
    highest_refined_percent_diff = max([abs(p) for p in percent_diffs])
    lowest_refined_percent_diff = min([abs(p) for p in percent_diffs])

    data = {
        "Entry": cif.file_name_without_ext,
        "Formula": cif.formula,
        "Structure": cif.structure,
        "R": R,
        "M": M,
        "X": X,
        "INT_distRR": distRR,
        "INT_distMM": distMM,
        "INT_distXX": distXX,
        "INT_distRM": distRM,
        "INT_distMX": distMX,
        "INT_distRX": distRX,
        "INT_Rsize": R_CIF_rad,
        "INT_Msize": M_CIF_rad,
        "INT_Xsize": X_CIF_rad,
        "INT_Rsize_by_Msize": Rsize_by_Msize,
        "INT_Msize_by_Xsize": Msize_by_Xsize,
        "INT_Rsize_by_Xsize": Rsize_by_Xsize,
        "INT_distRR_by2_byRsize": distRR_by_byRsize,
        "INT_distMM_by2_byMsize": distMM_by_byMsize,
        "INT_distXX_by2_byXsize": distXX_by_byXsize,
        "INT_distRM_byRsizebyMsize": distRM_by_byRsizebyMsize,
        "INT_distMX_byMsizebyXsize": distMX_by_byMsizebyXsize,
        "INT_distRX_byRsizebyXsize": distRX_by_byRsizebyXsize,
        "INT_Rsize_ref": R_CIF_rad_refined,
        "INT_Msize_ref": M_CIF_rad_refined,
        "INT_Xsize_ref": X_CIF_rad_refined,
        "INT_percent_diff_R_by_100": percent_diff_R,
        "INT_percent_diff_M_by_100": percent_diff_M,
        "INT_percent_diff_X_by_100": percent_diff_X,
        "INT_distRR_minus_ref_diff": RR_minus_ref_diff,
        "INT_distMM_minus_ref_diff": MM_minus_ref_diff,
        "INT_distXX_minus_ref_diff": XX_minus_ref_diff,
        "INT_distRM_minus_ref_diff": RM_minus_ref_diff,
        "INT_distMX_minus_ref_diff": MX_minus_ref_diff,
        "INT_distRX_minus_ref_diff": RX_minus_ref_diff,
        "INT_R_factor": obj_value,
        "INT_UNI_shortest_homoatomic_dist": shortest_homoatomic_distance,
        "INT_UNI_shortest_heteroatomic_dist": shortest_heteroatomic_distance,
        "INT_UNI_shortest_homoatomic_dist_by_2_by_atom_size": shortest_homoatomic_distance_by_2_by_atom_size,
        "INT_UNI_shortest_heteroatomic_dist_by_sum_of_atom_sizes": shortest_heteroatomic_distance_by_sum_of_atom_sizes,
        "INT_UNI_shortest_homoatomic_dist_by_2_by_refined_atom_size": shortest_homoatomic_distance_by_2_by_refined_atom_sizes,
        "INT_UNI_shortest_heteroatomic_dist_by_sum_of_refined_atom_sizes": shortest_heteroatomic_distance_by_refined_atom_sizes,
        "INT_UNI_highest_refined_percent_diff_abs": highest_refined_percent_diff,
        "INT_UNI_lowest_refined_percent_diff_abs": lowest_refined_percent_diff,
        "INT_UNI_refined_packing_efficiency": packing_efficiency,
    }

    uni_data = {
        "Entry": cif.file_name_without_ext,
        "Formula": cif.formula,
        "INT_UNI_shortest_homoatomic_dist": shortest_homoatomic_distance,
        "INT_UNI_shortest_heteroatomic_dist": shortest_heteroatomic_distance,
        "INT_UNI_shortest_homoatomic_dist_by_2_by_atom_size": shortest_homoatomic_distance_by_2_by_atom_size,
        "INT_UNI_shortest_heteroatomic_dist_by_sum_of_atom_sizes": shortest_heteroatomic_distance_by_sum_of_atom_sizes,
        "INT_UNI_shortest_homoatomic_dist_by_2_by_refined_atom_size": shortest_homoatomic_distance_by_2_by_refined_atom_sizes,
        "INT_UNI_shortest_heteroatomic_dist_by_sum_of_refined_atom_sizes": shortest_heteroatomic_distance_by_refined_atom_sizes,
        "INT_UNI_highest_refined_percent_diff_abs": highest_refined_percent_diff,
        "INT_UNI_lowest_refined_percent_diff_abs": lowest_refined_percent_diff,
        "INT_UNI_refined_packing_efficiency": packing_efficiency,
    }
    # log.print_dict_pretty(data, "ternar_int")
    return data, uni_data
