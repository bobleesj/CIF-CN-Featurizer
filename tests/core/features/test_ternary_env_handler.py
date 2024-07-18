# import pytest
# from core.features.ternary_env_handler import (
#     compute_ternary_env_features,
# )


# # @pytest.mark.now
# # def test_compute_ternary_env_features(URhIn_cif):
# #     R = "U"
# #     M = "Rh"
# #     X = "In"
# #     result = compute_ternary_env_features(URhIn_cif.connections, R, M, X)
# #     expected = {
# #         "R_shortest_dist_count": 3,
# #         "M_shortest_dist_count": 6,
# #         "X_shortest_dist_count": 2,
# #         "R_avg_shortest_dist_count": 3.0,
# #         "M_avg_shortest_dist_count": 4.0,
# #         "X_avg_shortest_dist_count": 2.0,
# #         "R_shortest_tol_dist_count": 5,
# #         "M_shortest_tol_dist_count": 6,
# #         "X_shortest_tol_dist_count": 2,
# #         "R_avg_shortest_dist_within_tol_count": 5.0,
# #         "M_avg_shortest_dist_within_tol_count": 7.5,
# #         "X_avg_shortest_dist_within_tol_count": 2.0,
# #         "R_second_by_first_shortest_dist": 1.000335232986926,
# #         "M_second_by_first_shortest_dist": 1.1296296296296295,
# #         "X_second_by_first_shortest_dist": 1.0555555555555556,
# #         "R_avg_second_by_first_shortest_dist": 1.000335232986926,
# #         "M_avg_second_by_first_shortest_dist": 1.0648768357756606,
# #         "X_avg_second_by_first_shortest_dist": 1.0555555555555556,
# #         "R_second_shortest_dist_count": 1,
# #         "M_second_shortest_dist_count": 4,
# #         "X_second_shortest_dist_count": 2,
# #         "R_avg_second_shortest_dist_count": 1.0,
# #         "M_avg_second_shortest_dist_count": 2.0,
# #         "X_avg_second_shortest_dist_count": 2.0,
# #         "R_homoatomic_dist_by_shortest_dist": 1.3023489932885906,
# #         "M_homoatomic_dist_by_shortest_dist": 1.4374074074074072,
# #         "X_homoatomic_dist_by_shortest_dist": 1.201359259259259,
# #         "R_avg_homoatomic_dist_by_shortest_dist": 1.3023489932885906,
# #         "M_avg_homoatomic_dist_by_shortest_dist": 1.3995808966861598,
# #         "X_avg_homoatomic_dist_by_shortest_dist": 1.201359259259259,
# #         "R_count_at_R_shortest_dist": 0,
# #         "R_count_at_M_shortest_dist": 0,
# #         "R_count_at_X_shortest_dist": 0,
# #         "R_avg_count_at_R_shortest_dist": 0.0,
# #         "R_avg_count_at_M_shortest_dist": 0.0,
# #         "R_avg_count_at_X_shortest_dist": 0.0,
# #         "M_count_at_R_shortest_dist": 4,
# #         "M_count_at_M_shortest_dist": 0,
# #         "M_count_at_X_shortest_dist": 2,
# #         "M_avg_count_at_R_shortest_dist": 4.0,
# #         "M_avg_count_at_M_shortest_dist": 0.0,
# #         "M_avg_count_at_X_shortest_dist": 2.0,
# #         "X_count_at_R_shortest_dist": 0,
# #         "X_count_at_M_shortest_dist": 6,
# #         "X_count_at_X_shortest_dist": 0,
# #         "X_avg_count_at_R_shortest_dist": 0.0,
# #         "X_avg_count_at_M_shortest_dist": 4.5,
# #         "X_avg_count_at_X_shortest_dist": 0.0,
# #     }

# #     for key in result:
# #         assert result[key] == pytest.approx(
# #             expected[key], abs=0.005
# #         ), f"Failed for {key}: expected {expected[key]}, got {result[key]}"
