# Structure Analysis/Featurizer (SAF)

![Feature Extraction Diagram](assets/img/feature-extraction-diagram.png)

## Purpose

Structure Analysis/Featurizer (SAF) is a Python script designed to process CIF
(Crystallographic Information File) files and extract geometric features. These
features include interatomic distances, information on atomic environments, and
coordination numbers. The script can sequentially process more than 10,000
`.cif` files and generate millions of data points used as ML input data.

:warning: **Caution:** Do you want to generate geometric features beyond binary
and ternary files? Please email me at
[sl5400@columbia.edu](mailto:sl5400@columbia.edu).

## Motivation

The script was originally developed to determine the coordination number and
geometry for each crystallographic site on complex structures [[1](#ref1)].
Then, we further included an interactive functionality for experimentalists and
data scientists to generate structural features from `.cif` file. These features
were engineered to be used as input data for ML models to predict crystal
structures and their properties.

## Features

- 94 numerical features for binary compounds saved in `.csv`
- 193 numerical features for ternary compounds saved in `.csv`

For a complete list of features, see the [Full Feature List](#full-feature-list)
section.

## Scope

The current version supports the processing of **binary** and **ternary** `.cif`
files containing the following elements: `Si` `Sc` `Fe` `Co` `Ni` `Ga` `Ge` `Y`
`Ru` `Rh` `Pd` `In` `Sn` `Sb` `La` `Ce` `Pr` `Nd` `Sm` `Eu` `Gd` `Tb` `Dy` `Ho`
`Er` `Tm` `Yb` `Lu` `Os` `Ir` `Pt` `Th` `U` `Al` `Mo` `Hf` `Ta`. `Ag` `As` `Au`
`B` `Ba` `Be` `Bi` `C` `Ca` `Cd` `Cr` `Cs` `Cu` `Hg` `K` `Li` `Mg` `Mn` `Na`
`Nb` `P` `Pb` `Rb` `Re` `S` `Se` `Sr` `Te` `Ti` `Tl` `V` `W` `Zn` `Zr`

:warning: You may use CIF Cleaner (https://github.com/bobleesj/cif-cleaner) to
interactively filter `.cif` files based on composition type (binary, ternary)
and elements without programming.

### Adding more elements

To include more elements, you need to provide `CIF_radius` and `Pauling_CN12`
values in the `get_radius_data()` function located in `core/data/radius.py` as
shown below:

```python
def get_radius_data():
    """
    Return a dictionary of element radii data.
    """
    data = {
        "Si": [1.176, 1.316],
        "Sc": [1.641, 1.620],
        "Fe": [1.242, 1.260],
        "Co": [1.250, 1.252],
        "Ni": [1.246, 1.244],
        "Ga": [1.243, 1.408],
        "Ge": [1.225, 1.366],
        ...
    }
```

### Atom labeling for compounds

For binary compounds, atoms are labeled as `AB`, and for ternary compounds,
atoms are labeled as `RMX`, where `R=A` and `M=B`. If you want to customize
this, modify the `get_binary_AB_labels` or `get_ternary_RMX_labels` function in
`core/config.py` as shown below:

```python
A_labels = ["Sc", "Y", "La", "Ce", "Pr", "Nd", "Sm",
            "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Th", "U"]
B_labels = ["Si", "Ga", "Ge", "In", "Sn", "Sb", "Al"]
M_labels = ["Fe", "Co", "Ni", "Ru", "Rh", "Pd", "Os", "Ir", "Pt"]
```

## Getting started

Start with the script via

```bash
python main.py
```

Once the script is started, the user needs to only confirm (1) whether to skip
`cif` files based on the number of atoms in the supercell generated and (2)
choose the folder.

```text
Welcome to CIF Featurizer! This script processes Crystallographic Information
File (CIF) files to extract various features such as interatomic distances,
atomic environment information, and coordination numbers.  It supports binary
and ternary compounds.

Q1. Do you want to skip any CIF files based on the number of unique in the supercell?
(Default: N) [y/N]: N

Available folders containing CIF files:
1. 20240226_huge_file_test
2. 20240402_ThSb
3. 20240303_ternary_binary_test
4. 20240402_URhIn

Enter the number corresponding to the folder containing .cif files: 3
```

### Output

After running the script using `python main.py` and selecting the folder
contianing `.cif` files, `.csv` files are generated. For binary compounds,
`binary_features.csv` with 124 features is generated. For ternary compounds,
`ternary_features.csv` with 165 unique features is generated. For all types of
compounds, `universal_featrues.csv` is generated.

### Coordination numbers

The coordination numbers and their geometric values are determined using four
unique coordination determination methods, as detailed in the manuscript
([DOI](https://doi.org/10.1016/j.jallcom.2023.173241)). Below is an example from
a site. Once the code becomes more matured, we will further make a better
documentation here.

| #   | CN method              | Central atom label | CN  | R   | M   | X   | Polyhedron volume | Dist from atom to center of mass | Edges | Faces |
| --- | ---------------------- | ------------------ | --- | --- | --- | --- | ----------------- | -------------------------------- | ----- | ----- |
| 1   | Shortest dist          | Er1                | 13  | 5   | 2   | 6   | 89.293            | 0.095                            | 33    | 22    |
| 2   | CIF radius sum         | Er1                | 13  | 5   | 2   | 6   | 89.293            | 0.095                            | 33    | 22    |
| 3   | CIF radius refined sum | Er1                | 13  | 5   | 2   | 6   | 89.293            | 0.095                            | 33    | 22    |
| 4   | Pualing radius sum     | Er1                | 13  | 5   | 2   | 6   | 89.293            | 0.095                            | 33    | 22    |

The coordination number-based geometric information is calculated as the average
based on the min, max, and avg of rows from each central label. As the project
evolves, further refinements and enhancements to the documentation will be
implemented.

## Installation

Before running the script, make sure you have the following dependencies
installed:

```bash
pip install click gemmi matplotlib numpy openpyxl pandas scipy sympy cifkit
cd structure-analyzer-featurizer
python main.py
```

The recommended way for installation is Conda

```bash
git clone https://github.com/bobleesj/structure-analyzer-featurizer.git
cd structure-analyzer-featurizer
conda create -n cif python=3.12
conda activate cif
pip install -r requirements.txt
python main.py
```

If you are new to Conda (Python package manager), you may refer to
[Intro to Python package manager for beginners (Ft. Conda with Cheatsheet](https://bobleesj.github.io/tutorial/2024/02/26/intro-to-python-package-manager.html).

## Contributors

- Anton Oliynyk - CUNY Hunger College
- Arnab Dutta - IIT Kharagpur
- Nikhil Kumar Barua - University of Waterloo
- Nishant Yadav - IIT Kharagpur
- Sangjoon Bob Lee - Columbia University
- Siddha Sankalpa Sethi - IIT Kharagpur

## Publications

Here is a list of publications that have used this code for analysis:

<span id="ref1"></span> [1] Y. Tyvanchuk, V. Babizhetskyy, S. Baran, A. Szytula,
V. Smetana, S. Lee, A. O. Oliynyk, A. Mudring, The crystal and electronic
structure of RE23Co6.7In20.3 (RE = Gd–Tm, Lu): A new structure type based on
intergrowth of AlB2- and CsCl-type related slabs. _Journal of Alloys and
Compounds_. **976**, 173241 (2024).
[doi.org/10.1016/j.jallcom.2023.173241](https://doi.org/10.1016/j.jallcom.2023.173241)

## Full feature list

#### Binary structural features

| #   | Feature                                                         | Description                                                                                                                                              |
| --- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Entry                                                           | Used to match with CAF data or any other data to merge in one single file                                                                                |
| 2   | formula                                                         |  Label                                                                                                                                                   |
| 3   | A                                                               | Element A matched with the group                                                                                                                         |
| 4   | B                                                               | Element B matched with the group                                                                                                                         |
| 5   | INT_distAA                                                      | Interatomic distances from CIF                                                                                                                           |
| 6   | INT_distBB                                                      | Interatomic distances from CIF                                                                                                                           |
| 7   | INT_distAB                                                      | Interatomic distances from CIF                                                                                                                           |
| 8   | INT_Asize                                                       | CIF radius for atom A                                                                                                                                    |
| 9   | INT_Bsize                                                       | CIF radius for atom B                                                                                                                                    |
| 10  | INT_Asize_by_Bsize                                              | Radius ratio (CIF radius)                                                                                                                                |
| 11  | INT_distAA_by2_byAsize                                          | Default size scale fit                                                                                                                                   |
| 12  | INT_distBB_by2_byBsize                                          | Default size scale fit                                                                                                                                   |
| 13  | INT_distAB_by2_byAsizebyBsize                                   | Default size scale                                                                                                                                       |
| 14  | INT_Asize_ref                                                   | Refined radius                                                                                                                                           |
| 15  | INT_Bsize_ref                                                   | Refined radius                                                                                                                                           |
| 16  | INT_percent_diff_A_by_100                                       | How much different from default scale                                                                                                                    |
| 17  | INT_percent_diff_B_by_100                                       | How much different from default scale                                                                                                                    |
| 18  | INT_distAA_minus_ref_diff                                       | Refined scale fitness (0 means the distance used for refinements)                                                                                        |
| 19  | INT_distBB_minus_ref_diff                                       | Refined scale fitness (0 means the distance used for refinements)                                                                                        |
| 20  | INT_distAB_minus_ref_diff                                       | Refined scale fitness (0 means the distance used for refinements)                                                                                        |
| 21  | INT_R_factor                                                    | R factor for the refinement (least square difference)                                                                                                    |
| 22  | INT_UNI_shortest_homoatomic_dist                                | Shortest homoatomic distance                                                                                                                             |
| 23  | INT_UNI_shortest_heteroatomic_dist                              | Shortest heteroatomic distance                                                                                                                           |
| 24  | INT_UNI_shortest_homoatomic_dist_by_2_by_atom_size              | Shortest homoatomic distance by 2 by atom size                                                                                                           |
| 25  | INT_UNI_shortest_heteroatomic_dist_by_sum_of_atom_sizes         | Shortest heteroatomic distance by sum of atom sizes                                                                                                      |
| 26  | INT_UNI_shortest_homoatomic_dist_by_2_by_refined_atom_size      | Shortest homoatomic distance by 2 by refined atom size                                                                                                   |
| 27  | INT_UNI_shortest_heteroatomic_dist_by_sum_of_refined_atom_sizes | Shortest heteroatomic distance by sum of refined sizes                                                                                                   |
| 28  | INT_UNI_highest_refined_percent_diff_abs                        | Highest refined percent difference by 100 (abs value)                                                                                                    |
| 29  | INT_UNI_lowest_refined_percent_diff_abs                         | Lowest refined percent difference by 100 (abs value)                                                                                                     |
| 30  | INT_UNI_packing_efficiency                                      | Packing efficiency in unit cell with refined radius                                                                                                      |
| 31  | WYC_A_lowest_wyckoff_label                                      | Lowest Wyckoff number for element A                                                                                                                      |
| 32  | WYC_B_lowest_wyckoff_label                                      | Lowest Wyckoff number for element B                                                                                                                      |
| 33  | WYC_identical_lowest_wyckoff_count                              | Number of sites with the lowest Wyckoff number                                                                                                           |
| 34  | WYC_A_sites_total                                               | Number of crystallographic sites for element A                                                                                                           |
| 35  | WYC_B_sites_total                                               | Number of crystallographic sites for element B                                                                                                           |
| 36  | WYC_A_multiplicity_total                                        | Sum of Wyckoff numbers for element A                                                                                                                     |
| 37  | WYC_B_multiplicity_total                                        | Sum of Wyckoff numbers for element B                                                                                                                     |
| 38  | ENV_A_shortest_dist_count                                       | Number of atoms that are at the shortest distance from atom A                                                                                            |
| 39  | ENV_B_shortest_dist_count                                       | Number of atoms that are at the shortest distance from atom B                                                                                            |
| 40  | ENV_A_avg_shortest_dist_count                                   | Average number of atoms that are at the shortest distance from atom A (case if multiple sites present)                                                   |
| 41  | ENV_B_avg_shortest_dist_count                                   | Average number of atoms that are at the shortest distance from atom B (case if multiple sites present)                                                   |
| 42  | ENV_A_shortest_tol_dist_count                                   | Number of atoms that are at the shortest distance from atom A (with some distance tolerance applied, default 5%)                                         |
| 43  | ENV_B_shortest_tol_dist_count                                   | Number of atoms that are at the shortest distance from atom B (with some distance tolerance applied, default 5%)                                         |
| 44  | ENV_A_avg_shortest_dist_within_tol_count                        | Average number of atoms that are at the shortest distance from atom A (case if multiple sites present, with some distance tolerance applied, default 5%) |
| 45  | ENV_B_avg_shortest_dist_within_tol_count                        | Average number of atoms that are at the shortest distance from atom B (case if multiple sites present, with some distance tolerance applied, default 5%) |
| 46  | ENV_A_second_by_first_shortest_dist                             | 2nd shortest distance/1st shorted distance for atom A, measures distortion of polyhedron                                                                 |
| 47  | ENV_B_second_by_first_shortest_dist                             | 2nd shortest distance/1st shorted distance for atom B, measures distortion of polyhedron                                                                 |
| 48  | ENV_A_avg_second_by_first_shortest_dist                         | 2nd shortest distance/1st shorted distance for atom A, measures distortion of polyhedron (case if multiple sites present)                                |
| 49  | ENV_B_avg_second_by_first_shortest_dist                         | 2nd shortest distance/1st shorted distance for atom B, measures distortion of polyhedron (case if multiple sites present)                                |
| 50  | ENV_A_second_shortest_dist_count                                | 2nd shortest distance count for atom A                                                                                                                   |
| 51  | ENV_B_second_shortest_dist_count                                | 2nd shortest distance count for atom B                                                                                                                   |
| 52  | ENV_A_avg_second_shortest_dist_count                            | Average 2nd shortest distance count for atom A                                                                                                           |
| 53  | ENV_B_avg_second_shortest_dist_count                            | Average 2nd shortest distance count for atom B                                                                                                           |
| 54  | ENV_A_homoatomic_dist_by_shortest_dist                          | A-A distance / shortest distance                                                                                                                         |
| 55  | ENV_B_homoatomic_dist_by_shortest_dist                          | B-B distance / shortest distance                                                                                                                         |
| 56  | ENV_A_avg_homoatomic_dist_by_shortest_dist                      | Average A-A distance / shortest distance                                                                                                                 |
| 57  | ENV_B_avg_homoatomic_dist_by_shortest_dist                      | Average B-B distance / shortest distance                                                                                                                 |
| 58  | ENV_A_count_at_A_shortest_dist                                  | Number of A atoms next to the A atoms at the shortest distance                                                                                           |
| 59  | ENV_A_count_at_B_shortest_dist                                  | Number of A atoms next to the B atoms at the shortest distance                                                                                           |
| 60  | ENV_A_avg_count_at_A_shortest_dist                              | Average number of A atoms next to the A atoms at the shortest distance                                                                                   |
| 61  | ENV_A_avg_count_at_B_shortest_dist                              | Average number of A atoms next to the B atoms at the shortest distance                                                                                   |
| 62  | ENV_B_count_at_A_shortest_dist                                  | Number of B atoms next to the A atoms at the shortest distance                                                                                           |
| 63  | ENV_B_count_at_B_shortest_dist                                  | Number of B atoms next to the B atoms at the shortest distance                                                                                           |
| 64  | ENV_B_avg_count_at_A_shortest_dist                              | Average number of B atoms next to the A atoms at the shortest distance                                                                                   |
| 65  | ENV_B_avg_count_at_B_shortest_dist                              | Average number of B atoms next to the B atoms at the shortest distance                                                                                   |
| 66  | CN_AVG_coordination_number                                      | Average coordination number                                                                                                                              |
| 67  | CN_AVG_A_atom_count                                             | Average atom A number within CN                                                                                                                          |
| 68  | CN_AVG_B_atom_count                                             | Average atom B number within CN                                                                                                                          |
| 69  | CN_AVG_polyhedron_volume                                        | Average volume of polyhedra                                                                                                                              |
| 70  | CN_AVG_central_atom_to_center_of_mass_dist                      | Average distance from the central atom to the center of mass of polyhedron                                                                               |
| 71  | CN_AVG_number_of_edges                                          | Average number of edges of polyhedron                                                                                                                    |
| 72  | CN_AVG_number_of_faces                                          | Average number of faces of polyhedron                                                                                                                    |
| 73  | CN_AVG_shortest_distance_to_face                                | Average shortest distance from central atom to center of face of polyhedron                                                                              |
| 74  | CN_AVG_shortest_distance_to_edge                                | Average shortest distance from central atom to middle edge of polyhedron                                                                                 |
| 75  | CN_AVG_volume_of_inscribed_sphere                               | Average volume of inscribed sphere that could be fit in polyhedron                                                                                       |
| 76  | CN_AVG_packing_efficiency                                       | Average packing efficiency of polyhedron                                                                                                                 |
| 77  | CN_MIN_coordination_number                                      | Minimum coordination number                                                                                                                              |
| 78  | CN_MIN_A_atom_count                                             | Minimum atom A number within CN                                                                                                                          |
| 79  | CN_MIN_B_atom_count                                             | Minimum atom B number within CN                                                                                                                          |
| 80  | CN_MIN_polyhedron_volume                                        | Minimum volume of polyhedra                                                                                                                              |
| 81  | CN_MIN_central_atom_to_center_of_mass_dist                      | Minimum distance from the central atom to the center of mass of polyhedron                                                                               |
| 82  | CN_MIN_number_of_edges                                          | Minimum number of edges of polyhedron                                                                                                                    |
| 83  | CN_MIN_number_of_faces                                          | Minimum number of faces of polyhedron                                                                                                                    |
| 84  | CN_MIN_shortest_distance_to_face                                | Minimum shortest distance from central atom to center of face of polyhedron                                                                              |
| 85  | CN_MIN_shortest_distance_to_edge                                | Minimum shortest distance from central atom to middle edge of polyhedron                                                                                 |
| 86  | CN_MIN_volume_of_inscribed_sphere                               | Minimum volume of inscribed sphere that could be fit in polyhedron                                                                                       |
| 87  | CN_MIN_packing_efficiency                                       | Minimum packing efficiency of polyhedron                                                                                                                 |
| 88  | CN_MAX_coordination_number                                      | Maximum coordination number                                                                                                                              |
| 89  | CN_MAX_A_atom_count                                             | Maximum atom A number within CN                                                                                                                          |
| 90  | CN_MAX_B_atom_count                                             | Maximum atom B number within CN                                                                                                                          |
| 91  | CN_MAX_polyhedron_volume                                        | Maximum volume of polyhedra                                                                                                                              |
| 92  | CN_MAX_central_atom_to_center_of_mass_dist                      | Maximum distance from the central atom to the center of mass of polyhedron                                                                               |
| 93  | CN_MAX_number_of_edges                                          | Maximum number of edges of polyhedron                                                                                                                    |
| 94  | CN_MAX_number_of_faces                                          | Maximum number of faces of polyhedron                                                                                                                    |
| 95  | CN_MAX_shortest_distance_to_face                                | Maximum shortest distance from central atom to center of face of polyhedron                                                                              |
| 96  | CN_MAX_shortest_distance_to_edge                                | Maximum shortest distance from central atom to middle edge of polyhedron                                                                                 |
| 97  | CN_MAX_volume_of_inscribed_sphere                               | Maximum volume of inscribed sphere that could be fit in polyhedron                                                                                       |
| 98  | CN_MAX_packing_efficiency                                       | Maximum packing efficiency of polyhedron                                                                                                                 |

#### Ternary structural features

| #   | Feature                                                         |
| --- | --------------------------------------------------------------- |
| 1   | Entry                                                           |
| 2   | formula                                                         |
| 3   | R                                                               |
| 4   | M                                                               |
| 5   | X                                                               |
| 6   | INT_distRR                                                      |
| 7   | INT_distMM                                                      |
| 8   | INT_distXX                                                      |
| 9   | INT_distRM                                                      |
| 10  | INT_distMX                                                      |
| 11  | INT_distRX                                                      |
| 12  | INT_Rsize                                                       |
| 13  | INT_Msize                                                       |
| 14  | INT_Xsize                                                       |
| 15  | INT_Rsize_by_Msize                                              |
| 16  | INT_Msize_by_Xsize                                              |
| 17  | INT_Rsize_by_Xsize                                              |
| 18  | INT_distRR_by2_byRsize                                          |
| 19  | INT_distMM_by2_byMsize                                          |
| 20  | INT_distXX_by2_byXsize                                          |
| 21  | INT_distRM_byRsizebyMsize                                       |
| 22  | INT_distMX_byMsizebyXsize                                       |
| 23  | INT_distRX_byRsizebyXsize                                       |
| 24  | INT_Rsize_ref                                                   |
| 25  | INT_Msize_ref                                                   |
| 26  | INT_Xsize_ref                                                   |
| 27  | INT_percent_diff_R_by_100                                       |
| 28  | INT_percent_diff_M_by_100                                       |
| 29  | INT_percent_diff_X_by_100                                       |
| 30  | INT_distRR_minus_ref_diff                                       |
| 31  | INT_distMM_minus_ref_diff                                       |
| 32  | INT_distXX_minus_ref_diff                                       |
| 33  | INT_distRM_minus_ref_diff                                       |
| 34  | INT_distMX_minus_ref_diff                                       |
| 35  | INT_distRX_minus_ref_diff                                       |
| 36  | INT_R_factor                                                    |
| 37  | INT_UNI_shortest_homoatomic_dist                                |
| 38  | INT_UNI_shortest_heteroatomic_dist                              |
| 39  | INT_UNI_shortest_homoatomic_dist_by_2_by_atom_size              |
| 40  | INT_UNI_shortest_heteroatomic_dist_by_sum_of_atom_sizes         |
| 41  | INT_UNI_shortest_homoatomic_dist_by_2_by_refined_atom_size      |
| 42  | INT_UNI_shortest_heteroatomic_dist_by_sum_of_refined_atom_sizes |
| 43  | INT_UNI_highest_refined_percent_diff_abs                        |
| 44  | INT_UNI_lowest_refined_percent_diff_abs                         |
| 45  | INT_UNI_packing_efficiency                                      |
| 46  | WYC_R_lowest_wyckoff_label                                      |
| 47  | WYC_M_lowest_wyckoff_label                                      |
| 48  | WYC_X_lowest_wyckoff_label                                      |
| 49  | WYC_identical_lowest_wyckoff_count                              |
| 50  | WYC_R_sites_total                                               |
| 51  | WYC_M_sites_total                                               |
| 52  | WYC_X_sites_total                                               |
| 53  | WYC_R_multiplicity_total                                        |
| 54  | WYC_M_multiplicity_total                                        |
| 55  | WYC_X_multiplicity_total                                        |
| 56  | ENV_R_shortest_dist_count                                       |
| 57  | ENV_M_shortest_dist_count                                       |
| 58  | ENV_X_shortest_dist_count                                       |
| 59  | ENV_R_avg_shortest_dist_count                                   |
| 60  | ENV_M_avg_shortest_dist_count                                   |
| 61  | ENV_X_avg_shortest_dist_count                                   |
| 62  | ENV_R_shortest_tol_dist_count                                   |
| 63  | ENV_M_shortest_tol_dist_count                                   |
| 64  | ENV_X_shortest_tol_dist_count                                   |
| 65  | ENV_R_avg_shortest_dist_within_tol_count                        |
| 66  | ENV_M_avg_shortest_dist_within_tol_count                        |
| 67  | ENV_X_avg_shortest_dist_within_tol_count                        |
| 68  | ENV_R_second_by_first_shortest_dist                             |
| 69  | ENV_M_second_by_first_shortest_dist                             |
| 70  | ENV_X_second_by_first_shortest_dist                             |
| 71  | ENV_R_avg_second_by_first_shortest_dist                         |
| 72  | ENV_M_avg_second_by_first_shortest_dist                         |
| 73  | ENV_X_avg_second_by_first_shortest_dist                         |
| 74  | ENV_R_second_shortest_dist_count                                |
| 75  | ENV_M_second_shortest_dist_count                                |
| 76  | ENV_X_second_shortest_dist_count                                |
| 77  | ENV_R_avg_second_shortest_dist_count                            |
| 78  | ENV_M_avg_second_shortest_dist_count                            |
| 79  | ENV_X_avg_second_shortest_dist_count                            |
| 80  | ENV_R_homoatomic_dist_by_shortest_dist                          |
| 81  | ENV_M_homoatomic_dist_by_shortest_dist                          |
| 82  | ENV_X_homoatomic_dist_by_shortest_dist                          |
| 83  | ENV_R_avg_homoatomic_dist_by_shortest_dist                      |
| 84  | ENV_M_avg_homoatomic_dist_by_shortest_dist                      |
| 85  | ENV_X_avg_homoatomic_dist_by_shortest_dist                      |
| 86  | ENV_R_count_at_R_shortest_dist                                  |
| 87  | ENV_R_count_at_M_shortest_dist                                  |
| 88  | ENV_R_count_at_X_shortest_dist                                  |
| 89  | ENV_R_avg_count_at_R_shortest_dist                              |
| 90  | ENV_R_avg_count_at_M_shortest_dist                              |
| 91  | ENV_R_avg_count_at_X_shortest_dist                              |
| 92  | ENV_M_count_at_R_shortest_dist                                  |
| 93  | ENV_M_count_at_M_shortest_dist                                  |
| 94  | ENV_M_count_at_X_shortest_dist                                  |
| 95  | ENV_M_avg_count_at_R_shortest_dist                              |
| 96  | ENV_M_avg_count_at_M_shortest_dist                              |
| 97  | ENV_M_avg_count_at_X_shortest_dist                              |
| 98  | ENV_X_count_at_R_shortest_dist                                  |
| 99  | ENV_X_count_at_M_shortest_dist                                  |
| 100 | ENV_X_count_at_X_shortest_dist                                  |
| 101 | ENV_X_avg_count_at_R_shortest_dist                              |
| 102 | ENV_X_avg_count_at_M_shortest_dist                              |
| 103 | ENV_X_avg_count_at_X_shortest_dist                              |
| 104 | CN_AVG_coordination_number                                      |
| 105 | CN_AVG_R_atom_count                                             |
| 106 | CN_AVG_M_atom_count                                             |
| 107 | CN_AVG_X_atom_count                                             |
| 108 | CN_AVG_polyhedron_volume                                        |
| 109 | CN_AVG_central_atom_to_center_of_mass_dist                      |
| 110 | CN_AVG_number_of_edges                                          |
| 111 | CN_AVG_number_of_faces                                          |
| 112 | CN_AVG_shortest_distance_to_face                                |
| 113 | CN_AVG_shortest_distance_to_edge                                |
| 114 | CN_AVG_volume_of_inscribed_sphere                               |
| 115 | CN_AVG_packing_efficiency                                       |
| 116 | CN_MIN_coordination_number                                      |
| 117 | CN_MIN_R_atom_count                                             |
| 118 | CN_MIN_M_atom_count                                             |
| 119 | CN_MIN_X_atom_count                                             |
| 120 | CN_MIN_polyhedron_volume                                        |
| 121 | CN_MIN_central_atom_to_center_of_mass_dist                      |
| 122 | CN_MIN_number_of_edges                                          |
| 123 | CN_MIN_number_of_faces                                          |
| 124 | CN_MIN_shortest_distance_to_face                                |
| 125 | CN_MIN_shortest_distance_to_edge                                |
| 126 | CN_MIN_volume_of_inscribed_sphere                               |
| 127 | CN_MIN_packing_efficiency                                       |
| 128 | CN_MAX_coordination_number                                      |
| 129 | CN_MAX_R_atom_count                                             |
| 130 | CN_MAX_M_atom_count                                             |
| 131 | CN_MAX_X_atom_count                                             |
| 132 | CN_MAX_polyhedron_volume                                        |
| 133 | CN_MAX_central_atom_to_center_of_mass_dist                      |
| 134 | CN_MAX_number_of_edges                                          |
| 135 | CN_MAX_number_of_faces                                          |
| 136 | CN_MAX_shortest_distance_to_face                                |
| 137 | CN_MAX_shortest_distance_to_edge                                |
| 138 | CN_MAX_volume_of_inscribed_sphere                               |
| 139 | CN_MAX_packing_efficiency                                       |
