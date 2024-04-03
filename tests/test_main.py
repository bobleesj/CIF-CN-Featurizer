import os
import shutil
import pandas as pd

from main import run_main


def generate_features(formula):
    print("Let's test the main output")
    cif_dir = f"tests/cif/{formula}"
    csv_dir = os.path.join(cif_dir, "csv")

    output_dir = f"tests/output/{formula}"
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copytree(cif_dir, output_dir, dirs_exist_ok=True)

    run_main(False, output_dir)

    output_csv_dir = os.path.join(output_dir, "csv")

    original_csv_files = sorted(
        [
            os.path.join(csv_dir, f)
            for f in os.listdir(csv_dir)
            if f.endswith(".csv")
        ]
    )
    output_csv_files = sorted(
        [
            os.path.join(output_csv_dir, f)
            for f in os.listdir(output_csv_dir)
            if f.endswith(".csv")
        ]
    )

    for original_file, output_file in zip(
        original_csv_files, output_csv_files
    ):
        original_df = pd.read_csv(original_file)
        output_df = pd.read_csv(output_file)
        # Round all numerical columns to 2 decimal places
        original_df_rounded = original_df.round(2)
        output_df_rounded = output_df.round(2)

        try:
            pd.testing.assert_frame_equal(
                original_df_rounded, output_df_rounded, check_like=True, atol=1e-5
            )

        except AssertionError as e:
            assert (
                False
            ), f"File contents do not match: {original_file} and {output_file}\n{e}"


def test_main():
    generate_features("ThSb")
    generate_features("URhIn")
