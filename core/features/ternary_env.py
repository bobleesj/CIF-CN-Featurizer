from cifkit.utils import string_parser
from core.utils.bond_count import (
    get_site_labels_per_element,
    compute_count_first_second_min_dist,
    extract_best_labels,
)


def compute_homoatomic_dist_by_site_shortest_dist(connections, R_best_label, M_best_label, X_best_label):
    """
    Computes the shortest homoatomic distances normalized by the shortest distance
    encountered at the best site for each element.
    """
    R = string_parser.get_atom_type_from_label(R_best_label)
    M = string_parser.get_atom_type_from_label(M_best_label)
    X = string_parser.get_atom_type_from_label(X_best_label)

    R_homoatomic_shortest_dist = float("inf")
    M_homoatomic_shortest_dist = float("inf")
    X_homoatomic_shortest_dist = float("inf")
    R_min_dist = float("inf")
    M_min_dist = float("inf")
    X_min_dist = float("inf")

    # Process each site
    for site_label, site_connections in connections.items():
        # Compute the shortest distance at this site
        current_min_dist = min([dist for _, dist, _, _ in site_connections])

        # Update the minimum distances for A and B if this is their best site
        if site_label == R_best_label:
            R_min_dist = current_min_dist
            # Find the shortest homoatomic distance for A
            R_homoatomic_shortest_dist = min([dist for label, dist, _, _ in site_connections if label.startswith(R)])

        if site_label == M_best_label:
            M_min_dist = current_min_dist
            # Find the shortest homoatomic distance for A
            M_homoatomic_shortest_dist = min([dist for label, dist, _, _ in site_connections if label.startswith(M)])

        if site_label == X_best_label:
            X_min_dist = current_min_dist
            # Find the shortest homoatomic distance for B
            X_homoatomic_shortest_dist = min([dist for label, dist, _, _ in site_connections if label.startswith(X)])

    # Normalize the shortest distances by the shortest distances at the best sites
    R_homoatomic_dist_by_shortest_dist = R_homoatomic_shortest_dist / R_min_dist
    M_homoatomic_dist_by_shortest_dist = M_homoatomic_shortest_dist / M_min_dist
    X_homoatomic_dist_by_shortest_dist = X_homoatomic_shortest_dist / X_min_dist

    return (
        R_homoatomic_dist_by_shortest_dist,
        M_homoatomic_dist_by_shortest_dist,
        X_homoatomic_dist_by_shortest_dist,
    )


def compute_avg_homoatomic_dist_by_site_shortest_dist(connections, R, M, X):
    """
    Computes the average of the homoatomic distances normalized by the
    shortest distance encountered at each site for two distinct element
    types within a given set of connections.
    """

    # Shortest distnace per site label
    element_to_site_labels = get_site_labels_per_element(connections)
    R_total_homoatomic_dist_by_shortest_dist = 0.0
    M_total_homoatomic_dist_by_shortest_dist = 0.0
    X_total_homoatomic_dist_by_shortest_dist = 0.0

    for site_label, site_connections in connections.items():
        min_dist_per_site = site_connections[0][1]
        for connection in site_connections:
            other_label, dist, _, _ = connection
            if site_label.startswith(R) and other_label.startswith(R):
                R_total_homoatomic_dist_by_shortest_dist += dist / min_dist_per_site
                break
            if site_label.startswith(M) and other_label.startswith(M):
                M_total_homoatomic_dist_by_shortest_dist += dist / min_dist_per_site
                break
            if site_label.startswith(X) and other_label.startswith(X):
                X_total_homoatomic_dist_by_shortest_dist += dist / min_dist_per_site
                break

    # Average of (A-A distance / shortest distance for each site label)
    # Average of (B-B distance / (shortest distance for each site label)

    R_avg_homoatomic_dist_by_shortest_dist = R_total_homoatomic_dist_by_shortest_dist / len(element_to_site_labels[R])
    M_avg_homoatomic_dist_by_shortest_dist = M_total_homoatomic_dist_by_shortest_dist / len(element_to_site_labels[M])
    X_avg_homoatomic_dist_by_shortest_dist = X_total_homoatomic_dist_by_shortest_dist / len(element_to_site_labels[X])
    return (
        R_avg_homoatomic_dist_by_shortest_dist,
        M_avg_homoatomic_dist_by_shortest_dist,
        X_avg_homoatomic_dist_by_shortest_dist,
    )


def get_R_and_M_and_X_count_in_best_label_per_element(connections, R, M, X):
    """
    Compute the occurrences of element types A and B at the shortest distances
    within their respective best labeled site for each element. The best site
    label is determined with the label with the shortest distance pair.
    """
    R_count_at_R_shortest_dist = 0
    R_count_at_M_shortest_dist = 0
    R_count_at_X_shortest_dist = 0

    M_count_at_R_shortest_dist = 0
    M_count_at_M_shortest_dist = 0
    M_count_at_X_shortest_dist = 0

    X_count_at_R_shortest_dist = 0
    X_count_at_M_shortest_dist = 0
    X_count_at_X_shortest_dist = 0

    dist_count_per_label = compute_count_first_second_min_dist(connections)
    best_label_dict = extract_best_labels(dist_count_per_label)

    best_R_site_label = best_label_dict[R]["best_label"]
    best_R_shortest_dist = best_label_dict[R]["details"]["shortest_dist"]
    best_M_site_label = best_label_dict[M]["best_label"]
    best_M_shortest_dist = best_label_dict[M]["details"]["shortest_dist"]
    best_X_site_label = best_label_dict[X]["best_label"]
    best_X_shortest_dist = best_label_dict[X]["details"]["shortest_dist"]

    for connection in connections[best_R_site_label]:
        other_label, dist, _, _ = connection
        if dist == best_R_shortest_dist:
            if other_label.startswith(R):
                R_count_at_R_shortest_dist += 1

            if other_label.startswith(M):
                M_count_at_R_shortest_dist += 1

            if other_label.startswith(X):
                X_count_at_R_shortest_dist += 1

    for connection in connections[best_M_site_label]:
        other_label, dist, _, _ = connection
        if dist == best_M_shortest_dist:
            if other_label.startswith(R):
                R_count_at_M_shortest_dist += 1

            if other_label.startswith(M):
                M_count_at_M_shortest_dist += 1

            if other_label.startswith(X):
                X_count_at_M_shortest_dist += 1

    for connection in connections[best_X_site_label]:
        other_label, dist, _, _ = connection
        if dist == best_X_shortest_dist:
            if other_label.startswith(R):
                R_count_at_X_shortest_dist += 1

            if other_label.startswith(M):
                M_count_at_X_shortest_dist += 1

            if other_label.startswith(X):
                X_count_at_X_shortest_dist += 1

    return (
        R_count_at_R_shortest_dist,
        R_count_at_M_shortest_dist,
        R_count_at_X_shortest_dist,
        M_count_at_R_shortest_dist,
        M_count_at_M_shortest_dist,
        M_count_at_X_shortest_dist,
        X_count_at_R_shortest_dist,
        X_count_at_M_shortest_dist,
        X_count_at_X_shortest_dist,
    )


def get_avg_R_and_M_and_X_count_in_per_element(connections, R, M, X):
    """
    Compute the occurrences of element types R, M, and X at the shortest distances
    within their respective site for all site labels
    """
    R_total_count_at_R_shortest_dist = 0
    R_total_count_at_M_shortest_dist = 0
    R_total_count_at_X_shortest_dist = 0
    M_total_count_at_R_shortest_dist = 0
    M_total_count_at_M_shortest_dist = 0
    M_total_count_at_X_shortest_dist = 0
    X_total_count_at_R_shortest_dist = 0
    X_total_count_at_M_shortest_dist = 0
    X_total_count_at_X_shortest_dist = 0

    dist_count_per_label = compute_count_first_second_min_dist(connections)
    # Use the best label dict to parse the number of site labels for R, M, and X
    best_labels = extract_best_labels(dist_count_per_label)
    R_site_label_count = best_labels[R]["label_count"]
    M_site_label_count = best_labels[M]["label_count"]
    X_site_label_count = best_labels[X]["label_count"]

    for site_label, connection_data in connections.items():
        parsed_element = string_parser.get_atom_type_from_label(site_label)
        shortest_dist_per_site_label = dist_count_per_label[site_label]["shortest_dist"]

        for connection in connection_data:
            other_label, dist, _, _ = connection

            if parsed_element == R and dist == shortest_dist_per_site_label:
                if other_label.startswith(R):
                    R_total_count_at_R_shortest_dist += 1
                elif other_label.startswith(M):
                    R_total_count_at_M_shortest_dist += 1
                elif other_label.startswith(X):
                    R_total_count_at_X_shortest_dist += 1

            elif parsed_element == M and dist == shortest_dist_per_site_label:
                if other_label.startswith(R):
                    M_total_count_at_R_shortest_dist += 1
                elif other_label.startswith(M):
                    M_total_count_at_M_shortest_dist += 1
                elif other_label.startswith(X):
                    M_total_count_at_X_shortest_dist += 1

            elif parsed_element == X and dist == shortest_dist_per_site_label:
                if other_label.startswith(R):
                    X_total_count_at_R_shortest_dist += 1
                elif other_label.startswith(M):
                    X_total_count_at_M_shortest_dist += 1
                elif other_label.startswith(X):
                    X_total_count_at_X_shortest_dist += 1

    # Calculating average counts
    R_avg_count_at_R = R_total_count_at_R_shortest_dist / R_site_label_count
    R_avg_count_at_M = R_total_count_at_M_shortest_dist / M_site_label_count
    R_avg_count_at_X = R_total_count_at_X_shortest_dist / X_site_label_count
    M_avg_count_at_R = M_total_count_at_R_shortest_dist / R_site_label_count
    M_avg_count_at_M = M_total_count_at_M_shortest_dist / M_site_label_count
    M_avg_count_at_X = M_total_count_at_X_shortest_dist / X_site_label_count
    X_avg_count_at_R = X_total_count_at_R_shortest_dist / R_site_label_count
    X_avg_count_at_M = X_total_count_at_M_shortest_dist / M_site_label_count
    X_avg_count_at_X = X_total_count_at_X_shortest_dist / X_site_label_count

    return (
        R_avg_count_at_R,
        R_avg_count_at_M,
        R_avg_count_at_X,
        M_avg_count_at_R,
        M_avg_count_at_M,
        M_avg_count_at_X,
        X_avg_count_at_R,
        X_avg_count_at_M,
        X_avg_count_at_X,
    )
