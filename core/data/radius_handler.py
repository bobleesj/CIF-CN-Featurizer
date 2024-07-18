import numpy as np
from core.data.radius import get_radius_data
from cifkit.data.radius_optimization import get_refined_CIF_radius


def get_is_radius_data_available(elements: list[str]) -> bool:
    """
    Check if both CIF and Pauling radius data are available
    for each element in the list.
    """
    data = get_radius_data()
    for element in elements:
        element_data = data.get(element, {})
        if not ("CIF_radius" in element_data and "Pauling_radius_CN12" in element_data):
            return False
    return True


def get_CIF_pauling_radius(elements: list[str]) -> dict:
    """
    Return CIF and Pualing data for a list of elements
    """
    data = get_radius_data()
    radii = {}
    for atom in elements:
        radii[atom] = {
            "CIF_radius": data[atom]["CIF_radius"],
            "Pauling_radius_CN12": data[atom]["Pauling_radius_CN12"],
        }

    return radii


def get_radius_values_per_element(elements, shortest_bond_distances) -> dict:
    """
    Merge CIF and Pauling radius data with CIF refined radius data.
    """
    is_radius_data_available = get_is_radius_data_available(elements)

    if not is_radius_data_available:
        return None

    CIF_pauling_rad = get_CIF_pauling_radius(elements)
    CIF_refined_rad = get_refined_CIF_radius(elements, shortest_bond_distances)

    combined_radii = {}
    for element in elements:
        combined_radii[element] = {
            "CIF_radius": CIF_pauling_rad[element]["CIF_radius"],
            "CIF_radius_refined": float(np.round(CIF_refined_rad.get(element), 3)),
            "Pauling_radius_CN12": CIF_pauling_rad[element]["Pauling_radius_CN12"],
        }

    return combined_radii


def compute_radius_sum(radius_values, is_radius_data_available: bool):
    """
    Compute the sum of two radii.
    """

    if not is_radius_data_available:
        return None

    elements = sorted(radius_values.keys())
    pair_distances: dict[str : dict[str, float]] = {
        "CIF_radius_sum": {},
        "CIF_radius_refined_sum": {},
        "Pauling_radius_sum": {},
    }

    # Calculate pair sums for each unique combination of elements
    for i, elem_i in enumerate(elements):
        for j in range(i, len(elements)):
            elem_j = elements[j]

            # Element pair label, e.g., A-B or A-A
            pair_label = f"{elem_i}-{elem_j}" if i != j else f"{elem_i}-{elem_i}"

            # Sum radii for each radius type
            pair_distances["CIF_radius_sum"][pair_label] = round(
                radius_values[elem_i]["CIF_radius"] + radius_values[elem_j]["CIF_radius"],
                3,
            )
            pair_distances["CIF_radius_refined_sum"][pair_label] = round(
                radius_values[elem_i]["CIF_radius_refined"] + radius_values[elem_j]["CIF_radius_refined"],
                3,
            )
            pair_distances["Pauling_radius_sum"][pair_label] = round(
                radius_values[elem_i]["Pauling_radius_CN12"] + radius_values[elem_j]["Pauling_radius_CN12"],
                3,
            )

    return pair_distances
