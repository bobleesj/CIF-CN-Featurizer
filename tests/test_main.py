import os
import pandas as pd
from main import run_main


def check_csv_files(output_dir, files_to_check):
    """Helper function to check expected vs. actual CSV files."""
    for file_name in files_to_check:
        expected_file_path = os.path.join(output_dir, "csv_expected", file_name)
        output_file_path = os.path.join(output_dir, "csv", file_name)

        # Read the expected and output dataframes
        expected_df = pd.read_csv(expected_file_path)
        output_df = pd.read_csv(output_file_path)

        # Check the data frame equality
        try:
            pd.testing.assert_frame_equal(
                expected_df,
                output_df,
                check_like=True,  # Ensure columns do not have to be same order
                check_dtype=False,  # Allow different data types for more robust comparison
                atol=0.01,  # Allow a small difference in numeric values
            )
        except AssertionError as e:
            assert False, f"DataFrame contents do not match in {file_name}: {e}"


def test_ternary_features():
    # Directory where the output is stored
    output_dir = "tests/output/URhIn"

    # Run the main function which processes the data and writes output CSV
    run_main(False, output_dir)

    # Define the list of files to check
    files_to_check = ["feature_ternary.csv", "feature_universal.csv"]

    # Check CSV files
    check_csv_files(output_dir, files_to_check)


def test_binary_features():
    # Directory where the output is stored
    output_dir = "tests/output/ThSb"

    run_main(False, output_dir)

    # Define the list of files to check
    files_to_check = ["feature_binary.csv", "feature_universal.csv"]

    # Check CSV files
    check_csv_files(output_dir, files_to_check)


def test_binary_ternary_combined_features():
    # Directory where the output is stored
    output_dir = "tests/output/combined"

    run_main(False, output_dir)

    # Define the list of files to check
    files_to_check = [
        "feature_binary.csv",
        "feature_ternary.csv",
        "feature_universal.csv",
    ]

    # Check CSV files
    check_csv_files(output_dir, files_to_check)
