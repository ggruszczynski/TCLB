# Step 1: Import the necessary libraries
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import matplotlib.pyplot as plt
import numpy as np

# %% Step 2: Create a reader for the VTI file
reader = vtk.vtkXMLImageDataReader()
# data_path = 'output/karman_VTK_P00_00010000.vti'
path= '/home/grzegorz/GITHUB/LBM/TCLB/output/poro_study/'
data_path = 'd2q9_poro_study_121perm_VTK_P00_00020253.vti'
reader.SetFileName(path + data_path)  # Update this path to your VTI file location
reader.Update()

# %% Step 3: (Optional) Extract the image data for further processing or visualization
image_data = reader.GetOutput()

# For example, you can get the dimensions of the image data
dims = image_data.GetDimensions()
print("Dimensions of the VTI file are:", dims)


# Assuming you have already read the image_data using vtkXMLImageDataReader
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
    
array_id = 2
print(f"Data for array is set to {i}")   
numpy_array = vtk_to_numpy(array)
 
# %% Assuming the data is 2D, reshape the flat numpy array into 2D
# dims = image_data.GetDimensions()
# numpy_array_2d = numpy_array.reshape(dims[1], dims[0])  # Adjust depending on how your data is organized


# ux = numpy_array[:,0].reshape(512, 512)  # Adjust depending on how your data is organized
# uy = numpy_array[:,1].reshape(512, 512)  # Adjust depending on how your data is organized
# data = np.sqrt(ux**2 +uy**2)

data = numpy_array.reshape(512, 512)
# Rotate the image by 180 degrees
data = np.flipud(np.fliplr(data))



# Step 4: Plot the 2D field using matplotlib
plt.figure(figsize=(14, 10))


from matplotlib.colors import LinearSegmentedColormap
colors = [(1, 1, 1), (0, 0, 1), (0, 0, 0)] # black, blue, white 
n_bins = 1000 # Discretizes the interpolation into bins 
cmap_name = 'custom_colormap' 
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

im = plt.imshow(data, cmap=cm, clim=(10, 11))
# im = plt.imshow(data, cmap='viridis')  # You can change the colormap as needed
# plt.colorbar()

# cbar = plt.colorbar(im, orientation='horizontal', fraction=0.1, pad=0.1)
# cbar.set_label('Intensity')  # You can customize the label

# plt.title('Velocity magnitude')

# plt.grid(which='major', color='#CCCCCC', linestyle='--')
# Optionally, you can customize the grid lines further
# plt.minorticks_on()  # Enable minor ticks if needed
# plt.grid(which='minor', color='#CCCCCC', linestyle=':')
plt.show()