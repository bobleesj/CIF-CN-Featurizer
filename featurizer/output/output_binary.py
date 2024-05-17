import pandas as pd
from featurizer.output import wyckoff_cols_drop
from util import df_util as df
from util.folder import save_to_csv_directory
from util import df_util

# Set pandas options to display all columns
pd.set_option("display.max_columns", None)


def prefix_columns(df, prefix):
    df.columns = [
        prefix + col if col != "entry" else col for col in df.columns
    ]
    return df


def drop_unwanted_columns(df, columns_to_drop=["A", "B", "Compound"]):
    return df.drop(
        columns=[col for col in columns_to_drop if col in df.columns]
    )


def merge_dfs_and_save_binary_output(
    interatomic_binary_df,
    interatomic_universal_df,
    atomic_env_wyckoff_binary_df,
    atomic_env_wyckoff_universal_df,
    atomic_env_binary_df,
    cn_binary_avg_df,
    cn_binary_min_df,
    cn_binary_max_df,
):
    columns_to_drop = wyckoff_cols_drop.get_wychoff_columns_to_drop()
    cn_binary_avg_df = df_util.drop_central_atom_compound_cols(
        cn_binary_avg_df
    )
    cn_binary_min_df = df_util.drop_central_atom_compound_cols(
        cn_binary_min_df
    )
    cn_binary_max_df = df_util.drop_central_atom_compound_cols(
        cn_binary_max_df
    )

    # Grouping by 'entry' and calculating the mean for other numeric columns
    cn_binary_avg_avg_df = cn_binary_avg_df.groupby("entry").mean()
    cn_binary_avg_min_df = cn_binary_min_df.groupby("entry").mean()
    cn_binary_avg_max_df = cn_binary_max_df.groupby("entry").mean()

    # Dropping unwanted columns from each DataFrame
    atomic_env_wyckoff_binary_df = drop_unwanted_columns(
        atomic_env_wyckoff_binary_df, columns_to_drop
    )
    atomic_env_wyckoff_universal_df = drop_unwanted_columns(
        atomic_env_wyckoff_universal_df, columns_to_drop
    )

    interatomic_binary_df = df_util.prefix_columns(
        interatomic_binary_df, "INT_BI_"
    )
    interatomic_universal_df = df_util.prefix_columns(
        interatomic_universal_df, "INT_UNI_"
    )
    atomic_env_wyckoff_binary_df = df_util.prefix_columns(
        atomic_env_wyckoff_binary_df, "WYC_BI_"
    )
    atomic_env_wyckoff_universal_df = df_util.prefix_columns(
        atomic_env_wyckoff_universal_df, "WYC_UNI_"
    )
    atomic_env_binary_df = df_util.prefix_columns(
        atomic_env_binary_df, "ENV_BI_"
    )
    cn_binary_avg_avg_df = df_util.prefix_columns(
        cn_binary_avg_avg_df, "CN_AVG_"
    )
    cn_binary_avg_min_df = df_util.prefix_columns(
        cn_binary_avg_min_df, "CN_MIN_"
    )
    cn_binary_avg_max_df = df_util.prefix_columns(
        cn_binary_avg_max_df, "CN_MAX_"
    )

    # Merging the DataFrames based on 'CIF_id' with suffixes
    # to avoid duplicate columns
    merged_df = (
        interatomic_binary_df.merge(
            interatomic_universal_df,
            on="entry",
        )
        .merge(
            atomic_env_wyckoff_binary_df,
            on="entry",
        )
        .merge(
            atomic_env_wyckoff_universal_df,
            on="entry",
        )
        .merge(atomic_env_binary_df, on="entry")
        .merge(cn_binary_avg_avg_df, on="entry")
        .merge(cn_binary_avg_min_df, on="entry")
        .merge(cn_binary_avg_max_df, on="entry")
    )

    # Print the head of the merged DataFrame
    for i, column in enumerate(merged_df.columns):
        print(i + 1, column)


def save_individual_binary_outputs(
    interatomic_binary_df,
    atomic_env_wyckoff_binary_df,
    atomic_env_binary_df,
    cn_binary_df,
    cn_binary_avg_df,
    cn_binary_min_df,
    cn_binary_max_df,
    cif_dir,
):
    # Dictionary of DataFrames and their corresponding file names
    dataframes = {
        "coordination_number_binary_all": cn_binary_df,
        "coordination_number_binary_avg": cn_binary_avg_df,
        "coordination_number_binary_min": cn_binary_min_df,
        "coordination_number_binary_max": cn_binary_max_df,
        "interatomic_features_binary": interatomic_binary_df,
        "atomic_environment_features_binary": atomic_env_binary_df,
        "atomic_environment_wyckoff_multiplicity_features_binary": atomic_env_wyckoff_binary_df,
    }

    # Loop through the dictionary and save each DataFrame
    for file_name, df in dataframes.items():
        save_to_csv_directory(cif_dir, df_util.round_df(df), file_name)
