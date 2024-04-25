import vtk

import matplotlib.pyplot as plt
import numpy as np
from utils import make_plot, save_img
from matplotlib.colors import LinearSegmentedColormap
import glob
from vtk.util.numpy_support import vtk_to_numpy


def check_arrays(data_path):
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(data_path)  # Update this path to your VTI file location
    reader.Update()

    image_data = reader.GetOutput()

    dims = image_data.GetDimensions()
    print("Dimensions of the VTI file are:", dims)
    
    cell_data = image_data.GetCellData()
    num_arrays = cell_data.GetNumberOfArrays()
    print(f"Number of arrays in cell data: {num_arrays}")
    
    # If there are arrays, access one as an example
    if num_arrays > 0:
        for i in range(num_arrays):
            array = cell_data.GetArray(i)
            if array:
                print(f"Array {i} name: {array.GetName()}")
        
            else:
                print(f"Array {i} is None")
    else:
        print("No arrays in cell data.")


def getdata_1D(data_path, array_id, reader, shape):
    reader.SetFileName(data_path)  # Update this path to your VTI file location
    reader.Update()

    image_data = reader.GetOutput()
    cell_data = image_data.GetCellData()
    array = cell_data.GetArray(array_id)

    numpy_array = vtk_to_numpy(array) # 1D data
         
    # Assuming the data is 2D, reshape the flat numpy array into 2D
    # dims = image_data.GetDimensions()
    # numpy_array_2d = numpy_array.reshape(dims[1], dims[0])  # Adjust depending on how your data is organized


    # ux = numpy_array[:,0].reshape(512, 512)  # Adjust depending on how your data is organized
    # uy = numpy_array[:,1].reshape(512, 512)  # Adjust depending on how your data is organized
    # data = np.sqrt(ux**2 +uy**2)



    data = numpy_array.reshape(shape[0], shape[1])
    # Rotate the image by 180 degrees
    data = np.flipud(np.fliplr(data))
    return data 