import pytest
from core.features.coordination import (
    get_CN_metrices_per_method,
    compute_min_max_avg_per_label,
    compute_number_of_atoms_in_binary_CN,
    compute_global_averages_for_min_max_avg_metrices,
)

from core.utils.element_parser import get_binary_AB_elements


@pytest.fixture(scope="function")
def RhSb2_CN_metrices_per_method():
    return {
        "SbI": {
            "dist_by_shortest_dist": {
                "volume_of_polyhedron": 7.841,
                "distance_from_avg_point_to_center": 0.329,
                "number_of_vertices": 4,
                "number_of_edges": 6,
                "number_of_faces": 4,
                "shortest_distance_to_face": 0.69,
                "shortest_distance_to_edge": 1.078,
                "volume_of_inscribed_sphere": 1.374,
                "packing_efficiency": 0.175,
            },
            "dist_by_CIF_radius_sum": {
                "volume_of_polyhedron": 7.841,
                "distance_from_avg_point_to_center": 0.329,
                "number_of_vertices": 4,
                "number_of_edges": 6,
                "number_of_faces": 4,
                "shortest_distance_to_face": 0.69,
                "shortest_distance_to_edge": 1.078,
                "volume_of_inscribed_sphere": 1.374,
                "packing_efficiency": 0.175,
            },
            "dist_by_CIF_radius_refined_sum": {
                "volume_of_polyhedron": 7.841,
                "distance_from_avg_point_to_center": 0.329,
                "number_of_vertices": 4,
                "number_of_edges": 6,
                "number_of_faces": 4,
                "shortest_distance_to_face": 0.69,
                "shortest_distance_to_edge": 1.078,
                "volume_of_inscribed_sphere": 1.374,
                "packing_efficiency": 0.175,
            },
            "dist_by_Pauling_radius_sum": {
                "volume_of_polyhedron": 93.866,
                "distance_from_avg_point_to_center": 0.48,
                "number_of_vertices": 14,
                "number_of_edges": 33,
                "number_of_faces": 22,
                "shortest_distance_to_face": 2.127,
                "shortest_distance_to_edge": 2.146,
                "volume_of_inscribed_sphere": 40.295,
                "packing_efficiency": 0.429,
            },
        },
        "Rh": {
            "dist_by_shortest_dist": {
                "volume_of_polyhedron": 28.667,
                "distance_from_avg_point_to_center": 0.268,
                "number_of_vertices": 7,
                "number_of_edges": 15,
                "number_of_faces": 10,
                "shortest_distance_to_face": 1.509,
                "shortest_distance_to_edge": 1.749,
                "volume_of_inscribed_sphere": 14.39,
                "packing_efficiency": 0.502,
            },
            "dist_by_CIF_radius_sum": {
                "volume_of_polyhedron": 28.667,
                "distance_from_avg_point_to_center": 0.268,
                "number_of_vertices": 7,
                "number_of_edges": 15,
                "number_of_faces": 10,
                "shortest_distance_to_face": 1.509,
                "shortest_distance_to_edge": 1.749,
                "volume_of_inscribed_sphere": 14.39,
                "packing_efficiency": 0.502,
            },
            "dist_by_CIF_radius_refined_sum": {
                "volume_of_polyhedron": 28.667,
                "distance_from_avg_point_to_center": 0.268,
                "number_of_vertices": 7,
                "number_of_edges": 15,
                "number_of_faces": 10,
                "shortest_distance_to_face": 1.509,
                "shortest_distance_to_edge": 1.749,
                "volume_of_inscribed_sphere": 14.39,
                "packing_efficiency": 0.502,
            },
            "dist_by_Pauling_radius_sum": {
                "volume_of_polyhedron": 28.667,
                "distance_from_avg_point_to_center": 0.268,
                "number_of_vertices": 7,
                "number_of_edges": 15,
                "number_of_faces": 10,
                "shortest_distance_to_face": 1.509,
                "shortest_distance_to_edge": 1.749,
                "volume_of_inscribed_sphere": 14.39,
                "packing_efficiency": 0.502,
            },
        },
        "SbII": {
            "dist_by_shortest_dist": {
                "volume_of_polyhedron": 9.762,
                "distance_from_avg_point_to_center": 0.284,
                "number_of_vertices": 4,
                "number_of_edges": 6,
                "number_of_faces": 4,
                "shortest_distance_to_face": 0.733,
                "shortest_distance_to_edge": 1.257,
                "volume_of_inscribed_sphere": 1.65,
                "packing_efficiency": 0.169,
            },
            "dist_by_CIF_radius_sum": {
                "volume_of_polyhedron": 9.762,
                "distance_from_avg_point_to_center": 0.284,
                "number_of_vertices": 4,
                "number_of_edges": 6,
                "number_of_faces": 4,
                "shortest_distance_to_face": 0.733,
                "shortest_distance_to_edge": 1.257,
                "volume_of_inscribed_sphere": 1.65,
                "packing_efficiency": 0.169,
            },
            "dist_by_CIF_radius_refined_sum": {
                "volume_of_polyhedron": 9.762,
                "distance_from_avg_point_to_center": 0.284,
                "number_of_vertices": 4,
                "number_of_edges": 6,
                "number_of_faces": 4,
                "shortest_distance_to_face": 0.733,
                "shortest_distance_to_edge": 1.257,
                "volume_of_inscribed_sphere": 1.65,
                "packing_efficiency": 0.169,
            },
            "dist_by_Pauling_radius_sum": {
                "volume_of_polyhedron": 107.745,
                "distance_from_avg_point_to_center": 0.419,
                "number_of_vertices": 15,
                "number_of_edges": 36,
                "number_of_faces": 24,
                "shortest_distance_to_face": 2.391,
                "shortest_distance_to_edge": 2.179,
                "volume_of_inscribed_sphere": 57.222,
                "packing_efficiency": 0.531,
            },
        },
    }


@pytest.fixture(scope="function")
def RhSb2_min_max_avg_CN_metrices_from_sites():
    return {
        "SbI": {
            "volume_of_polyhedron": {
                "min": 7.841,
                "max": 93.866,
                "avg": 29.34725,
            },
            "distance_from_avg_point_to_center": {
                "min": 0.329,
                "max": 0.48,
                "avg": 0.36675,
            },
            "number_of_vertices": {"min": 4, "max": 14, "avg": 6.5},
            "number_of_edges": {"min": 6, "max": 33, "avg": 12.75},
            "number_of_faces": {"min": 4, "max": 22, "avg": 8.5},
            "shortest_distance_to_face": {
                "min": 0.69,
                "max": 2.127,
                "avg": 1.0492499999999998,
            },
            "shortest_distance_to_edge": {
                "min": 1.078,
                "max": 2.146,
                "avg": 1.345,
            },
            "volume_of_inscribed_sphere": {
                "min": 1.374,
                "max": 40.295,
                "avg": 11.10425,
            },
            "packing_efficiency": {"min": 0.175, "max": 0.429, "avg": 0.2385},
        },
        "Rh": {
            "volume_of_polyhedron": {
                "min": 28.667,
                "max": 28.667,
                "avg": 28.667,
            },
            "distance_from_avg_point_to_center": {
                "min": 0.268,
                "max": 0.268,
                "avg": 0.268,
            },
            "number_of_vertices": {"min": 7, "max": 7, "avg": 7.0},
            "number_of_edges": {"min": 15, "max": 15, "avg": 15.0},
            "number_of_faces": {"min": 10, "max": 10, "avg": 10.0},
            "shortest_distance_to_face": {
                "min": 1.509,
                "max": 1.509,
                "avg": 1.509,
            },
            "shortest_distance_to_edge": {
                "min": 1.749,
                "max": 1.749,
                "avg": 1.749,
            },
            "volume_of_inscribed_sphere": {
                "min": 14.39,
                "max": 14.39,
                "avg": 14.39,
            },
            "packing_efficiency": {"min": 0.502, "max": 0.502, "avg": 0.502},
        },
        "SbII": {
            "volume_of_polyhedron": {
                "min": 9.762,
                "max": 107.745,
                "avg": 34.25775,
            },
            "distance_from_avg_point_to_center": {
                "min": 0.284,
                "max": 0.419,
                "avg": 0.31775,
            },
            "number_of_vertices": {"min": 4, "max": 15, "avg": 6.75},
            "number_of_edges": {"min": 6, "max": 36, "avg": 13.5},
            "number_of_faces": {"min": 4, "max": 24, "avg": 9.0},
            "shortest_distance_to_face": {
                "min": 0.733,
                "max": 2.391,
                "avg": 1.1475,
            },
            "shortest_distance_to_edge": {
                "min": 1.257,
                "max": 2.179,
                "avg": 1.4874999999999998,
            },
            "volume_of_inscribed_sphere": {
                "min": 1.65,
                "max": 57.222,
                "avg": 15.543000000000001,
            },
            "packing_efficiency": {"min": 0.169, "max": 0.531, "avg": 0.2595},
        },
    }


@pytest.mark.now
def test_find_min_max_avg_CN_metrices(RhSb2_CN_metrices_per_method, RhSb2_min_max_avg_CN_metrices_from_sites):
    """
    Compute the min, max, and avg of the CN metrices from each site label across 4 methods
    """
    result = compute_min_max_avg_per_label(RhSb2_CN_metrices_per_method)
    for label in RhSb2_min_max_avg_CN_metrices_from_sites:
        for key, metric in RhSb2_min_max_avg_CN_metrices_from_sites[label].items():
            assert result[label][key]["min"] == pytest.approx(
                metric["min"], abs=0.005
            ), f"{label}-{key} min is incorrect"
            assert result[label][key]["max"] == pytest.approx(
                metric["max"], abs=0.005
            ), f"{label}-{key} max is incorrect"
            assert result[label][key]["avg"] == pytest.approx(
                metric["avg"], abs=0.005
            ), f"{label}-{key} avg is incorrect"


@pytest.mark.now
def test_compute_global_averages(RhSb2_min_max_avg_CN_metrices_from_sites):
    result = compute_global_averages_for_min_max_avg_metrices(RhSb2_min_max_avg_CN_metrices_from_sites)
    expected = {
        "min": {
            "volume_of_polyhedron": 15.423333333333334,
            "distance_from_avg_point_to_center": 0.2936666666666667,
            "number_of_vertices": 5.0,
            "number_of_edges": 9.0,
            "number_of_faces": 6.0,
            "shortest_distance_to_face": 0.9773333333333333,
            "shortest_distance_to_edge": 1.3613333333333333,
            "volume_of_inscribed_sphere": 5.804666666666667,
            "packing_efficiency": 0.28200000000000003,
        },
        "max": {
            "volume_of_polyhedron": 76.75933333333334,
            "distance_from_avg_point_to_center": 0.389,
            "number_of_vertices": 12.0,
            "number_of_edges": 28.0,
            "number_of_faces": 18.666666666666668,
            "shortest_distance_to_face": 2.009,
            "shortest_distance_to_edge": 2.0246666666666666,
            "volume_of_inscribed_sphere": 37.30233333333334,
            "packing_efficiency": 0.4873333333333334,
        },
        "avg": {
            "volume_of_polyhedron": 30.757333333333335,
            "distance_from_avg_point_to_center": 0.3175,
            "number_of_vertices": 6.75,
            "number_of_edges": 13.75,
            "number_of_faces": 9.166666666666666,
            "shortest_distance_to_face": 1.23525,
            "shortest_distance_to_edge": 1.5271666666666668,
            "volume_of_inscribed_sphere": 13.679083333333333,
            "packing_efficiency": 0.3333333333333333,
        },
    }
    # Loop through each category (min, max, avg) and each metric
    for category in ["min", "max", "avg"]:
        for metric, value in expected[category].items():
            assert result[category][metric] == pytest.approx(value, abs=0.005)


@pytest.mark.now
def test_compute_number_of_atoms_in_CN(RhSb2_cif):
    CN_data = get_CN_metrices_per_method(RhSb2_cif)
    A, B = get_binary_AB_elements(list(RhSb2_cif.unique_elements))
    result = compute_number_of_atoms_in_binary_CN(RhSb2_cif.connections, CN_data, A, B)
    assert result == {
        "SbI": {
            "dist_by_shortest_dist": {"A_count": 3, "B_count": 1},
            "dist_by_CIF_radius_sum": {"A_count": 3, "B_count": 1},
            "dist_by_CIF_radius_refined_sum": {"A_count": 3, "B_count": 1},
            "dist_by_Pauling_radius_sum": {"A_count": 3, "B_count": 11},
        },
        "Rh": {
            "dist_by_shortest_dist": {"A_count": 1, "B_count": 6},
            "dist_by_CIF_radius_sum": {"A_count": 1, "B_count": 6},
            "dist_by_CIF_radius_refined_sum": {"A_count": 1, "B_count": 6},
            "dist_by_Pauling_radius_sum": {"A_count": 1, "B_count": 6},
        },
        "SbII": {
            "dist_by_shortest_dist": {"A_count": 3, "B_count": 1},
            "dist_by_CIF_radius_sum": {"A_count": 3, "B_count": 1},
            "dist_by_CIF_radius_refined_sum": {"A_count": 3, "B_count": 1},
            "dist_by_Pauling_radius_sum": {"A_count": 3, "B_count": 12},
        },
    }
    min_max_avg_result = compute_min_max_avg_per_label(result)
    assert min_max_avg_result == {
        "SbI": {
            "A_count": {"min": 3, "max": 3, "avg": 3.0},
            "B_count": {"min": 1, "max": 11, "avg": 3.5},
        },
        "Rh": {
            "A_count": {"min": 1, "max": 1, "avg": 1.0},
            "B_count": {"min": 6, "max": 6, "avg": 6.0},
        },
        "SbII": {
            "A_count": {"min": 3, "max": 3, "avg": 3.0},
            "B_count": {"min": 1, "max": 12, "avg": 3.75},
        },
    }


@pytest.mark.now
def test_compute_global_average_for_atom_count_in_CN():
    min_max_avg_result = {
        "SbI": {
            "A_count": {"min": 3, "max": 3, "avg": 3.0},
            "B_count": {"min": 1, "max": 11, "avg": 3.5},
        },
        "Rh": {
            "A_count": {"min": 1, "max": 1, "avg": 1.0},
            "B_count": {"min": 6, "max": 6, "avg": 6.0},
        },
        "SbII": {
            "A_count": {"min": 3, "max": 3, "avg": 3.0},
            "B_count": {"min": 1, "max": 12, "avg": 3.75},
        },
    }

    result = compute_global_averages_for_min_max_avg_metrices(min_max_avg_result)

    expected = {
        "min": {"A_count": 2.3333333333333335, "B_count": 2.6666666666666665},
        "max": {"A_count": 2.3333333333333335, "B_count": 9.666666666666666},
        "avg": {"A_count": 2.3333333333333335, "B_count": 4.416666666666667},
    }

    for category in ["min", "max", "avg"]:
        for metric, value in expected[category].items():
            assert result[category][metric] == pytest.approx(value, abs=0.005)
