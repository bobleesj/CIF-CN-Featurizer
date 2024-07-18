def print_dict_pretty(data, name):
    """
    Prints the contents of a dictionary in a pretty format.
    """
    print(f"\nPrint from {name}:")
    for i, (key, value) in enumerate(data.items(), start=1):
        print(f"{i}. {key}: {value}")
    print()


def print_connected_points(connection_data):
    """
    Utility function for printing connections per site label
    """
    for label, connections in connection_data.items():
        print(f"\nAtom site {label}:")
        for (
            label,
            dist,
            coords_1,
            coords_2,
        ) in connections[:10]:
            print(f"{label} {dist} {coords_1}, {coords_2}")
