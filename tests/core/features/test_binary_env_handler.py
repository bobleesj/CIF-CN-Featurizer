import pytest
from core.features.binary_env_handler import (
    compute_binary_env_features,
)

from core.utils.log import print_connected_points

@pytest.mark.now
def test_compute_binary_env_features_ThSb(ThSb_cif):
    print_connected_points(ThSb_cif.connections)
    # assert False
    result = compute_binary_env_features(ThSb_cif)
    expected = {
        "ENV_A_shortest_dist_count": 8,
        "ENV_B_shortest_dist_count": 8,
        "ENV_A_avg_shortest_dist_count": 8.0,
        "ENV_B_avg_shortest_dist_count": 8.0,
        "ENV_A_shortest_tol_dist_count": 8,
        "ENV_B_shortest_tol_dist_count": 8,
        "ENV_A_avg_shortest_dist_within_tol_count": 8.0,
        "ENV_B_avg_shortest_dist_within_tol_count": 8.0,
        "ENV_A_second_by_first_shortest_dist": 1.1561561561561562,
        "ENV_B_second_by_first_shortest_dist": 1.1561561561561562,
        "ENV_A_avg_second_by_first_shortest_dist": 1.1561561561561562,
        "ENV_B_avg_second_by_first_shortest_dist": 1.1561561561561562,
        "ENV_A_second_shortest_dist_count": 6,
        "ENV_B_second_shortest_dist_count": 6,
        "ENV_A_avg_second_shortest_dist_count": 6.0,
        "ENV_B_avg_second_shortest_dist_count": 6.0,
        "ENV_A_homoatomic_dist_by_shortest_dist": 1.1552552552552553,
        "ENV_B_homoatomic_dist_by_shortest_dist": 1.1552552552552553,
        "ENV_A_avg_homoatomic_dist_by_shortest_dist": 1.1552552552552553,
        "ENV_B_avg_homoatomic_dist_by_shortest_dist": 1.1552552552552553,
        "ENV_A_count_at_A_shortest_dist": 0,
        "ENV_A_count_at_B_shortest_dist": 8,
        "ENV_A_avg_count_at_A_shortest_dist": 0.0,
        "ENV_A_avg_count_at_B_shortest_dist": 8.0,
        "ENV_B_count_at_A_shortest_dist": 8,
        "ENV_B_count_at_B_shortest_dist": 0,
        "ENV_B_avg_count_at_A_shortest_dist": 8.0,
        "ENV_B_avg_count_at_B_shortest_dist": 0.0,
    }

    for key in result:
        assert result[key] == pytest.approx(expected[key], abs=0.005)

@pytest.mark.now
def test_compute_binary_env_features_RhSb2(RhSb2_cif):
    print_connected_points(RhSb2_cif.connections)

    result = compute_binary_env_features(RhSb2_cif)
    expected = {
        "ENV_A_shortest_dist_count": 1,
        "ENV_B_shortest_dist_count": 1,
        "ENV_A_avg_shortest_dist_count": 1.0,
        "ENV_B_avg_shortest_dist_count": 1.0,
        "ENV_A_shortest_tol_dist_count": 3,
        "ENV_B_shortest_tol_dist_count": 3,
        "ENV_A_avg_shortest_dist_within_tol_count": 3.0,
        "ENV_B_avg_shortest_dist_within_tol_count": 3.0,
        "ENV_A_second_by_first_shortest_dist": 1.0151033386327504,
        "ENV_B_second_by_first_shortest_dist": 1.0151033386327504,
        "ENV_A_avg_second_by_first_shortest_dist": 1.0151033386327504,
        "ENV_B_avg_second_by_first_shortest_dist": 1.0084943540825893,
        "ENV_A_second_shortest_dist_count": 1,
        "ENV_B_second_shortest_dist_count": 2,
        "ENV_A_avg_second_shortest_dist_count": 1.0,
        "ENV_B_avg_second_shortest_dist_count": 1.0,
        "ENV_A_homoatomic_dist_by_shortest_dist": 1.1971383147853736,
        "ENV_B_homoatomic_dist_by_shortest_dist": 1.1244038155802862,
        "ENV_A_avg_homoatomic_dist_by_shortest_dist": 1.1971383147853736,
        "ENV_B_avg_homoatomic_dist_by_shortest_dist": 1.095572948514125,
        "ENV_A_count_at_A_shortest_dist": 0,
        "ENV_A_count_at_B_shortest_dist": 1,
        "ENV_A_avg_count_at_A_shortest_dist": 0.0,
        "ENV_A_avg_count_at_B_shortest_dist": 1.0,
        "ENV_B_count_at_A_shortest_dist": 1,
        "ENV_B_count_at_B_shortest_dist": 0,
        "ENV_B_avg_count_at_A_shortest_dist": 1.0,
        "ENV_B_avg_count_at_B_shortest_dist": 0.0,
    }

    for key in result:
        assert result[key] == pytest.approx(expected[key], abs=0.005)
