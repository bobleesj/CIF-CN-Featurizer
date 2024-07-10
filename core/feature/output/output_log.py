from core.utils import df_util
from core.utils import folder


def save_log_csv(is_interactive_mode, df, cif_dir):
    if is_interactive_mode:
        folder.save_df_to_csv(cif_dir, df_util.round_df(df), "log")
