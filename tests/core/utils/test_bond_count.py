import pytest
from core.utils.bond_count import (
    compute_count_first_second_min_dist,
    extract_best_labels,
    extract_shortest_dist_with_tol,
    extract_avg_shortest_dist_with_tol,
    get_avg_second_by_first_shortest_dist_ratio,
)


@pytest.fixture(scope="function")
def Th7Rh3_site_dist_info():
    return {
        "Rh1": {
            "shortest_dist": 2.869,
            "second_shortest_dist": 2.95,
            "counts": {2.869: 2, 2.95: 1},
        },
        "Th1": {
            "shortest_dist": 2.965,
            "second_shortest_dist": 3.496,
            "counts": {2.965: 2, 3.496: 2},
        },
        "Th2": {
            "shortest_dist": 2.869,
            "second_shortest_dist": 2.95,
            "counts": {2.869: 2, 2.95: 1},
        },
        "Th3": {
            "shortest_dist": 3.019,
            "second_shortest_dist": 3.643,
            "counts": {3.019: 3, 3.643: 3},
        },
    }


@pytest.fixture(scope="function")
def binary_531015_cif_site_dist_info():
    return {
        "Sb1": {
            "shortest_dist": 3.332,
            "second_shortest_dist": 3.847,
            "counts": {3.332: 8, 3.847: 6},
        },
        "Th1": {
            "shortest_dist": 3.332,
            "second_shortest_dist": 3.847,
            "counts": {3.332: 8, 3.847: 6},
        },
    }


def test_find_shortest_distances_binary_ThSb(binary_531015_cif, binary_531015_cif_site_dist_info):
    result = compute_count_first_second_min_dist(binary_531015_cif.connections)
    print(result)
    assert result == binary_531015_cif_site_dist_info


def test_find_shortest_distances_binary_Th7Rh3(Th7Rh3_cif, Th7Rh3_site_dist_info):
    result = compute_count_first_second_min_dist(Th7Rh3_cif.connections)
    assert result == Th7Rh3_site_dist_info


def test_extract_best_labels_Th7Rh3(Th7Rh3_site_dist_info):
    result = extract_best_labels(Th7Rh3_site_dist_info)

    assert result == {
        "Rh": {
            "label_count": 1,
            "shortest_dist_total_count": 2,
            "second_shortest_dist_count": 1,
            "avg_shortest_dist": 2.0,
            "avg_second_shortest_dist_count": 1.0,
            "best_label": "Rh1",
            "details": {
                "shortest_dist": 2.869,
                "second_shortest_dist": 2.95,
                "counts": {2.869: 2, 2.95: 1},
            },
        },
        "Th": {
            "label_count": 3,
            "shortest_dist_total_count": 7,
            "second_shortest_dist_count": 6,
            "avg_shortest_dist": 2.3333333333333335,
            "avg_second_shortest_dist_count": 2.0,
            "best_label": "Th2",
            "details": {
                "shortest_dist": 2.869,
                "second_shortest_dist": 2.95,
                "counts": {2.869: 2, 2.95: 1},
            },
        },
    }


def test_extract_best_labels_531015(
    binary_531015_cif_site_dist_info,
):
    result = extract_best_labels(binary_531015_cif_site_dist_info)
    assert result == {
        "Sb": {
            "label_count": 1,
            "shortest_dist_total_count": 8,
            "second_shortest_dist_count": 6,
            "avg_shortest_dist": 8.0,
            "avg_second_shortest_dist_count": 6.0,
            "best_label": "Sb1",
            "details": {
                "shortest_dist": 3.332,
                "second_shortest_dist": 3.847,
                "counts": {3.332: 8, 3.847: 6},
            },
        },
        "Th": {
            "label_count": 1,
            "shortest_dist_total_count": 8,
            "second_shortest_dist_count": 6,
            "avg_shortest_dist": 8.0,
            "avg_second_shortest_dist_count": 6.0,
            "best_label": "Th1",
            "details": {
                "shortest_dist": 3.332,
                "second_shortest_dist": 3.847,
                "counts": {3.332: 8, 3.847: 6},
            },
        },
    }


def test_extract_shortest_dist_with_tol(binary_531015_cif, binary_531015_cif_site_dist_info):
    best_label_dist_info = extract_best_labels(binary_531015_cif_site_dist_info)
    result = extract_shortest_dist_with_tol(best_label_dist_info, binary_531015_cif.connections)

    assert result == {
        "Sb": {"shortest_dist_count_within_tol": 8},
        "Th": {"shortest_dist_count_within_tol": 8},
    }


@pytest.mark.fast
def test_extract_avg_shortest_dist_with_tol(Th7Rh3_cif):
    result = extract_avg_shortest_dist_with_tol(Th7Rh3_cif.connections)

    assert result == {
        "Rh": {
            "total_shortest_dist_within_tol_count": 5,
            "avg_shortest_dist_within_tol_count": 5.0,
        },
        "Th": {
            "total_shortest_dist_within_tol_count": 8,
            "avg_shortest_dist_within_tol_count": 2.6666666666666665,
        },
    }


@pytest.mark.fast
def test_extract_avg_shortest_dist_with_tol(binary_531015_cif):
    result = extract_avg_shortest_dist_with_tol(binary_531015_cif.connections)
    assert result == {
        "Sb": {
            "total_shortest_dist_within_tol_count": 8,
            "avg_shortest_dist_within_tol_count": 8.0,
        },
        "Th": {
            "total_shortest_dist_within_tol_count": 8,
            "avg_shortest_dist_within_tol_count": 8.0,
        },
    }


@pytest.mark.fast
def test_get_first_by_second_shortest_dist_ratio(binary_531015_cif_site_dist_info, binary_531015_cif):
    result = get_avg_second_by_first_shortest_dist_ratio(
        binary_531015_cif_site_dist_info, binary_531015_cif.connections
    )

    assert result == {
        "Sb": {"avg_second_by_first_shortest_dist": 1.154561824729892},
        "Th": {"avg_second_by_first_shortest_dist": 1.154561824729892},
    }


@pytest.mark.fast
def test_get_first_by_second_shortest_dist_ratio(Th7Rh3_site_dist_info, Th7Rh3_cif):
    result = get_avg_second_by_first_shortest_dist_ratio(Th7Rh3_site_dist_info, Th7Rh3_cif.connections)

    assert result == {
        "Rh": {"avg_second_by_first_shortest_dist": 1.028232833739979},
        "Th": {"avg_second_by_first_shortest_dist": 1.1380043890215203},
    }
