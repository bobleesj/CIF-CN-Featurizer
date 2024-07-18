from scipy.spatial import ConvexHull
from cifkit.utils import string_parser
from cifkit import Cif
from cifkit.coordination.geometry import compute_polyhedron_metrics

# For each file, get all polyhedrons


def get_CN_metrices_per_method(cif: Cif):
    """
    Find the best polyhedron for each label based on the minimum
    distance between the reference atom to the average position of
    connected atoms.
    """
    max_gaps_per_label = cif.CN_max_gap_per_site
    connections = cif.connections
    site_data = {}

    for label, CN_data_per_method in max_gaps_per_label.items():
        site_data[label] = {}

        for method, CN_data in CN_data_per_method.items():
            connection_data = connections[label][: CN_data["CN"]]
            polyhedron_points = []

            # Only if there are 4 or more points in the polyhedron
            if len(connection_data) > 3:
                for connection in connection_data:
                    polyhedron_points.append(connection[3])
            else:
                continue

            # Add the central atom as the last element
            polyhedron_points.append(connection_data[0][2])

            # Try to make a polyhedron
            try:
                hull = ConvexHull(polyhedron_points)

            except Exception:
                print(f"Error in determining polyhedron for {label} using {method} - skipped")
                site_data[label][method] = None
                continue  # Move to the next method

            # Returns non if ther eis any error
            polyhedron_metrics = compute_polyhedron_metrics(polyhedron_points, hull)
            site_data[label][method] = polyhedron_metrics

    return site_data


def compute_number_of_atoms_in_binary_CN(label_connections, CN_metrices, A, B):
    """
    Compute the number of atoms in the CN metrices.
    """
    CN_atom_count_data = {}
    for site_label, method_data in CN_metrices.items():
        CN_atom_count_data[site_label] = {}
        for method, data in method_data.items():
            # Get the number of CN per method
            CN = data["number_of_vertices"]
            CN_connections = label_connections[site_label][:CN]

            A_element_count = 0
            B_element_count = 0

            for connection in CN_connections:
                connected_label = connection[0]

                parsed_label = string_parser.get_atom_type_from_label(connected_label)
                if parsed_label == A:
                    A_element_count += 1
                elif parsed_label == B:
                    B_element_count += 1

            CN_atom_count_data[site_label][method] = {
                "A_count": A_element_count,
                "B_count": B_element_count,
            }
    return CN_atom_count_data


def compute_number_of_atoms_in_ternary_CN(label_connections, CN_metrices, R, M, X):
    """
    Compute the number of atoms in the CN metrices.
    """
    CN_atom_count_data = {}
    for site_label, method_data in CN_metrices.items():
        CN_atom_count_data[site_label] = {}
        for method, data in method_data.items():
            # Get the number of CN per method
            CN = data["number_of_vertices"]
            CN_connections = label_connections[site_label][:CN]

            R_element_count = 0
            M_element_count = 0
            X_element_count = 0

            for connection in CN_connections:
                connected_label = connection[0]

                parsed_label = string_parser.get_atom_type_from_label(connected_label)
                if parsed_label == R:
                    R_element_count += 1
                elif parsed_label == M:
                    M_element_count += 1
                elif parsed_label == X:
                    X_element_count += 1

            CN_atom_count_data[site_label][method] = {
                "R_count": R_element_count,
                "M_count": M_element_count,
                "X_count": X_element_count,
            }
    return CN_atom_count_data


def compute_min_max_avg_per_label(site_data):
    """
    Calculate the minimum, maximum, and average values for each metric across
    different calculation methods, grouped by each element label (e.g., Sb1, Th1).
    """
    result = {}
    # Iterate over each element (like Sb1, Th1, etc.)
    for label in site_data:
        metrics = {}
        # Iterate over each method under the element
        for method in site_data[label]:
            # Collect data for each metric within the method
            for key in site_data[label][method]:
                if key not in metrics:
                    metrics[key] = []
                metrics[key].append(site_data[label][method][key])

        # Calculate min, max, and avg for each metric within the site label
        result[label] = {}
        for key in metrics:
            result[label][key] = {
                "min": min(metrics[key]),
                "max": max(metrics[key]),
                "avg": sum(metrics[key]) / len(metrics[key]),
            }

    return result


def compute_global_averages_for_min_max_avg_metrices(min_max_avg_result):
    """
    Calculate global averages of all minimums, maximums, and averages across all labels
    from a pre-computed min-max-avg result.
    """
    # Initialize dictionaries to store cumulative sums of min, max, and avg
    global_sums = {"min": {}, "max": {}, "avg": {}}
    # Initialize counts to average the sums
    global_counts = {"min": {}, "max": {}, "avg": {}}
    # Summing values across all labels
    for label_data in min_max_avg_result.values():
        for metric, values in label_data.items():
            for stat in ["min", "max", "avg"]:
                if metric not in global_sums[stat]:
                    global_sums[stat][metric] = 0
                    global_counts[stat][metric] = 0
                global_sums[stat][metric] += values[stat]
                global_counts[stat][metric] += 1

    # Calculating global averages
    global_avg = {"min": {}, "max": {}, "avg": {}}
    for stat in ["min", "max", "avg"]:
        for metric, sum_value in global_sums[stat].items():
            global_avg[stat][metric] = sum_value / global_counts[stat][metric]

    return global_avg
