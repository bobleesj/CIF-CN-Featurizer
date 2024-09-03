from core.utils.element_parser import (
    get_binary_AB_elements,
    get_ternary_RMX_elements,
)
from core.config import get_all_possible_elements


def check_availability_for_binary_ternary(elements):
    possible_elements = get_all_possible_elements()

    for element in elements:
        if element not in possible_elements:
            raise ValueError(f"Element {element} not found in the configuration")

    element_count = len(elements)
    # Check the content either binary or ternary
    if element_count not in [2, 3]:
        raise ValueError(f"Only binary and ternary formulas are supported")

    # Checck the elements existing the in config
    element_count = len(elements)
    if element_count == 2:
        get_binary_AB_elements(elements)
    elif element_count == 3:
        get_ternary_RMX_elements(elements)
