import logging
import os
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from multiprocessing import Pool

import py3Dmol
import pyvista as pv
import yaml
from Bio.PDB import *
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class DNAConfig:
    RADIUS = 4
    VERTICAL_STRETCH = 4
    SPHERE_RADIUS = 0.3
    CYLINDER_RADIUS = 0.15
    BASE_COLORS_2D = {'A': 'red', 'T': 'blue', 'C': 'green', 'G': 'yellow'}
    BASE_COLORS_3D = {'A': '#FF0000', 'T': '#0000FF', 'C': '#00FF00', 'G': '#FFFF00'}


def load_config():
    config_path = os.path.join('config', 'settings.yaml')
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@lru_cache(maxsize=128)
def calculate_helix_coordinates(base_pairs):
    t = np.linspace(0, 8 * np.pi, base_pairs)
    coords = np.empty((base_pairs, 6))
    coords[:, 0] = DNAConfig.RADIUS * np.cos(t)
    coords[:, 1] = DNAConfig.RADIUS * np.sin(t)
    coords[:, 2] = DNAConfig.VERTICAL_STRETCH * t
    coords[:, 3] = DNAConfig.RADIUS * np.cos(t + np.pi)
    coords[:, 4] = DNAConfig.RADIUS * np.sin(t + np.pi)
    coords[:, 5] = DNAConfig.VERTICAL_STRETCH * t
    return coords


def parse_ancestry_dna(file_path):
    logger.info(f"Parsing DNA data from {file_path}")
    data = np.genfromtxt(file_path, delimiter='\t', dtype=str, comments='#')
    return data[:, :4]


def create_batch_spheres(coordinates, colors):
    spheres = pv.MultiBlock()
    for coord, color in zip(coordinates, colors):
        sphere = pv.Sphere(radius=DNAConfig.SPHERE_RADIUS, center=coord)
        spheres.append(sphere)
    return spheres, colors


def process_dna_batch(batch_data):
    genotypes = [entry[3] for entry in batch_data]
    bases1 = [g[0] if len(g) > 0 else 'A' for g in genotypes]
    bases2 = [g[1] if len(g) > 1 else 'T' for g in genotypes]
    return bases1, bases2


def generate_dna_helix(dna_data, base_pairs=100, output_path='output'):
    logger.info(f"Generating 2D DNA visualization for {base_pairs} base pairs")
    os.makedirs(output_path, exist_ok=True)

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')

    coords = calculate_helix_coordinates(base_pairs)
    x1, y1, z1 = coords[:, 0], coords[:, 1], coords[:, 2]
    x2, y2, z2 = coords[:, 3], coords[:, 4], coords[:, 5]

    ax.plot(x1, y1, z1, color='gray', alpha=0.5, linewidth=2)
    ax.plot(x2, y2, z2, color='gray', alpha=0.5, linewidth=2)

    bases1, bases2 = process_dna_batch(dna_data[:base_pairs])
    colors1 = [DNAConfig.BASE_COLORS_2D[base] for base in bases1]
    colors2 = [DNAConfig.BASE_COLORS_2D[base] for base in bases2]

    ax.scatter(x1, y1, z1, c=colors1, s=100)
    ax.scatter(x2, y2, z2, c=colors2, s=100)

    for i in range(base_pairs):
        ax.plot([x1[i], x2[i]], [y1[i], y2[i]], [z1[i], z2[i]],
                color='darkgray', alpha=0.8, linewidth=1.5)

    legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=color, label=base, markersize=10)
                       for base, color in DNAConfig.BASE_COLORS_2D.items()]
    ax.legend(handles=legend_elements, title='DNA Bases',
              loc='center left', bbox_to_anchor=(1.1, 0.5))

    ax.view_init(elev=0, azim=90)
    ax.set_axis_off()
    ax.set_box_aspect([1, 1, 2])

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    image_path = os.path.join(output_path, f'dna_helix_{timestamp}.png')
    plt.savefig(image_path, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()


def generate_3d_helix(dna_data, base_pairs=100, output_path='output'):
    logger.info(f"Generating 3D DNA visualization for {base_pairs} base pairs")
    plotter = pv.Plotter(window_size=[1920, 1080], off_screen=True)
    plotter.set_background('white')

    coords = calculate_helix_coordinates(base_pairs)
    bases1, bases2 = process_dna_batch(dna_data[:base_pairs])

    # Create backbone splines
    points1 = coords[:, :3]
    points2 = coords[:, 3:]
    backbone1 = pv.Spline(points1).tube(radius=DNAConfig.CYLINDER_RADIUS)
    backbone2 = pv.Spline(points2).tube(radius=DNAConfig.CYLINDER_RADIUS)

    # Add backbones
    plotter.add_mesh(backbone1, color='darkgray')
    plotter.add_mesh(backbone2, color='darkgray')

    # Batch process spheres
    spheres1, colors1 = create_batch_spheres(points1, [DNAConfig.BASE_COLORS_3D[b] for b in bases1])
    spheres2, colors2 = create_batch_spheres(points2, [DNAConfig.BASE_COLORS_3D[b] for b in bases2])

    for sphere, color in zip(spheres1, colors1):
        plotter.add_mesh(sphere, color=color)
    for sphere, color in zip(spheres2, colors2):
        plotter.add_mesh(sphere, color=color)

    # Add connecting tubes
    for i in range(base_pairs):
        cylinder = pv.Line(points1[i], points2[i]).tube(radius=DNAConfig.CYLINDER_RADIUS)
        plotter.add_mesh(cylinder, color='gray')

    legend_entries = []
    for base, color in DNAConfig.BASE_COLORS_3D.items():
        legend_entries.extend([f'Base {base}', color])
    plotter.add_legend(legend_entries)

    plotter.camera_position = 'xz'
    plotter.camera.zoom(1.5)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    image_path = os.path.join(output_path, f'dna_helix_3d_{timestamp}.png')
    plotter.screenshot(image_path)


def generate_3dmol_helix(dna_data, base_pairs=100):
    logger.info(f"Generating 3DMol DNA visualization for {base_pairs} base pairs")

    view = py3Dmol.view(width=1920, height=1080)
    coords = calculate_helix_coordinates(base_pairs)

    # Create DNA structure
    for i in range(base_pairs):
        view.addSphere({
            'center': {'x': coords[i, 0], 'y': coords[i, 1], 'z': coords[i, 2]},
            'radius': 0.5,
            'color': DNAConfig.BASE_COLORS_3D[dna_data[i][3][0]]
        })

    view.zoomTo()

    # Simple PNG export
    view.png()

    return view


if __name__ == "__main__":
    config = load_config()
    file_path = config['dna_file_path']
    base_pairs = config.get('base_pairs', 200)
    output_path = config.get('output_path', 'output')

    with Pool() as pool:
        dna_data = parse_ancestry_dna(file_path)
        generate_dna_helix(dna_data, base_pairs=base_pairs, output_path=output_path)
        generate_3d_helix(dna_data, base_pairs=base_pairs, output_path=output_path)
        generate_3dmol_helix(dna_data, base_pairs=base_pairs)


