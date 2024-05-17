from util import df_util
from util import folder


def save_log(is_interactive_mode, df, cif_dir):
    if is_interactive_mode:
        folder.save_to_csv_directory(
            cif_dir, df_util.round_df(df), "featurizer_log"
        )
