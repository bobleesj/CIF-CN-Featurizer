import textwrap
import click
import textwrap
import click


def print_intro_message():
    print()
    intro_message = (
        "Welcome to CIF Featurizer!\n"
        "This script processes Crystallographic Information File (CIF) files to extract various features such as interatomic distances, atomic environment information, and coordination numbers. It supports binary and ternary compounds.\n"
        "It is recommended to preprocess all CIF files with CIF Cleaner to ensure data consistency and to handle any potential errors in the CIF files. For more details, visit: https://github.com/bobleesj/cif-cleaner\n"
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


import click


def exceeds_atom_count_limit(all_points, supercell_max_atom_count):
    """
    Checks if the number of unique atomic positions after applying symmetry operations
    exceeds the specified atom count limit.
    """

    return len(all_points) > supercell_max_atom_count


# def get_user_input_on_supercell_generation_method():
#     click.echo("\nDo you want to modify the supercell generation method for CIF files with more than 200 atoms in the unit cell?")
#     is_supercell_generation_method_modified = click.confirm('(Default: N)', default=False)

#     if is_supercell_generation_method_modified:
#         click.echo("\nChoose a supercell generation method:")
#         click.echo("1. No shift (fastest)")
#         click.echo("2. +1 +1 +1 shifts in x, y, z directions")
#         click.echo("3. +-1, +-1, +-1 shifts (2x2x2 supercell generation, requires heavy computation, slowest)")

#         method = click.prompt("Choose your option by entering a number", type=int)

#         if method == 1:
#             click.echo("You've selected: No shift (fastest)\n")
#         elif method == 2:
#             click.echo("You've selected: +1 +1 +1 shifts in x, y, z directions\n")
#         elif method == 3:
#             click.echo("You've selected: +-1, +-1, +-1 shifts (2x2x2 supercell generation, slowest)\n")
#         else:
#             click.echo("Invalid option. Defaulting to No shift (fastest)\n")
#             method = 1
#     else:
#         method = None

#     return method
