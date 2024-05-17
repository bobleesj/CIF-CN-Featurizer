def join_columns_with_comma(df):
    columns = [
        "Mendeleev_number_of_elements_with_lowest_wyckoff",
        "valence_e_of_elements_with_lowest_wyckoff",
        "lowest_wyckoff_elements",
        "CIF_rad_of_elements_with_lowest_wyckoff",
        "CIF_rad_refined_of_elements_with_lowest_wyckoff",
        "Pauling_rad_of_elements_with_lowest_wyckoff",
        "Pauling_EN_of_elements_with_lowest_wyckoff",
        "MB_EN_of_elements_with_lowest_wyckoff",
    ]

    for column in columns:
        df[column] = df[column].apply(lambda x: ", ".join(map(str, x)))

    return df


def wyckoff_mapping_to_number_binary(df):
    wyckoff_mapping = {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
        "f": "6",
        "g": "7",
        "h": "8",
        "i": "9",
        "j": "10",
    }
    columns_to_map_binary = [
        "A_lowest_wyckoff_label",
        "B_lowest_wyckoff_label",
    ]

    for col in columns_to_map_binary:
        df[col] = df[col].replace(wyckoff_mapping)

    return df


def wyckoff_mapping_to_number_ternary(df):
    wyckoff_mapping = {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
        "f": "6",
        "g": "7",
        "h": "8",
        "i": "9",
        "j": "10",
    }
    columns_to_map_ternary = [
        "R_lowest_wyckoff_label",
        "M_lowest_wyckoff_label",
        "X_lowest_wyckoff_label",
    ]

    for col in columns_to_map_ternary:
        df[col] = df[col].replace(wyckoff_mapping)

    return df


def drop_central_atom_compound_cols(df):
    return df.drop(["central_atom", "compound"], axis=1)


def get_avg_min_max_dfs(df, cols_to_keep):
    avg_df = df.groupby(cols_to_keep).mean().reset_index()
    min_df = df.groupby(cols_to_keep).min().reset_index()
    max_df = df.groupby(cols_to_keep).max().reset_index()

    return avg_df, min_df, max_df


def round_df(df):
    numeric_cols = df.select_dtypes(include=["float64"]).columns
    df[numeric_cols] = df[numeric_cols].round(4)
    return df


def prefix_columns(df, prefix):
    df.columns = [
        prefix + col if col != "entry" else col for col in df.columns
    ]
    return df


def drop_unwanted_columns(df, columns_to_drop=["A", "B", "Compound"]):
    return df.drop(
        columns=[col for col in columns_to_drop if col in df.columns]
    )
