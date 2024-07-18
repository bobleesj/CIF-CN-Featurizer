from core.utils import environment_parser
from core.utils import element_parser
from cifkit import Cif


def compute_ternary_wyk_features(cif: Cif):
    loop_values = cif._loop_values
    elements = list(cif.unique_elements)
    R, M, X = element_parser.get_ternary_RMX_elements(elements)

    R_env, M_env, X_env = environment_parser.get_ternary_atomic_environment_info(loop_values, R, M, X)
    R_sites_total = R_env["sites"]
    R_multiplicity_total = R_env["multiplicity"]
    R_lowest_wyckoff_multiplicity = R_env["lowest_wyckoff_multiplicity"]

    M_sites_total = M_env["sites"]
    M_multiplicity_total = M_env["multiplicity"]
    M_lowest_wyckoff_multiplicity = M_env["lowest_wyckoff_multiplicity"]

    X_sites_total = X_env["sites"]
    X_multiplicity_total = X_env["multiplicity"]
    X_lowest_wyckoff_multiplicity = X_env["lowest_wyckoff_multiplicity"]

    # Create a list to store the elements with the lowest Wyckoff label
    lowest_wyckoff_elements = []

    # Determine the lowest Wyckoff label between A and B
    min_wyckoff_multiplicity = min(
        R_lowest_wyckoff_multiplicity,
        M_lowest_wyckoff_multiplicity,
        X_lowest_wyckoff_multiplicity,
    )

    # If R, M. X the lowest Wyckoff label, add them to the list
    if R_lowest_wyckoff_multiplicity == min_wyckoff_multiplicity:
        lowest_wyckoff_elements.append(R)

    if M_lowest_wyckoff_multiplicity == min_wyckoff_multiplicity:
        lowest_wyckoff_elements.append(M)

    if X_lowest_wyckoff_multiplicity == min_wyckoff_multiplicity:
        lowest_wyckoff_elements.append(X)

    identical_lowest_wyckoff_multiplicity_count = len(lowest_wyckoff_elements)

    data = {
        "WYK_R_lowest_wyckoff": R_lowest_wyckoff_multiplicity,
        "WYK_M_lowest_wyckoff": M_lowest_wyckoff_multiplicity,
        "WYK_X_lowest_wyckoff": X_lowest_wyckoff_multiplicity,
        "WYK_identical_lowest_wyckoff_count": identical_lowest_wyckoff_multiplicity_count,
        "WYK_R_sites_total": R_sites_total,
        "WYK_M_sites_total": M_sites_total,
        "WYK_X_sites_total": X_sites_total,
        "WYK_R_multiplicity_total": R_multiplicity_total,
        "WYK_M_multiplicity_total": M_multiplicity_total,
        "WYK_X_multiplicity_total": X_multiplicity_total,
    }
    uni_data = {
        "UNI_WYK_lowest_wyckoff": min_wyckoff_multiplicity,
    }

    return data, uni_data
