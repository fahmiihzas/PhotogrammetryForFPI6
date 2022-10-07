import pyvista as pv
from pyvista import examples
import numpy as np

def process(directory, extension=".obj"):
    #File Path
    filename = f'{directory}/kriteria1_dalam{extension}'
    filename1 = f'{directory}/kriteria1_luar{extension}'
    filename2 = f'{directory}/kaki{extension}'

    #Read File Path
    mesh = pv.read(filename)
    mesh1 = pv.read(filename1)
    mesh2 = pv.read(filename2)

    #Clip
    clipped = mesh.clip(normal=[1,0,0], 
                            origin=mesh.center, 
                            invert=False)
    clipped1 = mesh1.clip(normal=[1,0,0], 
                            origin=mesh1.center, 
                            invert=False)
    cell_indices = clipped.faces
    cell_indices1 = clipped1.faces

    # make sure all triangles
    assert not cell_indices.size % 4 and np.all(cell_indices.reshape(-1, 4)[:,0] == 3)
    assert not cell_indices1.size % 4 and np.all(cell_indices1.reshape(-1, 4)[:,0] == 3)


    #Medial Talar Head(dalam)
    data = np.zeros_like(mesh.points)
    data[:, 2] = mesh.points[:, 2]
    maksimum_point_z_medial = -data[:, 2].min()
    minimum_point_z_medial = -data[:, 2].max()
    median_z_medial = (maksimum_point_z_medial+maksimum_point_z_medial)//2
    talonavicular_medial = median_z_medial - minimum_point_z_medial
    #print(talonavicular_medial)

    #Lateral Talar Head(luar)
    data1 = np.zeros_like(mesh1.points)
    data1[:, 2] = mesh1.points[:, 2]
    maksimum_point_z_lateral = -data1[:, 2].min()
    minimum_point_z_lateral = -data1[:, 2].max()
    median_z_lateral = (maksimum_point_z_lateral+minimum_point_z_lateral)//2
    talonavicular_lateral = maksimum_point_z_lateral - median_z_lateral
    #print(talonavicular_lateral)

    #Center of shape
    centers = mesh.cell_centers()
    centers1 = mesh1.cell_centers()

    #clasification
    talonavicular_joint = talonavicular_lateral - talonavicular_medial
    if talonavicular_joint >= 1:
        index = 2
    elif 0.88 <= talonavicular_joint < 1:
        index = 1
    elif -0.7 <= talonavicular_joint < 0.88:
        index = 0
    elif -1 <= talonavicular_joint < -0.7:
        index = -1
    elif talonavicular_joint < -1:
        index = -2
    return index

def show(directory, extension='.obj'):
    filename = f'{directory}/kriteria1_dalam{extension}'
    filename1 = f'{directory}/kriteria1_luar{extension}'
    filename2 = f'{directory}/kaki{extension}'
    
    #Read File Path
    mesh = pv.read(filename)
    mesh1 = pv.read(filename1)
    mesh2 = pv.read(filename2)

    #Clip
    clipped = mesh.clip(normal=[1,0,0], 
                            origin=mesh.center, 
                            invert=False)
    clipped1 = mesh1.clip(normal=[1,0,0], 
                            origin=mesh1.center, 
                            invert=False)
    cell_indices = clipped.faces
    cell_indices1 = clipped1.faces

    # make sure all triangles
    assert not cell_indices.size % 4 and np.all(cell_indices.reshape(-1, 4)[:,0] == 3)
    assert not cell_indices1.size % 4 and np.all(cell_indices1.reshape(-1, 4)[:,0] == 3)

    # Grab ids for all cell nodes
    cell_node_ids = cell_indices.reshape(-1, 4)[:,1:4].ravel()
    cell_node_ids1 = cell_indices1.reshape(-1, 4)[:,1:4].ravel()

    #Bulging in Talonavicular Joint Coordinates
    cell_nodes = clipped.points[cell_node_ids]
    arr3D_bulging = np.array(cell_nodes)

    #Medial Talar Head(dalam)
    cell_nodes = clipped.points[cell_node_ids]
    data = np.zeros_like(mesh.points)
    data[:, 2] = mesh.points[:, 2]
    maksimum_point_z_medial = -data[:, 2].min()
    minimum_point_z_medial = -data[:, 2].max()
    median_z_medial = (maksimum_point_z_medial+maksimum_point_z_medial)//2
    talonavicular_medial = median_z_medial - minimum_point_z_medial

    #Lateral Talar Head(luar)
    cell_nodes1 = clipped1.points[cell_node_ids1]
    data1 = np.zeros_like(mesh1.points)
    data1[:, 2] = mesh1.points[:, 2]
    maksimum_point_z_lateral = -data1[:, 2].min()
    minimum_point_z_lateral = -data1[:, 2].max()
    median_z_lateral = (maksimum_point_z_lateral+minimum_point_z_lateral)//2
    talonavicular_lateral = maksimum_point_z_lateral - median_z_lateral

    #Center of shape
    centers = mesh.cell_centers()
    centers1 = mesh1.cell_centers()

    #plot
    #mesh.plot(cpos = 'zy',scalars=data[:, 2], scalar_bar_args={'title': 'Z Displacement'})

    p = pv.Plotter()
    p.add_mesh(mesh, show_edges=True, line_width=1)
    p.add_mesh(mesh1, show_edges=True, line_width=1)
    p.add_mesh(centers, color="r", point_size=8.0, render_points_as_spheres=True)
    p.add_mesh(centers1, color="r", point_size=8.0, render_points_as_spheres=True)
    p.show(cpos=('zy'))