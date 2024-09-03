from collections import defaultdict
import numpy as np
from cifkit.utils import string_parser


def compute_count_first_second_min_dist(
    all_labels_connections,
):
    """
    Determine the shortest and second shortest distances from
    each site label and their respective counts.
    """
    # Dictionary to hold the results
    first_second_dist_info = defaultdict(
        lambda: {
            "shortest_dist": None,
            "second_shortest_dist": None,
            "counts": {},
        }
    )

    # Collect all distances for each label
    for (
        label,
        connections,
    ) in all_labels_connections.items():
        distances = []
        for _, dist, _, _ in connections:
            distances.append(dist)

        if distances:
            # Sorting distances
            sorted_distances = sorted(distances)

            # Find unique distances and their counts using numpy
            unique_distances, counts = np.unique(sorted_distances, return_counts=True)

            # Populate the shortest_dist and second shortest_dist distances
            if len(unique_distances) > 0:
                first_second_dist_info[label]["shortest_dist"] = unique_distances[0]
                first_second_dist_info[label]["counts"][unique_distances[0]] = counts[0]
            if len(unique_distances) > 1:
                first_second_dist_info[label]["second_shortest_dist"] = unique_distances[1]
                first_second_dist_info[label]["counts"][unique_distances[1]] = counts[1]

    return dict(first_second_dist_info)


def extract_best_labels(data):
    """
    Extract the best label for each element based on the shortest distance,
    and if there's a tie, use the second shortest distance as a tiebreaker.
    """

    best_labels = {}
    label_counts = {}
    total_distances = {}

    # Initialize storage for distance statistics
    for label in data:
        element = string_parser.get_atom_type_from_label(
            label
        )  # Assuming label ends with a number like 'Rh1', 'Th1', etc.
        if element not in total_distances:
            total_distances[element] = {
                "shortest_counts": [],
                "second_shortest_counts": [],
            }

    # Collect data for each label
    for label, details in data.items():
        element = string_parser.get_atom_type_from_label(label)

        # Update label counts
        label_counts[element] = label_counts.get(element, 0) + 1

        # Update total distance counts
        total_distances[element]["shortest_counts"].append(details["counts"][details["shortest_dist"]])
        if "second_shortest_dist" in details:
            total_distances[element]["second_shortest_counts"].append(
                details["counts"].get(details["second_shortest_dist"], 0)
            )

        # Determine best label
        if element not in best_labels:
            best_labels[element] = (label, details)
        else:
            current_best = best_labels[element][1]
            if (details["shortest_dist"] < current_best["shortest_dist"]) or (
                details["shortest_dist"] == current_best["shortest_dist"]
                and details["second_shortest_dist"] < current_best["second_shortest_dist"]
            ):
                best_labels[element] = (label, details)

    # Prepare final output
    output = {}
    for element, (label, details) in best_labels.items():
        total_shortest = sum(total_distances[element]["shortest_counts"])
        total_second_shortest = sum(total_distances[element]["second_shortest_counts"])
        avg_shortest = total_shortest / label_counts[element]
        avg_second_shortest = (
            total_second_shortest / label_counts[element] if total_distances[element]["second_shortest_counts"] else 0
        )

        output[element] = {
            "label_count": label_counts[element],
            "shortest_dist_total_count": total_shortest,
            "second_shortest_dist_count": total_second_shortest,
            "avg_shortest_dist": avg_shortest,
            "avg_second_shortest_dist_count": avg_second_shortest,
            "best_label": label,
            "details": details,
        }

    return output


def extract_shortest_dist_with_tol(best_label_dist_info, connections, tol=0.05):
    """
    Compute the count of distances within a specified tolerance
    of the shortest distance of each site label
    """
    best_site_result = {}

    # Find the shortest distance form the best site label
    for element, info in best_label_dist_info.items():
        best_site_shortest_dist_count_within_tol = 0
        best_site_min_dist = best_label_dist_info[element]["details"]["shortest_dist"]
        best_site_label = best_label_dist_info[element]["best_label"]
        best_site_min_dist_with_tol = best_site_min_dist * (1 + tol)

        for connection in connections[best_site_label]:
            _, dist, _, _ = connection
            if dist <= best_site_min_dist_with_tol:
                best_site_shortest_dist_count_within_tol += 1

        best_site_result[element] = {
            "shortest_dist_count_within_tol": best_site_shortest_dist_count_within_tol,
        }
    return best_site_result


def extract_avg_shortest_dist_with_tol(connection_data, tol=0.05):
    """
    Compute the count of distances within a specified tolerance
    of the shortest distance of each site label
    """

    # Now, find the average
    site_result = defaultdict(lambda: {"shortest_dist_count_within_tol": 0})

    for site_label, connections in connection_data.items():
        site_result[site_label] = {}
        count_within_tol = 0
        min_dist_per_site_label = connections[0][1]
        site_min_dist_with_tol = min_dist_per_site_label * (1 + tol)

        for connection in connections:
            dist = connection[1]
            if dist <= site_min_dist_with_tol:
                count_within_tol += 1

        site_result[site_label] = {"shortest_dist_count_within_tol": count_within_tol}

    # Step 2: Aggregate counts by element and compute averages
    avg_result = defaultdict(lambda: {"total_shortest_dist_within_tol_count": 0})

    element_to_site_labels = get_site_labels_per_element(connection_data)

    for site_label, result in site_result.items():
        element = string_parser.get_atom_type_from_label(site_label)

        if site_label in element_to_site_labels[element]:
            avg_result[element]["total_shortest_dist_within_tol_count"] += result["shortest_dist_count_within_tol"]

    for element, result in avg_result.items():
        num_sites = len(element_to_site_labels[element])
        if num_sites > 0:
            result["avg_shortest_dist_within_tol_count"] = result["total_shortest_dist_within_tol_count"] / num_sites
        else:
            result["avg_shortest_dist_within_tol_count"] = 0.0
    return avg_result


def get_avg_second_by_first_shortest_dist_ratio(site_dist_info, connection_data):
    """
    Compute the ratio of the second shortest distance to the shortest distance
    for each site label
    """
    ratio_total_result = defaultdict(lambda: {"total_second_by_first_shortest_dist": 0.0})

    for site_label, data in site_dist_info.items():
        element = string_parser.get_atom_type_from_label(site_label)

        ratio = data["second_shortest_dist"] / data["shortest_dist"]
        ratio_total_result[element]["total_second_by_first_shortest_dist"] += ratio

    element_to_site_labels = get_site_labels_per_element(connection_data)
    ratio_avg_result = {}

    for element, result in ratio_total_result.items():
        num_sites = len(element_to_site_labels[element])
        if num_sites > 0:
            avg_ratio = result["total_second_by_first_shortest_dist"] / num_sites
        else:
            avg_ratio = 0.0

        ratio_avg_result[element] = {"avg_second_by_first_shortest_dist": avg_ratio}

    return ratio_avg_result


def get_site_labels_per_element(connection_data):
    element_to_site_labels = {}
    for site_label, connection in connection_data.items():
        element_label = string_parser.get_atom_type_from_label(site_label)
        if element_label not in element_to_site_labels:
            element_to_site_labels[element_label] = []
        element_to_site_labels[element_label].append(site_label)
    return element_to_site_labels
