import pyvista as pv
from pyvista import examples
import numpy as np

def process(directory, extension=".obj"):
    #File Path
    filename = f'{directory}/kriteria4{extension}'
    filename1 = f'{directory}/kaki{extension}'

    #Read File Path
    mesh = pv.read(filename)
    mesh1 = pv.read(filename1)
    clipped = mesh.clip(normal=[1,0,0], 
                            origin=mesh.center, 
                            invert=False)
    cell_indices = clipped.faces

    # make sure all triangles
    assert not cell_indices.size % 4 and np.all(cell_indices.reshape(-1, 4)[:,0] == 3)

    #Array XYZ Polydata
    data = np.zeros_like(mesh.points)
    data[:, 2] = mesh.points[:, 2]

    #clasification
    maksimum_point_z = -data[:, 2].min()
    minimum_point_z = -data[:, 2].max()
    median_z = (maksimum_point_z+minimum_point_z)//2
    Talonavicular_Joint = maksimum_point_z - median_z
    if Talonavicular_Joint >=1.95:
        index = 2
    elif 1.4 <= Talonavicular_Joint < 1.95:
        index = 1
    elif 0.46 <= Talonavicular_Joint < 1.4:
        index = 0
    elif 0.31 <= Talonavicular_Joint < 0.46:
        index = -1
    elif Talonavicular_Joint < 0.31:
        index = -2

    return index

def show(directory, extension=".obj"):
    filename = f'{directory}/kriteria4{extension}'
    filename1 = f'{directory}/kaki{extension}'

    #Read File Path
    mesh = pv.read(filename)
    mesh1 = pv.read(filename1)
    clipped = mesh.clip(normal=[1,0,0], 
                            origin=mesh.center, 
                            invert=False)
    cell_indices = clipped.faces

    # make sure all triangles
    assert not cell_indices.size % 4 and np.all(cell_indices.reshape(-1, 4)[:,0] == 3)

    #Center of shape
    centers = mesh.cell_centers()

    p = pv.Plotter()
    p.add_mesh(mesh, show_edges=True, line_width=1)
    p.add_mesh(mesh1, show_edges=True, line_width=1)
    p.add_mesh(centers, color="r", point_size=8.0, render_points_as_spheres=True)
    p.show(cpos=('zy'))