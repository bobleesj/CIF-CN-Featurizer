from cifkit import Cif
from core.utils.element_parser import (
    get_binary_AB_elements,
    get_ternary_RMX_elements,
)
from core.utils import log
from core.features.coordination import (
    get_CN_metrices_per_method,
    compute_number_of_atoms_in_binary_CN,
    compute_number_of_atoms_in_ternary_CN,
    compute_min_max_avg_per_label,
    compute_global_averages_for_min_max_avg_metrices,
)


def get_CN_atom_count_data(cif: Cif):
    # Compute geometrical features for the CN
    CN_metrices = get_CN_metrices_per_method(cif)
    # Compute min, max, and avg for each site label
    min_max_avg_CN_metrices = compute_min_max_avg_per_label(CN_metrices)

    if len(cif.unique_elements) == 2:
        A, B = get_binary_AB_elements(list(cif.unique_elements))
        CN_atom_count_data = compute_number_of_atoms_in_binary_CN(cif.connections, CN_metrices, A, B)

    if len(cif.unique_elements) == 3:
        R, M, X = get_ternary_RMX_elements(list(cif.unique_elements))
        CN_atom_count_data = compute_number_of_atoms_in_ternary_CN(cif.connections, CN_metrices, R, M, X)

    # Compute the min, max, and avg for each label. Each label has 4 methods
    min_max_avg_CN_count = compute_min_max_avg_per_label(CN_atom_count_data)
    # Find the average of the min, max, and avg across all labels
    avg_CN_metrics = compute_global_averages_for_min_max_avg_metrices(min_max_avg_CN_metrices)
    avg_CN_atom_count = compute_global_averages_for_min_max_avg_metrices(min_max_avg_CN_count)

    return avg_CN_metrics, avg_CN_atom_count


def get_CN_binary_features(cif: Cif):
    avg_CN_metrics, avg_CN_atom_count = get_CN_atom_count_data(cif)

    # Compute average of min, max, and avg

    data = {
        "CN_AVG_coordination_number": avg_CN_metrics["avg"]["number_of_vertices"],
        "CN_AVG_A_atom_count": avg_CN_atom_count["avg"]["A_count"],
        "CN_AVG_B_atom_count": avg_CN_atom_count["avg"]["B_count"],
        "CN_AVG_polyhedron_volume": avg_CN_metrics["avg"]["volume_of_polyhedron"],
        "CN_AVG_central_atom_to_center_of_mass_dist": avg_CN_metrics["avg"]["distance_from_avg_point_to_center"],
        "CN_AVG_number_of_edges": avg_CN_metrics["avg"]["number_of_edges"],
        "CN_AVG_number_of_faces": avg_CN_metrics["avg"]["number_of_faces"],
        "CN_AVG_shortest_distance_to_face": avg_CN_metrics["avg"]["shortest_distance_to_face"],
        "CN_AVG_shortest_distance_to_edge": avg_CN_metrics["avg"]["shortest_distance_to_edge"],
        "CN_AVG_volume_of_inscribed_sphere": avg_CN_metrics["avg"]["volume_of_inscribed_sphere"],
        "CN_AVG_packing_efficiency": avg_CN_metrics["avg"]["packing_efficiency"],
        "CN_MIN_coordination_number": avg_CN_metrics["min"]["number_of_vertices"],
        "CN_MIN_A_atom_count": avg_CN_atom_count["min"]["A_count"],
        "CN_MIN_B_atom_count": avg_CN_atom_count["min"]["B_count"],
        "CN_MIN_polyhedron_volume": avg_CN_metrics["min"]["volume_of_polyhedron"],
        "CN_MIN_central_atom_to_center_of_mass_dist": avg_CN_metrics["min"]["distance_from_avg_point_to_center"],
        "CN_MIN_number_of_edges": avg_CN_metrics["min"]["number_of_edges"],
        "CN_MIN_number_of_faces": avg_CN_metrics["min"]["number_of_faces"],
        "CN_MIN_shortest_distance_to_face": avg_CN_metrics["min"]["shortest_distance_to_face"],
        "CN_MIN_shortest_distance_to_edge": avg_CN_metrics["min"]["shortest_distance_to_edge"],
        "CN_MIN_volume_of_inscribed_sphere": avg_CN_metrics["min"]["volume_of_inscribed_sphere"],
        "CN_MIN_packing_efficiency": avg_CN_metrics["min"]["packing_efficiency"],
        "CN_MAX_coordination_number": avg_CN_metrics["min"]["number_of_vertices"],
        "CN_MAX_A_atom_count": avg_CN_atom_count["max"]["A_count"],
        "CN_MAX_B_atom_count": avg_CN_atom_count["max"]["B_count"],
        "CN_MAX_polyhedron_volume": avg_CN_metrics["max"]["volume_of_polyhedron"],
        "CN_MAX_central_atom_to_center_of_mass_dist": avg_CN_metrics["max"]["distance_from_avg_point_to_center"],
        "CN_MAX_number_of_edges": avg_CN_metrics["max"]["number_of_edges"],
        "CN_MAX_number_of_faces": avg_CN_metrics["max"]["number_of_faces"],
        "CN_MAX_shortest_distance_to_face": avg_CN_metrics["max"]["shortest_distance_to_face"],
        "CN_MAX_shortest_distance_to_edge": avg_CN_metrics["max"]["shortest_distance_to_edge"],
        "CN_MAX_volume_of_inscribed_sphere": avg_CN_metrics["max"]["volume_of_inscribed_sphere"],
        "CN_MAX_packing_efficiency": avg_CN_metrics["max"]["packing_efficiency"],
    }

    # log.print_dict_pretty(data, "env binary")
    # log.print_connected_points(cif.connections)
    return data


def get_CN_ternary_features(cif: Cif):
    avg_CN_metrics, avg_CN_atom_count = get_CN_atom_count_data(cif)

    # Compute average of min, max, and avg

    data = {
        "CN_AVG_coordination_number": avg_CN_metrics["avg"]["number_of_vertices"],
        "CN_AVG_R_atom_count": avg_CN_atom_count["avg"]["R_count"],
        "CN_AVG_M_atom_count": avg_CN_atom_count["avg"]["M_count"],
        "CN_AVG_X_atom_count": avg_CN_atom_count["avg"]["X_count"],
        "CN_AVG_polyhedron_volume": avg_CN_metrics["avg"]["volume_of_polyhedron"],
        "CN_AVG_central_atom_to_center_of_mass_dist": avg_CN_metrics["avg"]["distance_from_avg_point_to_center"],
        "CN_AVG_number_of_edges": avg_CN_metrics["avg"]["number_of_edges"],
        "CN_AVG_number_of_faces": avg_CN_metrics["avg"]["number_of_faces"],
        "CN_AVG_shortest_distance_to_face": avg_CN_metrics["avg"]["shortest_distance_to_face"],
        "CN_AVG_shortest_distance_to_edge": avg_CN_metrics["avg"]["shortest_distance_to_edge"],
        "CN_AVG_volume_of_inscribed_sphere": avg_CN_metrics["avg"]["volume_of_inscribed_sphere"],
        "CN_AVG_packing_efficiency": avg_CN_metrics["avg"]["packing_efficiency"],
        "CN_MIN_coordination_number": avg_CN_metrics["min"]["number_of_vertices"],
        "CN_MIN_R_atom_count": avg_CN_atom_count["min"]["R_count"],
        "CN_MIN_M_atom_count": avg_CN_atom_count["min"]["M_count"],
        "CN_MIN_X_atom_count": avg_CN_atom_count["min"]["X_count"],
        "CN_MIN_polyhedron_volume": avg_CN_metrics["min"]["volume_of_polyhedron"],
        "CN_MIN_central_atom_to_center_of_mass_dist": avg_CN_metrics["min"]["distance_from_avg_point_to_center"],
        "CN_MIN_number_of_edges": avg_CN_metrics["min"]["number_of_edges"],
        "CN_MIN_number_of_faces": avg_CN_metrics["min"]["number_of_faces"],
        "CN_MIN_shortest_distance_to_face": avg_CN_metrics["min"]["shortest_distance_to_face"],
        "CN_MIN_shortest_distance_to_edge": avg_CN_metrics["min"]["shortest_distance_to_edge"],
        "CN_MIN_volume_of_inscribed_sphere": avg_CN_metrics["min"]["volume_of_inscribed_sphere"],
        "CN_MIN_packing_efficiency": avg_CN_metrics["min"]["packing_efficiency"],
        "CN_MAX_coordination_number": avg_CN_metrics["max"]["number_of_vertices"],
        "CN_MAX_R_atom_count": avg_CN_atom_count["max"]["R_count"],
        "CN_MAX_M_atom_count": avg_CN_atom_count["max"]["M_count"],
        "CN_MAX_X_atom_count": avg_CN_atom_count["max"]["X_count"],
        "CN_MAX_polyhedron_volume": avg_CN_metrics["max"]["volume_of_polyhedron"],
        "CN_MAX_central_atom_to_center_of_mass_dist": avg_CN_metrics["max"]["distance_from_avg_point_to_center"],
        "CN_MAX_number_of_edges": avg_CN_metrics["max"]["number_of_edges"],
        "CN_MAX_number_of_faces": avg_CN_metrics["max"]["number_of_faces"],
        "CN_MAX_shortest_distance_to_face": avg_CN_metrics["max"]["shortest_distance_to_face"],
        "CN_MAX_shortest_distance_to_edge": avg_CN_metrics["max"]["shortest_distance_to_edge"],
        "CN_MAX_volume_of_inscribed_sphere": avg_CN_metrics["max"]["volume_of_inscribed_sphere"],
        "CN_MAX_packing_efficiency": avg_CN_metrics["max"]["packing_efficiency"],
    }

    return data
