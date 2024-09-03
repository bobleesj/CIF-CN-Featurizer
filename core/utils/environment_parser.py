from cifkit.utils.string_parser import strip_numbers_and_symbols
def parse_atomic_environment_from_loop(CIF_loop_values):
    # Initialize a dictionary to store element information
    atomic_env = {}

    # Get the number of atoms
    num_site_labels = len(CIF_loop_values[0])

    # Loop over all atoms
    for i in range(num_site_labels):
        # Get atomic info
        site_label = CIF_loop_values[0][i]
        site_element = strip_numbers_and_symbols(CIF_loop_values[1][i])
        multiplicity = int(CIF_loop_values[2][i])

        if site_element not in atomic_env:
            atomic_env[site_element] = {
                "sites": 0,
                "multiplicity": 0,
                "lowest_wyckoff_multiplicity": multiplicity,
                "lowest_wyckoff_element": site_label,
            }

        # Update the atom information in the dictionary
        atomic_env[site_element]["sites"] += 1
        atomic_env[site_element]["multiplicity"] += multiplicity

        # Update the element with the lowest Wyckoff multiplicity
        if multiplicity < atomic_env[site_element]["multiplicity"]:
            atomic_env[site_element]["lowest_wyckoff_multiplicity"] = multiplicity
            atomic_env[site_element]["lowest_wyckoff_element"] = site_label

    return atomic_env


def get_binary_atomic_environment_info(CIF_loop_values, A, B):
    atomic_env = parse_atomic_environment_from_loop(CIF_loop_values)
    A_env, B_env = None, None

    # Check if the desired elements are present
    if A in atomic_env:
        A_env = atomic_env[A]
    if B in atomic_env:
        B_env = atomic_env[B]

    return A_env, B_env


def get_ternary_atomic_environment_info(CIF_loop_values, R, M, X):
    atomic_env = parse_atomic_environment_from_loop(CIF_loop_values)
    R_env, M_env, X_env = None, None, None

    # Check if the desired elements are present
    if R in atomic_env:
        R_env = atomic_env[R]
    if M in atomic_env:
        M_env = atomic_env[M]
    if X in atomic_env:
        X_env = atomic_env[X]

    return R_env, M_env, X_env
