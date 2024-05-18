from featurizer.output import wyckoff_cols_drop
from util import df_util


def postprocess_merge_dfs(
    interatomic_universal_df, atomic_env_wyckoff_universal_df
):
    # Make copies of the dataframes to avoid modifying the original ones
    interatomic_universal_df_copy = interatomic_universal_df.copy()
    atomic_env_wyckoff_universal_df_copy = (
        atomic_env_wyckoff_universal_df.copy()
    )

    # Drop some Wychoff columns
    columns_to_drop = wyckoff_cols_drop.get_wychoff_columns_to_drop()
    atomic_env_wyckoff_universal_df_copy = df_util.drop_unwanted_columns(
        atomic_env_wyckoff_universal_df_copy, columns_to_drop
    )

    # Add column pre-fixes
    interatomic_universal_df_copy = df_util.prefix_columns(
        interatomic_universal_df_copy, "INT_UNI_"
    )
    atomic_env_wyckoff_universal_df_copy = df_util.prefix_columns(
        atomic_env_wyckoff_universal_df_copy, "WYC_UNI_"
    )

    merged_df = df_util.merge_dfs_on_entry(
        [interatomic_universal_df_copy, atomic_env_wyckoff_universal_df_copy]
    )

    return merged_df
