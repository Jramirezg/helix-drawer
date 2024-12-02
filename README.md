# DNA Helix Visualizer

A simple tool for visualizing DNA sequences in both 2D and 3D, with support for interactive exploration. This project provides multiple visualization methods including static 2D/3D renders and interactive molecular viewing.

## Features

- 2D DNA helix visualization using Matplotlib
- 3D static visualization using PyVista
- Interactive 3D visualization using py3Dmol
- Support for AncestryDNA data format
- Color-coded base pairs (A, T, C, G)
- Multiple output formats (PNG, interactive)
- Configurable visualization parameters
- Multi-threaded processing for large datasets

## Installation

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install numpy matplotlib pyvista pyyaml nglview mdtraj biopython py3dmol jupyter
```

## Project structure
```
dna-visualizer/
├── config/
│   └── settings.yaml
├── helix_drawer.py
├── view_dna.ipynb
├── output/
└── README.md
```

## Configuration
Create config/settings.yaml with:


```
dna_file_path: "path/to/your/dna_data.txt"
base_pairs: 200
output_path: "output"
```

## Usage
Static Visualizations
Generate both 2D and 3D static visualizations:

```aiignore
python3 helix_drawer.py

```

## Interactive Visualization
```aiignore
jupyter notebook

```

Open view_dna.ipynb
Run all cells to see the interactive 3D visualization

## Input Data Format
The DNA input file should be tab-separated with these columns:

* Chromosome
* Position
* rsid
* Genotype

### Example Data
```aiignore
1   752721  rs3131972   AG
1   776546  rs12124819  AA
1   832918  rs4040617   GA

```

## Output Files
The program generates:

dna_helix_[timestamp].png: 2D visualization
dna_helix_3d_[timestamp].png: 3D static visualization
Interactive 3D model in Jupyter notebook

## Color Coding
Base pairs are represented with distinct colors:

* Adenine (A): Red
* Thymine (T): Blue
* Cytosine (C): Green
* Guanine (G): Yellow

## Requirements
* Python 3.8+
* Modern web browser for interactive visualization
* 2GB RAM minimum
* Graphics support for 3D rendering

## Testing and Development

### Test Data Generation

The project includes a test data generator that creates synthetic DNA data files in AncestryDNA format. Located in `tests/generate_test_data.py`:
The generator creates realistic test data with:

* Random chromosomes (1-22, X, Y, MT)
* Valid position values
* Random rsid values
* Valid base pair combinations

## Test Files Structure
```aiignore
tests/
├── generate_test_data.py
├── test_ancestry_data.txt
└── large_test_ancestry_data
```

## To use the test data generator, run:
```aiignore
python3 -m tests.generate_test_data

```

This will create a test file with 500,000 DNA entries, perfect for testing the visualization features without requiring real genetic data.


