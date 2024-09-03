from core.utils import environment_parser
from core.utils import element_parser
from cifkit import Cif


def compute_binary_wyc_features(cif: Cif):
    elements = list(cif.unique_elements)
    A, B = element_parser.get_binary_AB_elements(elements)
    A_env, B_env = environment_parser.get_binary_atomic_environment_info(cif._loop_values, A, B)

    A_sites_total = A_env["sites"]
    A_multiplicity_total = A_env["multiplicity"]
    A_lowest_wyckoff_multiplicity = A_env["lowest_wyckoff_multiplicity"]

    B_sites_total = B_env["sites"]
    B_multiplicity_total = B_env["multiplicity"]
    B_lowest_wyckoff_multiplicity = B_env["lowest_wyckoff_multiplicity"]

    # Create a list to store the elements with the lowest Wyckoff label
    lowest_wyckoff_elements = []

    # Determine the lowest Wyckoff label between A and B
    min_wyckoff_multiplicity = min(
        A_lowest_wyckoff_multiplicity,
        B_lowest_wyckoff_multiplicity,
    )

    # If A or B have the lowest Wyckoff label, add them to the list
    if A_lowest_wyckoff_multiplicity == min_wyckoff_multiplicity:
        lowest_wyckoff_elements.append(A)

    if B_lowest_wyckoff_multiplicity == min_wyckoff_multiplicity:
        lowest_wyckoff_elements.append(B)

    identical_lowest_wyckoff_multiplicity_count = len(lowest_wyckoff_elements)

    data = {
        "WYK_A_lowest_wyckoff": A_lowest_wyckoff_multiplicity,
        "WYK_B_lowest_wyckoff": B_lowest_wyckoff_multiplicity,
        "WYK_identical_lowest_wyckoff_count": identical_lowest_wyckoff_multiplicity_count,
        "WYK_A_sites_total": A_sites_total,
        "WYK_B_sites_total": B_sites_total,
        "WYK_A_multiplicity_total": A_multiplicity_total,
        "WYK_B_multiplicity_total": B_multiplicity_total,
    }

    uni_data = {
        "UNI_WYK_lowest_wyckoff": min_wyckoff_multiplicity,
    }
    
  

    return data, uni_data
