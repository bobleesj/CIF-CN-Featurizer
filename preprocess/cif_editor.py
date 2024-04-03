import re
from preprocess import cif_parser


def preprocess_cif_file_on_label_element(file_path):
    is_cif_file_updated = False

    cif_block = cif_parser.get_cif_block(file_path)
    cif_loop_values = cif_parser.get_loop_values(
        cif_block, cif_parser.get_loop_tags()
    )
    num_element_labels = len(cif_loop_values[0])
    (
        _,
        compound_formula,
        _,
        _,
    ) = cif_parser.get_compound_phase_tag_id_from_third_line(file_path)

    # Get lines in _atom_site_occupancy only
    modified_lines = []
    content_lines = cif_parser.get_loop_content(
        file_path, "_atom_site_occupancy"
    )

    if content_lines is None:
        raise RuntimeError("Could not find atom site loop.")

    if num_element_labels < 2:
        raise RuntimeError("Wrong number of values in the loop")

    for line in content_lines:
        line = line.strip()
        site_label, atom_type_symbol = line.split()[:2]
        atom_type_from_label = cif_parser.get_atom_type(site_label)

        """
        Type 8.
        Ex) 1817279.cif
        In1,Co3B Co 4 c 0.75 0.25 0.59339 0.07(3)
        -> Co13B Co 4 c 0.75 0.25 0.59339 0.07(3)
        """

        # Check whether it has a comma
        if "," in site_label:
            site_label_original = site_label
            # Get 'Er1In3B'
            site_label = site_label.replace(",", "").split(" ")[0]

            # Get ['Er', 'Co', 'In']
            elements = re.findall("[A-Z][a-z]*", compound_formula)

            # Filter out labels containing elements from compound_formula
            # Er1In3B is filtered to 13B
            for element in elements:
                if element in site_label:
                    site_label = site_label.replace(element, "")

            # Combine stripped_site_label with element
            modified_label = atom_type_symbol + site_label

            line = line.replace(site_label_original, modified_label)
            is_cif_file_updated = True

        """
        Type 9.
        Ex) 1200981
        Snb Sn 4 c 0.0595 0.25 0.0952 1
        -> SnB Sn 4 c 0.0595 0.25 0.0952 1
        """

        # Check 3 letter, all of them are alphabets

        if (
            len(site_label) == 3
            and site_label[0].isalpha()
            and site_label[1].isalpha()
            and site_label[2].isalpha()
        ):
            # Uppercase the last character
            modified_label = (
                site_label[0] + site_label[1] + site_label[2].upper()
            )

            # Modify the label
            line = line.replace(site_label, modified_label)  # Modify the line
            is_cif_file_updated = True

        if atom_type_symbol != atom_type_from_label:
            # print("atom_type_label", atom_type_label)
            # print("atom_type_symbol", atom_type_symbol)
            # print("atom_type_from_label", atom_type_from_label)

            """
            Type 1.
            Ex) test/format_label_cif_files/symbolic_atom_label_type_1/250165.cif
            M1 Th 4 a 0 0 0 0.99 -> Th1 Th 4 a 0 0 0 0.99
            """
            if (
                len(site_label) == 2
                and site_label[-1].isdigit()
                and site_label[-2].isalpha()
            ):
                # Get the new label Ex) M1 -> Ge1
                new_label = site_label.replace(
                    atom_type_from_label, atom_type_symbol
                )
                line = line.replace(site_label, new_label)  # Modify the line
                is_cif_file_updated = True

            """
            Type 2.
            Ex) 312084.cif
            M1A Ge 8 h 0 0.06 0.163 0.500 -> Ge1A Ge 8 h 0 0.06 0.163 0.50
            """

            if (
                len(site_label) == 3
                and site_label[-1].isalpha()
                and site_label[-2].isdigit()
                and site_label[-3].isalpha()
            ):
                new_label = site_label.replace(
                    atom_type_from_label, atom_type_symbol
                )
                line = line.replace(site_label, new_label)  # Modify the line
                is_cif_file_updated = True

            """
            Type 3.
            Ex)1603834.cif
            R Nd 2 a 0 0 0 1 -> Nd Nd 2 a 0 0 0 1
            """

            if len(site_label) == 1 and site_label[-1].isalpha():
                new_label = site_label.replace(
                    atom_type_from_label, atom_type_symbol
                )
                line = line.replace(site_label, new_label)
                is_cif_file_updated = True

            """
            Type 4.
            Ex) 1711694.cif
            Ln Gd 2 a 0 0 0.0 1 -> Gd Gd 2 a 0 0 0.0 1
            """
            if (
                len(site_label) == 2
                and site_label[-1].isalpha()
                and site_label[-2].isalpha()
            ):
                if site_label.lower() not in atom_type_symbol.lower():
                    # print(atom_type_label.lower(), atom_type_symbol.lower())
                    # Do not use get_atom_type since replace the entire label
                    new_label = site_label.replace(
                        site_label, atom_type_symbol
                    )
                    line = line.replace(site_label, new_label)
                    is_cif_file_updated = True

            """
            Type 5. 
            Ex) 1049941.cif
            PR1 Pr 4 j 0.02076 0.5 0.30929 1 -> Pr1 Pr 4 j 0.02076 0.5 0.30929 1
            """

            if (
                len(site_label) == 3
                and site_label[0].isalpha()
                and site_label[1].isalpha()
                and site_label[2].isdigit()
            ):
                first_two_label_characters = site_label[0] + site_label[1]
                if (
                    first_two_label_characters.lower()
                    == atom_type_symbol.lower()
                ):
                    modified_label = (
                        site_label[0] + site_label[1].lower() + site_label[2]
                    )
                    line = line.replace(site_label, modified_label)
                    is_cif_file_updated = True

            """
            Type 6.

            Ex) 1049941.cif
            NG1A Ni 4 j 0 0.172 0.5 0.88(1) -> Ni1A Ni 4 j 0 0.172 0.5 0.88(1)
            """
            if (
                len(site_label) == 4
                and site_label[0].isalpha()
                and site_label[1].isalpha()
                and site_label[2].isdigit()
                and site_label[3].isalpha()
            ):
                first_two_label_characters = site_label[0] + site_label[1]
                if (
                    first_two_label_characters.lower()
                    != atom_type_symbol.lower()
                ):
                    modified_label = (
                        atom_type_symbol + site_label[2] + site_label[3]
                    )
                    line = line.replace(site_label, modified_label)
                    is_cif_file_updated = True

            """
            Type 7.
            Ex) 1817279.cif
            Fe2 Pt 1 d 0.5 0.5 0.5 0.01(4) -> Pt2 Pt 1 d 0.5 0.5 0.5 0.01(4)
            """
            if (
                len(site_label) == 3
                and site_label[0].isalpha()
                and site_label[1].isalpha()
                and site_label[2].isdigit()
            ):
                first_two_label_characters = site_label[0] + site_label[1]
                if (
                    first_two_label_characters.lower()
                    != atom_type_symbol.lower()
                ):
                    modified_label = atom_type_symbol + site_label[2]
                    line = line.replace(site_label, modified_label)
                    is_cif_file_updated = True

        modified_lines.append(line + "\n")

    if is_cif_file_updated:
        with open(file_path, "r") as f:
            original_lines = f.readlines()

        start_index, end_index = cif_parser.get_line_start_end_line_indexes(
            file_path, "_atom_site_occupancy"
        )
        # Replace the specific section in original_lines with modified_lines
        original_lines[start_index:end_index] = modified_lines

        # Write the modified content back to the file
        with open(file_path, "w") as f:
            f.writelines(original_lines)


def preprocess_cif_file_by_removing_author_loop(file_path):
    start_index, end_index = cif_parser.get_line_start_end_line_indexes(
        file_path, "_publ_author_address"
    )

    with open(file_path, "r") as f:
        original_lines = f.readlines()

        # Replace the specific section in original_lines with modified_lines
        original_lines[start_index:end_index] = ["''\n", ";\n", ";\n"]

    with open(file_path, "w") as f:
        f.writelines(original_lines)
