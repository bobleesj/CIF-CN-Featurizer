from cifkit import Cif

from core.utils.bond_count import (
    compute_count_first_second_min_dist,
    extract_best_labels,
    extract_shortest_dist_with_tol,
    extract_avg_shortest_dist_with_tol,
    get_avg_second_by_first_shortest_dist_ratio,
)

from core.features.binary_env import (
    compute_homoatomic_dist_by_site_shortest_dist,
    compute_avg_homoatomic_dist_by_site_shortest_dist,
    get_A_and_B_count_in_best_label_per_element,
    get_avg_A_and_B_count_in_per_element,
)
from core.utils import element_parser
from core.utils import log


def compute_binary_env_features(cif: Cif):
    connections = cif.connections
    A, B = element_parser.get_binary_AB_elements(list(cif.unique_elements))
    (
        A_avg_homoatomic_dist_by_shortest_dist,
        B_avg_homoatomic_dist_by_shortest_dist,
    ) = compute_avg_homoatomic_dist_by_site_shortest_dist(connections, A, B)
    (
        A_count_at_A_shortest_dist,
        A_count_at_B_shortest_dist,
        B_count_at_A_shortest_dist,
        B_count_at_B_shortest_dist,
    ) = get_A_and_B_count_in_best_label_per_element(connections, A, B)
    (
        A_avg_count_at_A_shortest_dist,
        A_avg_count_at_B_shortest_dist,
        B_avg_count_at_A_shortest_dist,
        B_avg_count_at_B_shortest_dist,
    ) = get_avg_A_and_B_count_in_per_element(connections, A, B)

    # Compute the first, second shortest distances and count
    first_second_dist_per_label_data = compute_count_first_second_min_dist(connections)
    # Compute the best site for each label, determined by the shortest distance
    best_site_data = extract_best_labels(first_second_dist_per_label_data)

    # Tol result
    tol_results = extract_shortest_dist_with_tol(best_site_data, connections)
    A_shortest_dist_count_within_tol = tol_results[A]["shortest_dist_count_within_tol"]
    B_shortest_dist_count_within_tol = tol_results[B]["shortest_dist_count_within_tol"]

    avg_tol_results = extract_avg_shortest_dist_with_tol(connections)
    A_avg_shortest_dist_within_tol_count = avg_tol_results[A]["avg_shortest_dist_within_tol_count"]
    B_avg_shortest_dist_within_tol_count = avg_tol_results[B]["avg_shortest_dist_within_tol_count"]

    A_best_label = best_site_data[A]["best_label"]
    B_best_label = best_site_data[B]["best_label"]

    (
        A_homoatomic_dist_by_shortest_dist,
        B_homoatomic_dist_by_shortest_dist,
    ) = compute_homoatomic_dist_by_site_shortest_dist(connections, A_best_label, B_best_label)

    # First shortest distance
    A_shortest_dist = best_site_data[A]["details"]["shortest_dist"]
    B_shortest_dist = best_site_data[B]["details"]["shortest_dist"]

    # Second shortest distance
    A_second_shortest_dist = best_site_data[A]["details"]["second_shortest_dist"]
    B_second_shortest_dist = best_site_data[B]["details"]["second_shortest_dist"]

    # Shorest distance count from best site
    A_shortest_dist_count = best_site_data[A]["details"]["counts"][A_shortest_dist]
    B_shortest_dist_count = best_site_data[B]["details"]["counts"][B_shortest_dist]

    # Second shorest distance count from best site
    A_second_shortest_dist_count = best_site_data[A]["details"]["counts"][A_second_shortest_dist]
    B_second_shortest_dist_count = best_site_data[B]["details"]["counts"][B_second_shortest_dist]

    # Avg shortest distance count across site labels per element
    A_avg_shortest_dist_count = best_site_data[A]["avg_shortest_dist"]
    B_avg_shortest_dist_count = best_site_data[B]["avg_shortest_dist"]

    # Avg second shortest distance count across site labels per element
    A_avg_second_shortest_dist_count = best_site_data[A]["avg_second_shortest_dist_count"]
    B_avg_second_shortest_dist_count = best_site_data[B]["avg_second_shortest_dist_count"]

    # Get avg second by first shortest distance ratio across site labels per element
    avg_second_by_first_dist = get_avg_second_by_first_shortest_dist_ratio(
        first_second_dist_per_label_data, connections
    )
    A_avg_second_by_first_shortest_dist = avg_second_by_first_dist[A]["avg_second_by_first_shortest_dist"]
    B_avg_second_by_first_shortest_dist = avg_second_by_first_dist[B]["avg_second_by_first_shortest_dist"]

    data = {
        "ENV_A_shortest_dist_count": A_shortest_dist_count,
        "ENV_B_shortest_dist_count": B_shortest_dist_count,
        "ENV_A_avg_shortest_dist_count": A_avg_shortest_dist_count,
        "ENV_B_avg_shortest_dist_count": B_avg_shortest_dist_count,
        "ENV_A_shortest_tol_dist_count": A_shortest_dist_count_within_tol,
        "ENV_B_shortest_tol_dist_count": B_shortest_dist_count_within_tol,
        "ENV_A_avg_shortest_dist_within_tol_count": A_avg_shortest_dist_within_tol_count,
        "ENV_B_avg_shortest_dist_within_tol_count": B_avg_shortest_dist_within_tol_count,
        "ENV_A_second_by_first_shortest_dist": A_second_shortest_dist / A_shortest_dist,
        "ENV_B_second_by_first_shortest_dist": B_second_shortest_dist / B_shortest_dist,
        "ENV_A_avg_second_by_first_shortest_dist": A_avg_second_by_first_shortest_dist,
        "ENV_B_avg_second_by_first_shortest_dist": B_avg_second_by_first_shortest_dist,
        "ENV_A_second_shortest_dist_count": A_second_shortest_dist_count,
        "ENV_B_second_shortest_dist_count": B_second_shortest_dist_count,
        "ENV_A_avg_second_shortest_dist_count": A_avg_second_shortest_dist_count,
        "ENV_B_avg_second_shortest_dist_count": B_avg_second_shortest_dist_count,
        "ENV_A_homoatomic_dist_by_shortest_dist": A_homoatomic_dist_by_shortest_dist,
        "ENV_B_homoatomic_dist_by_shortest_dist": B_homoatomic_dist_by_shortest_dist,
        "ENV_A_avg_homoatomic_dist_by_shortest_dist": A_avg_homoatomic_dist_by_shortest_dist,
        "ENV_B_avg_homoatomic_dist_by_shortest_dist": B_avg_homoatomic_dist_by_shortest_dist,
        "ENV_A_count_at_A_shortest_dist": A_count_at_A_shortest_dist,
        "ENV_A_count_at_B_shortest_dist": A_count_at_B_shortest_dist,
        "ENV_A_avg_count_at_A_shortest_dist": A_avg_count_at_A_shortest_dist,
        "ENV_A_avg_count_at_B_shortest_dist": A_avg_count_at_B_shortest_dist,
        "ENV_B_count_at_A_shortest_dist": B_count_at_A_shortest_dist,
        "ENV_B_count_at_B_shortest_dist": B_count_at_B_shortest_dist,
        "ENV_B_avg_count_at_A_shortest_dist": B_avg_count_at_A_shortest_dist,
        "ENV_B_avg_count_at_B_shortest_dist": B_avg_count_at_B_shortest_dist,
    }
    # log.print_dict_pretty(data, "env binary")
    # log.print_connected_points(connections)
    return data
