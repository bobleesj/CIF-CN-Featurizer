def get_shortest_bond_distances_by_AB(
    shortest_bond_pair_distance: dict[str, float],
    A: str,
    B: str,
) -> dict[str, float]:
    """
    Get sorted bond distances by AB pair
    """
    for (
        elem1,
        elem2,
    ), distance in shortest_bond_pair_distance.items():
        if elem1 == elem2 == A:
            distAA = distance
        elif elem1 == elem2 == B:
            distBB = distance
        elif (elem1 == A and elem2 == B) or (elem1 == B and elem2 == A):
            distAB = distance

    shortest_distances_pair = {
        "AA": distAA,
        "BB": distBB,
        "AB": distAB,
    }
    return shortest_distances_pair


def get_AA_BB_AB_dists(shortest_distances_pair: dict[str, float]) -> tuple[float, float, float]:
    distAA = shortest_distances_pair["AA"]
    distBB = shortest_distances_pair["BB"]
    distAB = shortest_distances_pair["AB"]
    return distAA, distBB, distAB


def get_shortest_bond_distances_by_RMX(
    shortest_bond_pair_distance: dict[str, float],
    R: str,
    M: str,
    X: str,
) -> dict[str, float]:
    """
    Get sorted bond distances by AB pair
    """
    for (
        elem1,
        elem2,
    ), distance in shortest_bond_pair_distance.items():
        if elem1 == elem2 == R:
            distRR = distance
        elif elem1 == elem2 == M:
            distMM = distance
        elif elem1 == elem2 == X:
            distXX = distance
        elif (elem1 == R and elem2 == M) or (elem1 == M and elem2 == R):
            distRM = distance
        elif (elem1 == R and elem2 == X) or (elem1 == X and elem2 == R):
            distRX = distance
        elif (elem1 == M and elem2 == X) or (elem1 == X and elem2 == M):
            distMX = distance

    shortest_distances_pair = {
        "RR": distRR,
        "MM": distMM,
        "XX": distXX,
        "RM": distRM,
        "RX": distRX,
        "MX": distMX,
    }
    return shortest_distances_pair


def get_RR_MM_XX_RM_RX_MX_dists(shortest_distances_pair: dict[str, float]) -> tuple[float, float, float]:
    distRR = shortest_distances_pair["RR"]
    distBB = shortest_distances_pair["MM"]
    distXX = shortest_distances_pair["XX"]
    distRM = shortest_distances_pair["RM"]
    distRX = shortest_distances_pair["RX"]
    distMX = shortest_distances_pair["MX"]
    return distRR, distBB, distXX, distRM, distRX, distMX
