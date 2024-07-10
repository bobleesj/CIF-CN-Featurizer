import pandas as pd
from core.utils import df_util


def compute_avg_avg_cn_values(cn_avg_df, cn_min_df, cn_max_df):
    cn_avg_df_copy = cn_avg_df.copy()
    cn_min_df_copy = cn_min_df.copy()
    cn_max_df_copy = cn_max_df.copy()

    cn_avg_df_copy = df_util.drop_central_atom_formula_cols(cn_avg_df_copy)
    cn_min_df_copy = df_util.drop_central_atom_formula_cols(cn_min_df_copy)
    cn_max_df_copy = df_util.drop_central_atom_formula_cols(cn_max_df_copy)

    # Grouping by 'entry' and calculating the mean for other numeric columns
    cn_avg_avg_df = cn_avg_df_copy.groupby("Entry").mean()
    cn_avg_min_df = cn_min_df_copy.groupby("Entry").mean()
    cn_avg_max_df = cn_max_df_copy.groupby("Entry").mean()
    return cn_avg_avg_df, cn_avg_min_df, cn_avg_max_df
