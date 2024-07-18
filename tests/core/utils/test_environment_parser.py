from core.utils.environment_parser import (
    parse_atomic_environment_from_loop,
    get_binary_atomic_environment_info,
    get_ternary_atomic_environment_info,
)

from cifkit import Cif


def test_parse_atomic_environment_from_loop():
    file_path = "tests/cif/binary/Th7Rh3.cif"
    cif = Cif(file_path)
    atomic_env = parse_atomic_environment_from_loop(cif._loop_values)

    assert atomic_env == {
        "Rh": {
            "sites": 1,
            "multiplicity": 6,
            "lowest_wyckoff_multiplicity": 6,
            "lowest_wyckoff_element": "Rh1",
        },
        "Th": {
            "sites": 3,
            "multiplicity": 14,
            "lowest_wyckoff_multiplicity": 2,
            "lowest_wyckoff_element": "Th3",
        },
    }


def test_get_binary_atomic_environment_info():
    file_path = "tests/cif/binary/Th7Rh3.cif"
    cif = Cif(file_path)
    A_info, B_info = get_binary_atomic_environment_info(cif._loop_values, "Th", "Rh")

    assert A_info == {
        "sites": 3,
        "multiplicity": 14,
        "lowest_wyckoff_multiplicity": 2,
        "lowest_wyckoff_element": "Th3",
    }
    assert B_info == {
        "sites": 1,
        "multiplicity": 6,
        "lowest_wyckoff_multiplicity": 6,
        "lowest_wyckoff_element": "Rh1",
    }


def test_get_ternary_atomic_environment_info():
    file_path = "tests/cif/ternary/URhIn.cif"
    cif = Cif(file_path)
    R_env, M_env, X_env = get_ternary_atomic_environment_info(cif._loop_values, "U", "Rh", "In")

    assert R_env == {
        "sites": 1,
        "multiplicity": 3,
        "lowest_wyckoff_multiplicity": 3,
        "lowest_wyckoff_element": "U1",
    }
    assert M_env == {
        "sites": 2,
        "multiplicity": 3,
        "lowest_wyckoff_multiplicity": 1,
        "lowest_wyckoff_element": "Rh2",
    }

    assert X_env == {
        "sites": 1,
        "multiplicity": 3,
        "lowest_wyckoff_multiplicity": 3,
        "lowest_wyckoff_element": "In1",
    }
