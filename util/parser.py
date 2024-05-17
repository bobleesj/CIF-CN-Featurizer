import re


def remove_string_braket(value_string):
    """
    Removes parentheses from a value string and convert to float if possible.
    """
    return (
        float(value_string.split("(")[0])
        if "(" in value_string
        else float(value_string)
    )


def get_parsed_formula(formula):
    pattern = r"([A-Z][a-z]*)(\d*\.?\d*)"
    elements = re.findall(pattern, formula)
    return elements


def get_num_element(formula):
    elements = get_parsed_formula(formula)
    return len(elements)
