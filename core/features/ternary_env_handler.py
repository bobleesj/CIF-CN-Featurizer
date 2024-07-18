from core.utils.bond_count import (
    compute_count_first_second_min_dist,
    extract_best_labels,
    extract_shortest_dist_with_tol,
    extract_avg_shortest_dist_with_tol,
    get_avg_second_by_first_shortest_dist_ratio,
)
from core.utils.element_parser import get_ternary_RMX_elements
from core.features.ternary_env import (
    compute_homoatomic_dist_by_site_shortest_dist,
    compute_avg_homoatomic_dist_by_site_shortest_dist,
    get_R_and_M_and_X_count_in_best_label_per_element,
    get_avg_R_and_M_and_X_count_in_per_element,
)

from cifkit import Cif


def compute_ternary_env_features(cif: Cif):
    connections = cif.connections
    R, M, X = get_ternary_RMX_elements(list(cif.unique_elements))

    (
        R_avg_homoatomic_dist_by_shortest_dist,
        M_avg_homoatomic_dist_by_shortest_dist,
        X_avg_homoatomic_dist_by_shortest_dist,
    ) = compute_avg_homoatomic_dist_by_site_shortest_dist(connections, R, M, X)
    (
        R_count_at_R_shortest_dist,
        R_count_at_M_shortest_dist,
        R_count_at_X_shortest_dist,
        M_count_at_R_shortest_dist,
        M_count_at_M_shortest_dist,
        M_count_at_X_shortest_dist,
        X_count_at_R_shortest_dist,
        X_count_at_M_shortest_dist,
        X_count_at_X_shortest_dist,
    ) = get_R_and_M_and_X_count_in_best_label_per_element(connections, R, M, X)

    (
        R_avg_count_at_R_shorest_dist,
        R_avg_count_at_M_shorest_dist,
        R_avg_count_at_X_shorest_dist,
        M_avg_count_at_R_shorest_dist,
        M_avg_count_at_M_shorest_dist,
        M_avg_count_at_X_shorest_dist,
        X_avg_count_at_R_shorest_dist,
        X_avg_count_at_M_shorest_dist,
        X_avg_count_at_X_shorest_dist,
    ) = get_avg_R_and_M_and_X_count_in_per_element(connections, R, M, X)

    # Compute the first, second shortest distances and count
    first_second_dist_per_label_data = compute_count_first_second_min_dist(connections)
    # Compute the best site for each label, determined by the shortest distance
    best_site_data = extract_best_labels(first_second_dist_per_label_data)

    # Tol result
    tol_results = extract_shortest_dist_with_tol(best_site_data, connections)
    R_shortest_dist_count_within_tol = tol_results[R]["shortest_dist_count_within_tol"]
    M_shortest_dist_count_within_tol = tol_results[M]["shortest_dist_count_within_tol"]
    X_shortest_dist_count_within_tol = tol_results[X]["shortest_dist_count_within_tol"]

    avg_tol_results = extract_avg_shortest_dist_with_tol(connections)
    R_avg_shortest_dist_within_tol_count = avg_tol_results[R]["avg_shortest_dist_within_tol_count"]
    M_avg_shortest_dist_within_tol_count = avg_tol_results[M]["avg_shortest_dist_within_tol_count"]
    X_avg_shortest_dist_within_tol_count = avg_tol_results[X]["avg_shortest_dist_within_tol_count"]

    R_best_label = best_site_data[R]["best_label"]
    M_best_label = best_site_data[M]["best_label"]
    X_best_label = best_site_data[X]["best_label"]

    (
        R_homoatomic_dist_by_shortest_dist,
        M_homoatomic_dist_by_shortest_dist,
        X_homoatomic_dist_by_shortest_dist,
    ) = compute_homoatomic_dist_by_site_shortest_dist(connections, R_best_label, M_best_label, X_best_label)

    # First shortest distance
    R_shortest_dist = best_site_data[R]["details"]["shortest_dist"]
    M_shortest_dist = best_site_data[M]["details"]["shortest_dist"]
    X_shortest_dist = best_site_data[X]["details"]["shortest_dist"]

    # Second shortest distance
    R_second_shortest_dist = best_site_data[R]["details"]["second_shortest_dist"]
    M_second_shortest_dist = best_site_data[M]["details"]["second_shortest_dist"]
    X_second_shortest_dist = best_site_data[X]["details"]["second_shortest_dist"]

    # First shortest distance count
    R_shortest_dist_count = best_site_data[R]["details"]["counts"][R_shortest_dist]
    M_shortest_dist_count = best_site_data[M]["details"]["counts"][M_shortest_dist]
    X_shortest_dist_count = best_site_data[X]["details"]["counts"][X_shortest_dist]

    # Second shorest distance count
    R_second_shortest_dist_count = best_site_data[R]["details"]["counts"][R_second_shortest_dist]
    M_second_shortest_dist_count = best_site_data[M]["details"]["counts"][M_second_shortest_dist]
    X_second_shortest_dist_count = best_site_data[X]["details"]["counts"][X_second_shortest_dist]

    # Avg shortest distance count across site labels per element
    R_avg_shortest_dist_count = best_site_data[R]["avg_shortest_dist"]
    M_avg_shortest_dist_count = best_site_data[M]["avg_shortest_dist"]
    X_avg_shortest_dist_count = best_site_data[X]["avg_shortest_dist"]

    # Avg second shortest distance count across site labels per element
    R_avg_second_shortest_dist_count = best_site_data[R]["avg_second_shortest_dist_count"]
    M_avg_second_shortest_dist_count = best_site_data[M]["avg_second_shortest_dist_count"]
    X_avg_second_shortest_dist_count = best_site_data[M]["avg_second_shortest_dist_count"]

    # Get avg second by first shortest distance ratio across site labels per element
    avg_second_by_first_dist = get_avg_second_by_first_shortest_dist_ratio(
        first_second_dist_per_label_data, connections
    )
    R_avg_second_by_first_shortest_dist = avg_second_by_first_dist[R]["avg_second_by_first_shortest_dist"]
    M_avg_second_by_first_shortest_dist = avg_second_by_first_dist[M]["avg_second_by_first_shortest_dist"]
    X_avg_second_by_first_shortest_dist = avg_second_by_first_dist[X]["avg_second_by_first_shortest_dist"]

    results = {
        "ENV_R_shortest_dist_count": R_shortest_dist_count,
        "ENV_M_shortest_dist_count": M_shortest_dist_count,
        "ENV_X_shortest_dist_count": X_shortest_dist_count,
        "ENV_R_avg_shortest_dist_count": R_avg_shortest_dist_count,
        "ENV_M_avg_shortest_dist_count": M_avg_shortest_dist_count,
        "ENV_X_avg_shortest_dist_count": X_avg_shortest_dist_count,
        "ENV_R_shortest_tol_dist_count": R_shortest_dist_count_within_tol,
        "ENV_M_shortest_tol_dist_count": M_shortest_dist_count_within_tol,
        "ENV_X_shortest_tol_dist_count": X_shortest_dist_count_within_tol,
        "ENV_R_avg_shortest_dist_within_tol_count": R_avg_shortest_dist_within_tol_count,
        "ENV_M_avg_shortest_dist_within_tol_count": M_avg_shortest_dist_within_tol_count,
        "ENV_X_avg_shortest_dist_within_tol_count": X_avg_shortest_dist_within_tol_count,
        "ENV_R_second_by_first_shortest_dist": R_second_shortest_dist / R_shortest_dist,
        "ENV_M_second_by_first_shortest_dist": M_second_shortest_dist / M_shortest_dist,
        "ENV_X_second_by_first_shortest_dist": X_second_shortest_dist / X_shortest_dist,
        "ENV_R_avg_second_by_first_shortest_dist": R_avg_second_by_first_shortest_dist,
        "ENV_M_avg_second_by_first_shortest_dist": M_avg_second_by_first_shortest_dist,
        "ENV_X_avg_second_by_first_shortest_dist": X_avg_second_by_first_shortest_dist,
        "ENV_R_second_shortest_dist_count": R_second_shortest_dist_count,
        "ENV_M_second_shortest_dist_count": M_second_shortest_dist_count,
        "ENV_X_second_shortest_dist_count": X_second_shortest_dist_count,
        "ENV_R_avg_second_shortest_dist_count": R_avg_second_shortest_dist_count,
        "ENV_M_avg_second_shortest_dist_count": M_avg_second_shortest_dist_count,
        "ENV_X_avg_second_shortest_dist_count": X_avg_second_shortest_dist_count,
        "ENV_R_homoatomic_dist_by_shortest_dist": R_homoatomic_dist_by_shortest_dist,
        "ENV_M_homoatomic_dist_by_shortest_dist": M_homoatomic_dist_by_shortest_dist,
        "ENV_X_homoatomic_dist_by_shortest_dist": X_homoatomic_dist_by_shortest_dist,
        "ENV_R_avg_homoatomic_dist_by_shortest_dist": R_avg_homoatomic_dist_by_shortest_dist,
        "ENV_M_avg_homoatomic_dist_by_shortest_dist": M_avg_homoatomic_dist_by_shortest_dist,
        "ENV_X_avg_homoatomic_dist_by_shortest_dist": X_avg_homoatomic_dist_by_shortest_dist,
        "ENV_R_count_at_R_shortest_dist": R_count_at_R_shortest_dist,
        "ENV_M_count_at_R_shortest_dist": M_count_at_R_shortest_dist,
        "ENV_X_count_at_R_shortest_dist": X_count_at_R_shortest_dist,
        "ENV_R_avg_count_at_R_shortest_dist": R_avg_count_at_R_shorest_dist,
        "ENV_M_avg_count_at_R_shortest_dist": M_avg_count_at_R_shorest_dist,
        "ENV_X_avg_count_at_R_shortest_dist": X_avg_count_at_R_shorest_dist,
        "ENV_R_count_at_M_shortest_dist": R_count_at_M_shortest_dist,
        "ENV_M_count_at_M_shortest_dist": M_count_at_M_shortest_dist,
        "ENV_X_count_at_M_shortest_dist": X_count_at_M_shortest_dist,
        "ENV_R_avg_count_at_M_shortest_dist": R_avg_count_at_M_shorest_dist,
        "ENV_M_avg_count_at_M_shortest_dist": M_avg_count_at_M_shorest_dist,
        "ENV_X_avg_count_at_M_shortest_dist": X_avg_count_at_M_shorest_dist,
        "ENV_R_count_at_X_shortest_dist": R_count_at_X_shortest_dist,
        "ENV_M_count_at_X_shortest_dist": M_count_at_X_shortest_dist,
        "ENV_X_count_at_X_shortest_dist": X_count_at_X_shortest_dist,
        "ENV_R_avg_count_at_X_shortest_dist": R_avg_count_at_X_shorest_dist,
        "ENV_M_avg_count_at_X_shortest_dist": M_avg_count_at_X_shorest_dist,
        "ENV_X_avg_count_at_X_shortest_dist": X_avg_count_at_X_shorest_dist,
    }
    return results
