from cifkit.utils import string_parser
from core.utils.bond_count import (
    get_site_labels_per_element,
    compute_count_first_second_min_dist,
    extract_best_labels,
)


def compute_homoatomic_dist_by_site_shortest_dist(connections, A_best_label, B_best_label):
    """
    Computes the shortest homoatomic distances normalized by the shortest distance
    encountered at the best site for each element.
    """
    A = string_parser.get_atom_type_from_label(A_best_label)
    B = string_parser.get_atom_type_from_label(B_best_label)

    A_homoatomic_shortest_dist = float("inf")
    B_homoatomic_shortest_dist = float("inf")
    A_min_dist = float("inf")
    B_min_dist = float("inf")

    # Process each site
    for site_label, site_connections in connections.items():
        # Compute the shortest distance at this site
        current_min_dist = min([dist for _, dist, _, _ in site_connections])

        # Update the minimum distances for A and B if this is their best site
        if site_label == A_best_label:
            A_min_dist = current_min_dist
            # Find the shortest homoatomic distance for A
            A_homoatomic_shortest_dist = min([dist for label, dist, _, _ in site_connections if label.startswith(A)])

        if site_label == B_best_label:
            B_min_dist = current_min_dist
            # Find the shortest homoatomic distance for B
            B_homoatomic_shortest_dist = min([dist for label, dist, _, _ in site_connections if label.startswith(B)])

    # Normalize the shortest distances by the shortest distances at the best sites
    A_homoatomic_dist_by_shortest_dist = A_homoatomic_shortest_dist / A_min_dist
    B_homoatomic_dist_by_shortest_dist = B_homoatomic_shortest_dist / B_min_dist

    return (
        A_homoatomic_dist_by_shortest_dist,
        B_homoatomic_dist_by_shortest_dist,
    )


def compute_avg_homoatomic_dist_by_site_shortest_dist(connections, A, B):
    """
    Computes the average of the homoatomic distances normalized by the
    shortest distance encountered at each site for two distinct element
    types within a given set of connections.
    """

    # Shortest distnace per site label
    element_to_site_labels = get_site_labels_per_element(connections)
    A_total_homoatomic_dist_by_shortest_dist = 0.0
    B_total_homoatomic_dist_by_shortest_dist = 0.0

    for site_label, site_connections in connections.items():
        min_dist_per_site = site_connections[0][1]
        for connection in site_connections:
            other_label, dist, _, _ = connection
            if site_label.startswith(A) and other_label.startswith(A):
                A_total_homoatomic_dist_by_shortest_dist += dist / min_dist_per_site
                break
            if site_label.startswith(B) and other_label.startswith(B):
                B_total_homoatomic_dist_by_shortest_dist += dist / min_dist_per_site
                break

    # Average of (A-A distance / shortest distance for each site label)
    # Average of (B-B distance / (shortest distance for each site label)

    A_avg_homoatomic_dist_by_shortest_dist = A_total_homoatomic_dist_by_shortest_dist / len(element_to_site_labels[A])
    B_avg_homoatomic_dist_by_shortest_dist = B_total_homoatomic_dist_by_shortest_dist / len(element_to_site_labels[B])
    return (
        A_avg_homoatomic_dist_by_shortest_dist,
        B_avg_homoatomic_dist_by_shortest_dist,
    )


def get_A_and_B_count_in_best_label_per_element(connections, A, B):
    """
    Compute the occurrences of element types A and B at the shortest distances
    within their respective best labeled site for each element. The best site
    label is determined with the label with the shortest distance pair.
    """
    A_count_at_A_shortest_dist = 0
    A_count_at_B_shortest_dist = 0
    B_count_at_A_shortest_dist = 0
    B_count_at_B_shortest_dist = 0

    dist_count_per_label = compute_count_first_second_min_dist(connections)
    best_label_dict = extract_best_labels(dist_count_per_label)

    best_A_site_label = best_label_dict[A]["best_label"]
    best_A_shortest_dist = best_label_dict[A]["details"]["shortest_dist"]
    best_B_site_label = best_label_dict[B]["best_label"]
    best_B_shortest_dist = best_label_dict[B]["details"]["shortest_dist"]

    for connection in connections[best_A_site_label]:
        other_label, dist, _, _ = connection
        if dist == best_A_shortest_dist:
            if other_label.startswith(A):
                A_count_at_A_shortest_dist += 1

            if other_label.startswith(B):
                B_count_at_A_shortest_dist += 1

    for connection in connections[best_B_site_label]:
        other_label, dist, _, _ = connection
        if dist == best_B_shortest_dist:
            if other_label.startswith(A):
                A_count_at_B_shortest_dist += 1

            if other_label.startswith(B):
                B_count_at_B_shortest_dist += 1

    return (
        A_count_at_A_shortest_dist,
        A_count_at_B_shortest_dist,
        B_count_at_A_shortest_dist,
        B_count_at_B_shortest_dist,
    )


def get_avg_A_and_B_count_in_per_element(connections, A, B):
    """
    Compute the occurrences of element types A and B at the shortest distances
    within their respective site for all site labels
    """
    A_total_count_at_A_shortest_dist = 0
    A_total_count_at_B_shortest_dist = 0
    B_total_count_at_A_shortest_dist = 0
    B_total_count_at_B_shortest_dist = 0

    dist_count_per_label = compute_count_first_second_min_dist(connections)
    # Use the best label dict to parse the number of site labels for A and B
    best_labels = extract_best_labels(dist_count_per_label)
    A_site_label_count = best_labels[A]["label_count"]
    B_site_label_count = best_labels[B]["label_count"]

    for site_label, connection_data in connections.items():
        # Get the shortest distance for the site label
        parsed_element = string_parser.get_atom_type_from_label(site_label)
        shortest_dist_per_site_label = dist_count_per_label[site_label]["shortest_dist"]

        # Loop through each connection
        for connection in connection_data:
            other_label, dist, _, _ = connection

            if parsed_element == A:
                if dist == shortest_dist_per_site_label:
                    if other_label.startswith(A):
                        A_total_count_at_A_shortest_dist += 1

                    if other_label.startswith(B):
                        B_total_count_at_A_shortest_dist += 1

            if parsed_element == B:
                if dist == shortest_dist_per_site_label:
                    if other_label.startswith(A):
                        A_total_count_at_B_shortest_dist += 1

                    if other_label.startswith(B):
                        B_total_count_at_B_shortest_dist += 1

    A_avg_count_at_A_shortest_dist = A_total_count_at_A_shortest_dist / A_site_label_count
    A_avg_count_at_B_shortest_dist = A_total_count_at_B_shortest_dist / B_site_label_count
    B_avg_count_at_A_shortest_dist = B_total_count_at_A_shortest_dist / A_site_label_count
    B_avg_count_at_B_shortest_dist = B_total_count_at_B_shortest_dist / B_site_label_count
    return (
        A_avg_count_at_A_shortest_dist,
        A_avg_count_at_B_shortest_dist,
        B_avg_count_at_A_shortest_dist,
        B_avg_count_at_B_shortest_dist,
    )
