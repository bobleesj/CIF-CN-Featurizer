import pandas as pd
from featurizer.output import wyckoff_cols_drop
from util import df_util

# Set pandas options to display all columns
pd.set_option("display.max_columns", None)


def postprocess_merge_dfs(
    interatomic_ternary_df,
    interatomic_universal_df,
    atomic_env_wyckoff_ternary_df,
    atomic_env_wyckoff_universal_df,
    atomic_env_ternary_df,
    cn_ternary_avg_df,
    cn_ternary_min_df,
    cn_ternary_max_df,
):
    columns_to_drop = wyckoff_cols_drop.get_wychoff_columns_to_drop()

    cn_ternary_avg_df = df_util.drop_central_atom_compound_cols(
        cn_ternary_avg_df
    )
    cn_ternary_min_df = df_util.drop_central_atom_compound_cols(
        cn_ternary_min_df
    )
    cn_ternary_max_df = df_util.drop_central_atom_compound_cols(
        cn_ternary_max_df
    )

    # Grouping by 'entry' and calculating the mean for other numeric columns
    cn_ternary_avg_avg_df = cn_ternary_avg_df.groupby("entry").mean()
    cn_ternary_avg_min_df = cn_ternary_min_df.groupby("entry").mean()
    cn_ternary_avg_max_df = cn_ternary_max_df.groupby("entry").mean()

    # Dropping unwanted columns from each DataFrame
    atomic_env_wyckoff_ternary_df = df_util.drop_unwanted_columns(
        atomic_env_wyckoff_ternary_df, columns_to_drop
    )
    atomic_env_wyckoff_universal_df = df_util.drop_unwanted_columns(
        atomic_env_wyckoff_universal_df, columns_to_drop
    )

    interatomic_ternary_df = df_util.prefix_columns(
        interatomic_ternary_df, "INT_BI_"
    )
    interatomic_universal_df = df_util.prefix_columns(
        interatomic_universal_df, "INT_UNI_"
    )
    atomic_env_wyckoff_ternary_df = df_util.prefix_columns(
        atomic_env_wyckoff_ternary_df, "WYC_BI_"
    )
    atomic_env_wyckoff_universal_df = df_util.prefix_columns(
        atomic_env_wyckoff_universal_df, "WYC_UNI_"
    )
    atomic_env_ternary_df = df_util.prefix_columns(
        atomic_env_ternary_df, "ENV_BI_"
    )
    cn_ternary_avg_avg_df = df_util.prefix_columns(
        cn_ternary_avg_avg_df, "CN_AVG_"
    )
    cn_ternary_avg_min_df = df_util.prefix_columns(
        cn_ternary_avg_min_df, "CN_MIN_"
    )
    cn_ternary_avg_max_df = df_util.prefix_columns(
        cn_ternary_avg_max_df, "CN_MAX_"
    )

    # Merging the DataFrames based on 'CIF_id' with suffixes
    # to avoid duplicate columns
    dfs = [
        interatomic_ternary_df,
        interatomic_universal_df,
        atomic_env_wyckoff_ternary_df,
        atomic_env_wyckoff_universal_df,
        atomic_env_ternary_df,
        cn_ternary_avg_avg_df,
        cn_ternary_avg_min_df,
        cn_ternary_avg_max_df,
    ]
    merged_df = df_util.merge_dfs_on_entry(dfs)

    return merged_df
