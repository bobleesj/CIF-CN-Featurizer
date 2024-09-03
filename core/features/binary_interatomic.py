from core.optimize import radius as radius_opt
from cifkit import Cif
from core.utils import packing, bond_distance
from core.utils import element_parser
from core.data.radius_handler import (
    get_radius_values_per_element,
)


def compute_binary_interatomic_features(cif: Cif):
    """
    Parse A, B
    """
    # Get A, B
    elements = list(cif.unique_elements)
    A, B = element_parser.get_binary_AB_elements(elements)

    # Get Asize_ref, Bsize_ref
    combined_radii = get_radius_values_per_element(elements, cif.shortest_bond_pair_distance)
    A_CIF_rad = combined_radii[A]["CIF_radius"]
    B_CIF_rad = combined_radii[B]["CIF_radius"]

    shortest_distances_pair_sorted = bond_distance.get_shortest_bond_distances_by_AB(
        cif.shortest_bond_pair_distance, A, B
    )
    distAA, distBB, distAB = bond_distance.get_AA_BB_AB_dists(shortest_distances_pair_sorted)

    radii_refined, obj_value = radius_opt.optimize_CIF_rad_binary(
        A_CIF_rad,
        B_CIF_rad,
        shortest_distances_pair_sorted,
        True,
    )
    A_CIF_rad_refined, B_CIF_rad_refined = radii_refined

    # Distances
    distAB_by_byAsizebyBsize = distAB / (A_CIF_rad + B_CIF_rad)

    distA_A_rad = distAA / 2
    distB_B_rad = distBB / 2

    AA_ref_radius_sum = 2 * A_CIF_rad_refined
    BB_ref_radius_sum = 2 * B_CIF_rad_refined
    AB_ref_radius_sum = A_CIF_rad_refined + B_CIF_rad_refined

    percent_diff_A = (A_CIF_rad_refined - A_CIF_rad) / A_CIF_rad
    percent_diff_B = (B_CIF_rad_refined - B_CIF_rad) / B_CIF_rad

    # Interatomic distance features
    Asize_by_Bsize = A_CIF_rad / B_CIF_rad
    distAA_by_byAsize = distA_A_rad / A_CIF_rad
    distBB_by_byBsize = distB_B_rad / B_CIF_rad
    distAB_by_byAsizebyBsize = distAB / (A_CIF_rad + B_CIF_rad)

    AA_minus_ref_diff = (distAA - AA_ref_radius_sum) / distAA
    BB_minus_ref_diff = (distBB - BB_ref_radius_sum) / distBB
    AB_minus_ref_diff = (distAB - AB_ref_radius_sum) / distAB

    CIF_rad_refined_dict = {
        A: A_CIF_rad_refined,
        B: B_CIF_rad_refined,
    }

    # Packing efficiency
    packing_efficiency = packing.compute_packing_efficiency(
        (A, B),
        cif._loop_values,
        CIF_rad_refined_dict,
        cif.unitcell_lengths,
        cif.unitcell_angles,
    )

    homoatomic_distances = {key: shortest_distances_pair_sorted[key] for key in ["AA", "BB"]}
    heteroatomic_distance = shortest_distances_pair_sorted["AB"]
    shortest_homoatomic_distance = min(homoatomic_distances.values())
    shortest_heteroatomic_distance = heteroatomic_distance

    # Define the CIF and refined radii
    cif_radii = {
        "AA": A_CIF_rad,
        "BB": B_CIF_rad,
        "AB": (A_CIF_rad + B_CIF_rad),
    }
    refined_radii = {
        "AA": A_CIF_rad_refined,
        "BB": B_CIF_rad_refined,
        "AB": (A_CIF_rad_refined + B_CIF_rad_refined),
    }
    percent_diffs = [percent_diff_A, percent_diff_B]

    # Find key of shortest_homoatomic_distance in distances
    shortest_homo_key = [k for k, v in shortest_distances_pair_sorted.items() if v == shortest_homoatomic_distance][0]

    shortest_homoatomic_distance_by_2_by_atom_size = (shortest_homoatomic_distance / 2) / cif_radii[shortest_homo_key]
    shortest_heteroatomic_distance_by_sum_of_atom_sizes = shortest_heteroatomic_distance / cif_radii["AB"]
    shortest_homoatomic_distance_by_2_by_refined_atom_sizes = (shortest_homoatomic_distance / 2) / refined_radii[
        shortest_homo_key
    ]
    shortest_heteroatomic_distance_by_refined_atom_sizes = shortest_heteroatomic_distance / refined_radii["AB"]
    highest_refined_percent_diff = max([abs(p) for p in percent_diffs])
    lowest_refined_percent_diff = min([abs(p) for p in percent_diffs])

    data = {
        "Entry": cif.file_name_without_ext,
        "Formula": cif.formula,
        "Structure": cif.structure,
        "A": A,
        "B": B,
        "INT_distAA": distAA,
        "INT_distBB": distBB,
        "INT_distAB": distAB,
        "INT_Asize": A_CIF_rad,
        "INT_Bsize": B_CIF_rad,
        "INT_Asize_by_Bsize": Asize_by_Bsize,
        "INT_distAA_by2_byAsize": distAA_by_byAsize,
        "INT_distBB_by2_byBsize": distBB_by_byBsize,
        "INT_distAB_by2_byAsizebyBsize": distAB_by_byAsizebyBsize,
        "INT_Asize_ref": A_CIF_rad_refined,
        "INT_Bsize_ref": B_CIF_rad_refined,
        "INT_percent_diff_A_by_100": percent_diff_A,
        "INT_percent_diff_B_by_100": percent_diff_B,
        "INT_distAA_minus_ref_diff": AA_minus_ref_diff,
        "INT_distBB_minus_ref_diff": BB_minus_ref_diff,
        "INT_distAB_minus_ref_diff": AB_minus_ref_diff,
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

    return data, uni_data
