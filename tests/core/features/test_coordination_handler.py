import pytest
from core.features.coordination_handler import get_CN_binary_features


@pytest.mark.now
def test_get_CN_binary_features(RhSb2_cif):
    result = get_CN_binary_features(RhSb2_cif)
    expected = {
        "CN_AVG_coordination_number": 6.75,
        "CN_AVG_A_atom_count": 2.3333333333333335,
        "CN_AVG_B_atom_count": 4.416666666666667,
        "CN_AVG_polyhedron_volume": 30.756333333333334,
        "CN_AVG_central_atom_to_center_of_mass_dist": 0.31716666666666665,
        "CN_AVG_number_of_edges": 13.75,
        "CN_AVG_number_of_faces": 9.166666666666666,
        "CN_AVG_shortest_distance_to_face": 1.2349166666666667,
        "CN_AVG_shortest_distance_to_edge": 1.5271666666666668,
        "CN_AVG_volume_of_inscribed_sphere": 13.672416666666665,
        "CN_AVG_packing_efficiency": 0.333,
        "CN_MIN_coordination_number": 5.0,
        "CN_MIN_A_atom_count": 2.3333333333333335,
        "CN_MIN_B_atom_count": 2.6666666666666665,
        "CN_MIN_polyhedron_volume": 15.422333333333334,
        "CN_MIN_central_atom_to_center_of_mass_dist": 0.2933333333333334,
        "CN_MIN_number_of_edges": 9.0,
        "CN_MIN_number_of_faces": 6.0,
        "CN_MIN_shortest_distance_to_face": 0.977,
        "CN_MIN_shortest_distance_to_edge": 1.3613333333333333,
        "CN_MIN_volume_of_inscribed_sphere": 5.797999999999999,
        "CN_MIN_packing_efficiency": 0.2816666666666667,
        "CN_MAX_coordination_number": 5.0,
        "CN_MAX_A_atom_count": 2.3333333333333335,
        "CN_MAX_B_atom_count": 9.666666666666666,
        "CN_MAX_polyhedron_volume": 76.75833333333334,
        "CN_MAX_central_atom_to_center_of_mass_dist": 0.38866666666666666,
        "CN_MAX_number_of_edges": 28.0,
        "CN_MAX_number_of_faces": 18.666666666666668,
        "CN_MAX_shortest_distance_to_face": 2.0086666666666666,
        "CN_MAX_shortest_distance_to_edge": 2.0246666666666666,
        "CN_MAX_volume_of_inscribed_sphere": 37.29566666666667,
        "CN_MAX_packing_efficiency": 0.48699999999999993,
    }
    print(result)

    for key in result:
        assert result[key] == pytest.approx(expected[key], abs=0.01)
