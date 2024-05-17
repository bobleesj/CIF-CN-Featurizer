from util import parser


def add_formula_info_to_universal_col(df, formula):
    """
    Adds a 'compound' column with
    """
    location = (
        df.columns.get_loc("entry") + 1
        if "entry" in df.columns
        else len(df.columns)
    )
    df.insert(location, "compound", formula)
    return df


def add_formula_info_to_binary_col(df, formula):
    """
    Adds 'compound', 'A', and 'B' columns
    """
    num_of_elements = parser.get_num_element(formula)
    parsed_formula = parser.get_parsed_formula(formula)
    if num_of_elements != 2:
        raise ValueError("Formula does not represent a binary compound.")

    A = parsed_formula[0][0]
    B = parsed_formula[1][0]

    location = (
        df.columns.get_loc("entry") + 1
        if "entry" in df.columns
        else len(df.columns)
    )
    df.insert(location, "compound", formula)
    df.insert(location + 1, "A", A)
    df.insert(location + 2, "B", B)
    return df


def add_formula_info_to_ternary_col(df, formula):
    """
    Adds 'compound', 'R', 'M', and 'X' columns
    """
    num_of_elements = parser.get_num_element(formula)
    parsed_formula = parser.get_parsed_formula(formula)
    if num_of_elements != 3:
        raise ValueError("Formula does not represent a ternary compound.")

    R = parsed_formula[0][0]
    M = parsed_formula[1][0]
    X = parsed_formula[2][0]

    location = (
        df.columns.get_loc("entry") + 1
        if "entry" in df.columns
        else len(df.columns)
    )
    df.insert(location, "compound", formula)
    df.insert(location + 1, "R", R)
    df.insert(location + 2, "M", M)
    df.insert(location + 3, "X", X)
    return df
