from util import parser


def add_formula_info_to_universal_col(df, formula):
    """
    Adds a 'formula' column with
    """
    location = (
        df.columns.get_loc("entry") + 1
        if "entry" in df.columns
        else len(df.columns)
    )
    df.insert(location, "formula", formula)
    return df


def add_formula_info_to_binary_col(df, formula):
    """
    Adds 'formula', 'A', and 'B' columns
    """
    num_of_elements = parser.get_num_element(formula)
    parsed_formula = parser.get_parsed_formula(formula)
    if num_of_elements != 2:
        raise ValueError("Formula does not represent a binary formula.")

    A = parsed_formula[0][0]
    B = parsed_formula[1][0]

    location = (
        df.columns.get_loc("entry") + 1
        if "entry" in df.columns
        else len(df.columns)
    )
    df.insert(location, "formula", formula)
    df.insert(location + 1, "A", A)
    df.insert(location + 2, "B", B)
    return df


def add_formula_info_to_ternary_col(df, formula):
    """
    Adds 'formula', 'R', 'M', and 'X' columns
    """
    num_of_elements = parser.get_num_element(formula)
    parsed_formula = parser.get_parsed_formula(formula)
    if num_of_elements != 3:
        raise ValueError("Formula does not represent a ternary formula.")

    R = parsed_formula[0][0]
    M = parsed_formula[1][0]
    X = parsed_formula[2][0]

    location = (
        df.columns.get_loc("entry") + 1
        if "entry" in df.columns
        else len(df.columns)
    )
    df.insert(location, "formula", formula)
    df.insert(location + 1, "R", R)
    df.insert(location + 2, "M", M)
    df.insert(location + 3, "X", X)
    return df


def remove_col_prefix_for_formula_info(col_name):
    prefixes = ["INT_", "INT_"]
    suffixes = ["formula", "R", "M", "X", "A", "B"]

    for prefix in prefixes:
        if col_name.startswith(prefix):
            remaining = col_name[len(prefix) :]
            if remaining in suffixes:
                return remaining
    return col_name
