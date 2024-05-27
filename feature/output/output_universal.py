from util import df_util
from feature.output import wyckoff_cols_drop
from feature import coordination_number_util
import pandas as pd

# from feature import coordination_number_util as cn_util

pd.set_option("display.max_columns", None)  # Ensure all columns are shown
pd.set_option("display.max_rows", None)  # Ensure all rows are shown


def postprocess_merge_dfs(
    interatomic_universal_df,
    atomic_env_wyckoff_universal_df,
    cn_universal_df,
):
    # print(cn_universal_df)
    # Define columns to keep for aggregation which are numeric
    cols_to_keep = [
        "coordination_number",
        "polyhedron_volume",
        "central_atom_to_center_of_mass_dist",
        "number_of_edges",
        "number_of_faces",
        "shortest_distance_to_face",
        "shortest_distance_to_edge",
        "volume_of_inscribed_sphere",
        "packing_efficiency",
    ]

    # Group by 'Entry' and 'central_atom', and only include the numeric columns
    grouped = cn_universal_df.groupby(["Entry", "central_atom"])[cols_to_keep]

    # Calculate the average, min, and max
    cn_uni_avg_df = grouped.mean().reset_index()
    cn_uni_min_df = grouped.min().reset_index()
    cn_uni_max_df = grouped.max().reset_index()

    cn_avg_df_copy = cn_uni_avg_df.copy()
    cn_min_df_copy = cn_uni_min_df.copy()
    cn_max_df_copy = cn_uni_max_df.copy()

    cn_avg_df_copy = df_util.drop_unwanted_columns(
        cn_avg_df_copy, ["Formula", "central_atom"]
    )
    cn_min_df_copy = df_util.drop_unwanted_columns(
        cn_min_df_copy, ["Formula", "central_atom"]
    )
    cn_max_df_copy = df_util.drop_unwanted_columns(
        cn_max_df_copy, ["Formula", "central_atom"]
    )

    cn_avg_avg_df = cn_avg_df_copy.groupby("Entry").mean()
    cn_avg_min_df = cn_min_df_copy.groupby("Entry").mean()
    cn_avg_max_df = cn_max_df_copy.groupby("Entry").mean()
    cn_avg_avg_df = df_util.prefix_columns(cn_avg_avg_df, "CN_AVG_")
    cn_avg_min_df = df_util.prefix_columns(cn_avg_min_df, "CN_MIN_")
    cn_avg_max_df = df_util.prefix_columns(cn_avg_max_df, "CN_MAX_")

    # Make copies of the dataframes to avoid modifying the original ones
    interatomic_universal_df_copy = interatomic_universal_df.copy()
    atomic_env_wyckoff_universal_df_copy = (
        atomic_env_wyckoff_universal_df.copy()
    )

    # Add column pre-fixes
    interatomic_universal_df_copy = df_util.prefix_columns(
        interatomic_universal_df_copy, "INT_UNI_"
    )
    atomic_env_wyckoff_universal_df_copy = df_util.prefix_columns(
        atomic_env_wyckoff_universal_df_copy, "WYC_UNI_"
    )

    merged_df = df_util.merge_dfs_on_entry(
        [
            interatomic_universal_df_copy,
            atomic_env_wyckoff_universal_df_copy,
            cn_avg_avg_df,
            cn_avg_min_df,
            cn_avg_max_df,
        ]
    )

    print(merged_df)
    return merged_df
