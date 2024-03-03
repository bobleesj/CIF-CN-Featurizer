# CIF Coordination Number Featurizer
![Feature Extraction Diagram](feature-extraction-diagram.png)

The CIF File Featurizer is a Python script designed to process CIF (Crystallographic Information File) files and extract various features from them. These features include interatomic distances, atomic environment information, and coordination numbers. The script can handle binary and ternary compounds.

## Features
- Process CIF files to extract structural information.
- Calculate interatomic distances between atoms.
- Extract atomic environment information using Wyckoff positions.
- Calculate coordination numbers for each atom.
- Save extracted features to CSV files for further analysis.

## Installation
Before running the script, make sure you have the following dependencies installed:


You can install these dependencies using pip:

```bash
pip install click gemmi matplotlib numpy openpyxl pandas pytest scipy sympy
cd cif-featurizer
python main.py
```

The recommended way for installation is using Conda

```bash
git clone https://github.com/bobleesj/cif-featurizer.git
cd cif-featurizer
conda create -n cif python=3.12
conda activate cif
pip install -r requirements.txt
python main.py
```

> If you are new to Conda (Python package manager), I have written a tutorial for you here [Intro to Python package manager for beginners (Ft. Conda with Cheatsheet](https://bobleesj.github.io/tutorial/2024/02/26/intro-to-python-package-manager.html).

## Contributors
- Anton Oliynyk
- Arnab Dutta
- Nikhil Kumar Barua
- Nishant Yadav
- Sangjoon Bob Lee
- Siddha Sankalpa Sethi

## CIF CLEAN
Before running `CIF Featurizer` it is recommended to use [CIF Cleaner](https://github.com/bobleesj/cif-cleaner/) to pre-process and relocate any CIF files with error. 


## Publications 
Here is a list of publications that have used this code for analysis

[1] Y. Tyvanchuk, V. Babizhetskyy, S. Baran, A. Szytula, V. Smetana, S. Lee, A. O. Oliynyk, A.
Mudring, The crystal and electronic structure of RE23Co6.7In20.3 (RE = Gd–Tm, Lu): A new structure type based on intergrowth of AlB2- and CsCl-type related slabs. *Journal of Alloys and Compounds*. **976**, 173241 (2024). [doi.org/10.1016/j.jallcom.2023.173241](https://doi.org/10.1016/j.jallcom.2023.173241)

