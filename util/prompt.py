import textwrap
import click
from click import style, echo


def print_intro_message():
    print()
    intro_message = (
        "Welcome to CIF Featurizer!\n"
        "This script processes Crystallographic Information File (CIF) files"
        " to extract various features such as interatomic distances, atomic"
        " environment information, and coordination numbers. "
        " It supports binary and ternary compounds.\n"
    )

    # Use textwrap to ensure that the message fits within a certain width
    click.echo(textwrap.fill(intro_message, width=80))


def get_user_input_on_file_skip():
    click.echo(
        "\nQ1. Do you want to skip any CIF files based on the number of unique in the supercell?"
    )
    skip_based_on_atoms = click.confirm("(Default: N)", default=False)
    print()

    if skip_based_on_atoms:
        click.echo("Files with atoms exceeding this count will be skipped")
        supercell_max_atom_count = click.prompt(
            "Enter the threshold for the maximum number of atoms in the supercell",
            type=int,
        )
    else:
        supercell_max_atom_count = float(
            "inf"
        )  # A large number to essentially disable skipping
    return supercell_max_atom_count


def exceeds_atom_count_limit(all_points, supercell_max_atom_count):
    """
    Checks if the number of unique atomic positions after applyin
    symmetry operations exceeds the specified atom count limit.
    """

    return len(all_points) > supercell_max_atom_count


def print_progress_current(
    i, filename_with_ext, supercell_points, total_file_count
):
    echo(
        style(
            f"Processing {filename_with_ext} with "
            f"{len(supercell_points)} atoms ({i}/{total_file_count})",
            fg="yellow",
        )
    )
