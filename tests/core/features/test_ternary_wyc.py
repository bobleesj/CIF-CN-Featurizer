# import pytest
# from cifkit import Cif
# from core.utils.element_parser import get_ternary_RMX_elements
# from core.features.ternary_wyc import (
#     compute_ternary_env_features,
# )


# @pytest.mark.now
# def test_compute_ternary_wyc_features():
#     cif = Cif("tests/cif/ternary/URhIn.cif")
#     elements = list(cif.unique_elements)
#     R, M, X = get_ternary_RMX_elements(elements)
#     result = compute_ternary_env_features(cif._loop_values, R, M, X)

#     assert result == {
#         "lowest_wyckoff_elements": "Rh",
#         "R_lowest_wyckoff_label": 3,
#         "M_lowest_wyckoff_label": 1,
#         "X_lowest_wyckoff_label": 3,
#         "identical_lowest_wyckoff_count": 1,
#         "R_sites_total": 1,
#         "M_sites_total": 2,
#         "X_sites_total": 1,
#         "R_multiplicity_total": 3,
#         "M_multiplicity_total": 3,
#         "X_multiplicity_total": 3,
#     }
