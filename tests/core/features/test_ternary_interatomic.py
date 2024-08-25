import pytest
from cifkit import Cif
from core.features.ternary_interatomic import (
    compute_ternary_interatomic_features,
)


@pytest.mark.now
def test_compute_ternary_interatomic_feature():
    file_path = "tests/cif/ternary/URhIn.cif"
    cif = Cif(file_path)
    result = compute_ternary_interatomic_features(cif)
    expected = {
        "Entry": "URhIn",
        "Formula": "URhIn",
        "R": "U",
        "M": "Rh",
        "X": "In",
        "distRR": 3.881,
        "distMM": 3.881,
        "distXX": 3.24367,
        "distRM": 2.98347,
        "distMX": 2.69678,
        "distRX": 3.20977,
        "Rsize": 1.377,
        "Msize": 1.345,
        "Xsize": 1.624,
        "Rsize_by_Msize": 1.0237918215613384,
        "Msize_by_Xsize": 0.8282019704433496,
        "Rsize_by_Xsize": 0.8479064039408867,
        "distRR_by2_byRsize": 1.4092229484386347,
        "distMM_by2_byMsize": 1.4427509293680296,
        "distXX_by2_byXsize": 0.9986668719211822,
        "distRM_byRsizebyMsize": 1.0960580455547393,
        "distMX_byMsizebyXsize": 0.9083125631525765,
        "distRX_byRsizebyXsize": 1.0695668110629788,
        "Rsize_ref": 1.6147054655661603,
        "Msize_ref": 1.3687645344338397,
        "Xsize_ref": 1.32801546556616,
        "percent_diff_R_by_100": 0.17262561043294142,
        "percent_diff_M_by_100": 0.017668798835568586,
        "percent_diff_X_by_100": -0.18225648672034486,
        "distRR_minus_ref_diff": 0.16789205587932984,
        "distMM_minus_ref_diff": 0.2946330665118063,
        "distXX_minus_ref_diff": 0.18116487462278216,
        "distRM_minus_ref_diff": 0,
        "distMX_minus_ref_diff": 0,
        "distRX_minus_ref_diff": 0.08327217511284406,
        "refined_packing_eff": 0.60985,
        "R_factor": 0.06332921478128069,
        "shortest_homoatomic_dist": 3.24367,
        "shortest_heteroatomic_dist": 2.69678,
        "shortest_homoatomic_dist_by_2_by_atom_size": 0.9986668719211822,
        "shortest_heteroatomic_dist_by_sum_of_atom_sizes": 0.9083125631525765,
        "shortest_homoatomic_dist_by_2_by_refined_atom_size": 1.2212470728332812,
        "shortest_heteroatomic_dist_by_sum_of_refined_atom_sizes": 1.0000000000000002,
        "highest_refined_percent_diff_abs": 0.18225648672034486,
        "lowest_refined_percent_diff_abs": 0.017668798835568586,
        "packing_efficiency": 0.60985,
    }

    # Check each expected value
    for key, expected_value in expected.items():
        if key == "R_factor":
            assert result[key] == pytest.approx(
                expected_value,
                abs=0.05,  # Optimization obj may be different
            )
        else:
            # For float
            if isinstance(expected_value, float):
                assert result[key] == pytest.approx(expected_value, abs=0.001)
            # For str, integer, etc.
            else:
                assert result[key] == expected_value
