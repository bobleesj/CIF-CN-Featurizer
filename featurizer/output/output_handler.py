from output import output_util


def add_compound_element_cols(binary_df, ternary_df, universal_df, formula):
    # Include A, B, compound columns for binary compounds
    binary_df = output_util.add_formula_info_to_binary_col(binary_df, formula)

    # Include R, M, X, compound columns for ternary compounds
    ternary_df = output_util.add_formula_info_to_ternary_col(
        ternary_df, formula
    )

    # Include compound column for universal
    universal_df = output_util.add_formula_info_to_universal_col(
        universal_df, formula
    )

    return (binary_df, ternary_df, universal_df)
