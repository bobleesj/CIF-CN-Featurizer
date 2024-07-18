import itertools
from core.config import get_binary_AB_labels
from core.config import get_ternary_RMX_labels


def get_binary_AB_elements(
    elements: list[str],
) -> tuple[str, str]:
    """
    Get A, B elements from a list of two elements.
    """

    A_labels, B_labels = get_binary_AB_labels()

    A: str = None
    B: str = None

    if elements[0] in A_labels and elements[1] in B_labels:
        A = elements[0]
        B = elements[1]
    elif elements[0] in B_labels and elements[1] in A_labels:
        A = elements[1]
        B = elements[0]
    else:
        return sorted(elements)

    return A, B


def get_ternary_RMX_elements(
    elements: list[str],
) -> tuple[str, str, str]:
    """
    Get R, M, X elements from a list of three elements.
    """

    R_labels, M_labels, X_labels = get_ternary_RMX_labels()

    # Use a loop to check each permutation of the input elements
    try:
        for perm in itertools.permutations(elements):
            if perm[0] in R_labels and perm[1] in M_labels and perm[2] in X_labels:
                return (
                    perm[0],
                    perm[1],
                    perm[2],
                )  # R, M, X found correctly
    except IndexError:
        return sorted(elements)
