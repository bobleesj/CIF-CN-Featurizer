import core.preprocess.cif_parser as cif_parser
import core.preprocess.supercell as supercell


def get_CIF_info(file_path, loop_tags, supercell_generation_method=3):
    """
    Parse the CIF data from the given file path.
    """
    cif_block = cif_parser.get_cif_block(file_path)
    cell_lengths, cell_angles_rad = cif_parser.get_cell_lenghts_angles_rad(cif_block)
    cif_loop_values = cif_parser.get_loop_values(cif_block, loop_tags)
    all_coords_list = supercell.get_coords_list(cif_block, cif_loop_values)
    (
        all_points,
        unique_labels,
        atom_site_list,
    ) = supercell.get_points_and_labels(
        all_coords_list, cif_loop_values, supercell_generation_method
    )

    return (
        cif_block,
        cell_lengths,
        cell_angles_rad,
        all_coords_list,
        all_points,
        unique_labels,
        atom_site_list,
    )


def read_and_prepare_cif_data(filename):
    loop_tags = cif_parser.get_loop_tags()
    cif_block = cif_parser.get_cif_block(filename)
    cif_id = cif_block.name
    cell_lengths, cell_angles_rad = supercell.process_cell_data(cif_block)
    cif_loop_values = cif_parser.get_loop_values(cif_block, loop_tags)
    all_coords_list = supercell.get_coords_list(cif_block, cif_loop_values)

    return (
        cif_id,
        cif_block,
        cell_lengths,
        cell_angles_rad,
        cif_loop_values,
        all_coords_list,
    )
