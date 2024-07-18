def parse_atomic_environment_from_loop(CIF_loop_values):
    # Initialize a dictionary to store element information
    atomic_env = {}

    # Get the number of atoms
    num_atoms = len(CIF_loop_values[0])

    # Loop over all atoms
    for i in range(num_atoms):
        # Get atomic info
        label = CIF_loop_values[0][i]
        type_symbol = CIF_loop_values[1][i]
        multiplicity = int(CIF_loop_values[2][i])

        if type_symbol not in atomic_env:
            atomic_env[type_symbol] = {
                "sites": 0,
                "multiplicity": 0,
                "lowest_wyckoff_multiplicity": multiplicity,
                "lowest_wyckoff_element": label,
            }

        # Update the atom information in the dictionary
        atomic_env[type_symbol]["sites"] += 1
        atomic_env[type_symbol]["multiplicity"] += multiplicity

        # Update the element with the lowest Wyckoff multiplicity
        if multiplicity < atomic_env[type_symbol]["multiplicity"]:
            atomic_env[type_symbol]["lowest_wyckoff_multiplicity"] = multiplicity
            atomic_env[type_symbol]["lowest_wyckoff_element"] = label

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
