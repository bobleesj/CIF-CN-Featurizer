import pytest
from core.utils.element_parser import get_binary_AB_elements
from core.features.binary_wyc import (
    compute_binary_wyc_features,
)


@pytest.mark.now
def test_compute_binary_wyc_features_ThSb(ThSb_cif):
    result, uni_result = compute_binary_wyc_features(ThSb_cif)

    expected = {
        "WYK_A_lowest_wyckoff": 1,
        "WYK_B_lowest_wyckoff": 1,
        "WYK_identical_lowest_wyckoff_count": 2,
        "WYK_A_sites_total": 1,
        "WYK_B_sites_total": 1,
        "WYK_A_multiplicity_total": 1,
        "WYK_B_multiplicity_total": 1,
    }

    uni_expected = {
        "UNI_WYK_lowest_wyckoff": 1,
    }

    assert result == expected
    assert uni_result == uni_expected


@pytest.mark.now
def test_compute_binary_wyc_features_ThSb(RhSb2_cif):
    result, uni_result = compute_binary_wyc_features(RhSb2_cif)

    expected = {
        "WYK_A_lowest_wyckoff": 4,
        "WYK_B_lowest_wyckoff": 4,
        "WYK_identical_lowest_wyckoff_count": 2,
        "WYK_A_sites_total": 1,
        "WYK_B_sites_total": 2,
        "WYK_A_multiplicity_total": 4,
        "WYK_B_multiplicity_total": 8,
    }

    uni_expected = {"UNI_WYK_lowest_wyckoff": 4}

    assert result == expected
    assert uni_result == uni_expected


@pytest.mark.now
def test_compute_binary_wyc_features_ThSb(Th7Rh3_cif):
    result, uni_result = compute_binary_wyc_features(Th7Rh3_cif)

    expected = {
        "WYK_A_lowest_wyckoff": 2,
        "WYK_B_lowest_wyckoff": 6,
        "WYK_identical_lowest_wyckoff_count": 1,
        "WYK_A_sites_total": 3,
        "WYK_B_sites_total": 1,
        "WYK_A_multiplicity_total": 14,
        "WYK_B_multiplicity_total": 6,
    }

    uni_expected = {"UNI_WYK_lowest_wyckoff": 2}

    print(result, uni_result)

    assert result == expected
    assert uni_result == uni_expected
