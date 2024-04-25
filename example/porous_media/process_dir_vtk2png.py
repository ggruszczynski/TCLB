
# %%
# Step 1: Import the necessary libraries
import vtk

import matplotlib.pyplot as plt
import numpy as np
from utils import make_plot, save_img
from matplotlib.colors import LinearSegmentedColormap
import glob, os

from vtk_utils import check_arrays, getdata_1D

# %% Step 2: Create a reader for the VTI file
reader = vtk.vtkXMLImageDataReader()
# data_path = 'output/karman_VTK_P00_00010000.vti'
# directory_path= '/home/grzegorz/GITHUB/LBM/TCLB/output/poro_study/'

# file_path = 'd2q9_poro_study_121perm_VTK_P00_00002003.vti'
# subdir = 'poro_study_kc_abs_normal_permability/'

# subdir = 'poro_study_tanh_kc_chi_permability/'
# subdir = 'poro_study_porosity_chi_distribution/'
subdir = 'poro_study_porosity_normal_distribution/'


directory_path = '/home/grzegorz/GITHUB/LBM/TCLB/output/' + subdir

# data_path = directory_path + file_path
shape = (512,512)
data_path = glob.glob(directory_path + '*.vti')[10]

check_arrays(data_path)
data=getdata_1D(data_path, array_id=2, reader=reader, shape=shape) 

colors = [(1, 1, 1), (0, 0, 1), (0, 0, 0)] # black, blue, white 
n_bins = 1000 # Discretizes the interpolation into bins 
cmap_name = 'custom_colormap' 
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)


make_plot(data, "title", cm, vmin=10.05, vmax=11, ticks=[10, 10.2, 10.4, 10.6, 10.8, 11]) 
save_img(data, h=shape[0], w=shape[1], cmap=cm, vmin=10, vmax=11, title=f'uff.png')

output_dir = 'script_output/' + subdir

# Check if the directory exists
if not os.path.exists(output_dir):
    # Create the directory if it does not exist
    os.makedirs(output_dir)
    print(f"Directory '{output_dir}' created successfully")
else:
    print(f"Directory '{output_dir}' already exists")


# %% Step 2:    
counter = 1000
vti_files = glob.glob(directory_path + '*.vti')
# List of strings to check for endings
endings_to_remove = ["00000001.vti", "00000002.vti", "00000003.vti"]

# Remove items from the list ending with any string in the endings_to_remove list
vti_files = [item for item in vti_files if not any(item.endswith(ending) for ending in endings_to_remove)]

vti_files_sorted = sorted(vti_files)
# for file_path in glob.glob(directory_path + '*.vti'):
for file in vti_files_sorted:
    print(f"processing {counter}:  {file}")
    reader = vtk.vtkXMLImageDataReader()
    counter = counter +1
    data=getdata_1D(file, array_id=2, reader=reader, shape=shape) 
    save_img(data, h=shape[0], w=shape[1], cmap=cm, vmin=10.05, vmax=11, title=output_dir + f'H_{counter}.png')


# %% Step 2: 

import subprocess

# Define the ffmpeg command as a list of arguments
ffmpeg_command = [
    'ffmpeg',
    '-framerate', '24',
    '-pattern_type', 'glob',
    '-i', f'{output_dir}H_*.png',
    # '-vf', 'scale=-2:512', # -2 value in the scale parameter is a special value that maintains the aspect ratio of the input video while resizing it
    '-vf', 'scale=512:512',
    '-c:v', 'libx264',
    '-profile:v', 'high',
    '-b:v', '5M',
    '-crf', '17',
    '-pix_fmt', 'yuv420p',
    f'{output_dir}_ink_H_output.mp4'
]

# Execute the ffmpeg command, automatically confirming any prompts
subprocess.run(ffmpeg_command, text=True, input='y\n')

