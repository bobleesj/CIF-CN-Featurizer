import pytest
from core.features.binary_interatomic import (
    compute_binary_interatomic_features,
)


@pytest.mark.now
def test_binary_test(ThSb_cif):
    result, result_uni = compute_binary_interatomic_features(ThSb_cif)

    # Expected values
    expected = {
        "Entry": "ThSb",
        "Formula": "ThSb",
        "A": "Th",
        "B": "Sb",
        "INT_distAA": 3.847,
        "INT_distBB": 3.847,
        "INT_distAB": 3.33159,
        "INT_Asize": 1.798,
        "INT_Bsize": 1.434,
        "INT_Asize_by_Bsize": 1.2538354253835426,
        "INT_distAA_by2_byAsize": 1.0697997775305894,
        "INT_distBB_by2_byBsize": 1.341352859135286,
        "INT_distAB_by2_byAsizebyBsize": 1.0308137376237623,
        "INT_Asize_ref": 1.9235,
        "INT_Bsize_ref": 1.4080899999999996,
        "INT_percent_diff_A_by_100": 0.06979977753058951,
        "INT_percent_diff_B_by_100": -0.018068340306834255,
        "INT_distAA_minus_ref_diff": 0.0,  # (distAA - AA_ref_radius_sum) / distAA
        "INT_distBB_minus_ref_diff": 0.2679542500649859,
        "INT_distAB_minus_ref_diff": 1.3329647701249632e-16,
        "INT_R_factor": 0.005198473864763359,
        "INT_UNI_shortest_homoatomic_dist": 3.847,
        "INT_UNI_shortest_heteroatomic_dist": 3.33159,
        "INT_UNI_shortest_homoatomic_dist_by_2_by_atom_size": 1.0697997775305894,
        "INT_UNI_shortest_heteroatomic_dist_by_sum_of_atom_sizes": 1.0308137376237623,
        "INT_UNI_shortest_homoatomic_dist_by_2_by_refined_atom_size": 1.0,
        "INT_UNI_shortest_heteroatomic_dist_by_sum_of_refined_atom_sizes": 1.0000000000000002,
        "INT_UNI_highest_refined_percent_diff_abs": 0.06979977753058951,
        "INT_UNI_lowest_refined_percent_diff_abs": 0.018068340306834255,
        "INT_UNI_refined_packing_efficiency": 0.72900,
    }

    # Check each expected value
    for key, expected_value in expected.items():
        # For float
        if isinstance(expected_value, float):
            assert result[key] == pytest.approx(expected_value, abs=0.001)
        # For str, integer, etc.
        else:
            assert result[key] == expected_value
