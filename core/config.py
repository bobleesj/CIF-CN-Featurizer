def get_binary_AB_labels() -> tuple[list[str], list[str]]:
    A_labels = [
        "Sc",
        "Y",
        "La",
        "Ce",
        "Pr",
        "Nd",
        "Sm",
        "Eu",
        "Gd",
        "Tb",
        "Dy",
        "Ho",
        "Er",
        "Tm",
        "Yb",
        "Lu",
        "Th",
        "U",
        "Fe",
        "Co",
        "Ni",
    ]
    B_labels = ["Si", "Ga", "Ge", "In", "Sn", "Sb", "Al", "Pd", "Rh"]

    return A_labels, B_labels


def get_ternary_RMX_labels() -> tuple[list[str], list[str], list[str]]:
    R_labels = [
        "Sc",
        "Y",
        "La",
        "Ce",
        "Pr",
        "Nd",
        "Sm",
        "Eu",
        "Gd",
        "Tb",
        "Dy",
        "Ho",
        "Er",
        "Tm",
        "Yb",
        "Lu",
        "Th",
        "U",
    ]
    M_labels = ["Si", "Ga", "Ge", "Rh", "Sn", "Sb", "Al"]

    X_labels = [
        "Fe",
        "Co",
        "Ni",
        "Ru",
        "In",
        "Pd",
        "Os",
        "Ir",
        "Pt",
    ]

    return R_labels, M_labels, X_labels


def get_all_possible_elements() -> list[str]:
    possible_elements = [
        "Si",
        "Sc",
        "Fe",
        "Co",
        "Ni",
        "Ga",
        "Ge",
        "Y",
        "Ru",
        "Rh",
        "Pd",
        "In",
        "Sn",
        "Sb",
        "La",
        "Ce",
        "Pr",
        "Nd",
        "Sm",
        "Eu",
        "Gd",
        "Tb",
        "Dy",
        "Ho",
        "Er",
        "Tm",
        "Yb",
        "Lu",
        "Os",
        "Ir",
        "Pt",
        "Th",
        "U",
        "Al",
        "Mo",
        "Hf",
        "Ta",
    ]
    return possible_elements
