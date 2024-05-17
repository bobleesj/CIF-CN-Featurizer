from featurizer.output import wyckoff_cols_drop
from util import df_util


def postprocess_merge_dfs(
    interatomic_universal_df, atomic_env_wyckoff_universal_df
):
    # Rename columns by replacing 'INT_' or 'UNI_INT' with ''
    interatomic_universal_df.columns = [
        col.replace("INT_UNI_", "").replace("INT_UNI_INT_UNI_", "")
        for col in interatomic_universal_df.columns
    ]

    # Drop some Wychoff columns
    columns_to_drop = wyckoff_cols_drop.get_wychoff_columns_to_drop()
    atomic_env_wyckoff_universal_df = df_util.drop_unwanted_columns(
        atomic_env_wyckoff_universal_df, columns_to_drop
    )

    # Add column pre-fixes
    interatomic_universal_df = df_util.prefix_columns(
        interatomic_universal_df, "INT_UNI_"
    )
    atomic_env_wyckoff_universal_df = df_util.prefix_columns(
        atomic_env_wyckoff_universal_df, "WYC_UNI_"
    )

    merged_df = df_util.merge_dfs_on_entry(
        [interatomic_universal_df, atomic_env_wyckoff_universal_df]
    )

    return merged_df
