import shutil
import os
import cv2
import numpy as np
import glob

# Define the source image file
# source_image1 = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/Porosity_Chi_distribution.png'
# source_image2 = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/generated_kc_chi_permability_512x512.png'



# Define the destination directory where the copied images will be saved

# batch1
# subdir = 'poro_study_tanh_kc_chi_permability/'
# source_image1_hist = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/tanh_kc_permability_from_Chi_porosity.png'
# source_image2_background = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/generated_tanh_kc_chi_permability_512x512.png'


#batch2
# subdir = 'poro_study_porosity_chi_distribution/'
# source_image1_hist = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/Porosity_Chi_distribution.png'
# source_image2_background = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/generated_porosity_chi_distribution_512x512.png'

#batch3
subdir = 'poro_study_porosity_normal_distribution/'
source_image1_hist = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/Porosity_normal_distribution.png'
source_image2_background = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/generated_porosity_normal_distribution_512x512.png'


# DESTINATION
destination_directory = '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/script_output/' + subdir

# Define the starting index for naming the copied images
start_index = 1000

# Define the number of times you want to copy the image
# num_files_to_generate = len(os.listdir(destination_directory))
num_files_to_generate = 333

# Loop through and copy the image N times
for i in range(num_files_to_generate):
    new_filename = f'imghist_{start_index + i +1}.png'
    shutil.copyfile(source_image1_hist, destination_directory + new_filename)
    print(f'Copied {source_image1_hist} to {destination_directory + new_filename}')

for i in range(num_files_to_generate):
    new_filename = f'imgbackground_{start_index + i +1}.png'
    shutil.copyfile(source_image2_background, destination_directory + new_filename)
    print(f'Copied {source_image2_background} to {destination_directory + new_filename}')




print(f'Images copied successfully to {destination_directory}')

def join_images_side_by_side_cv(img1_path, img2_path, img3_path, output_path):
    image1 = cv2.imread(img1_path)
    image2 = cv2.imread(img2_path)
    image3 = cv2.imread(img3_path)
    # Resize images to the same height
    # height = min(image1.shape[0], image2.shape[0])
    # image1 = cv2.resize(image1, (int(image1.shape[1] * height / image1.shape[0]), height))
    # image2 = cv2.resize(image2, (int(image2.shape[1] * height / image2.shape[0]), height))
    image2 = cv2.resize(image2, (512, 512))
    image3 = cv2.resize(image3, (512, 512))
    
    # Concatenate images horizontally
    new_image = np.hstack((image1, image2, image3))

    # Save the new image
    cv2.imwrite(output_path, new_image)


def list_and_sort_files(pattern):
    """List files matching the pattern and sort them."""
    files = glob.glob(pattern)
    files.sort()
    return files
  
# List and sort the files
H_files = list_and_sort_files(destination_directory+'H_*.png')
a_files = list_and_sort_files(destination_directory+'imgbackground_*.png')
b_files = list_and_sort_files(destination_directory+'imghist_*.png')


# Assuming both lists are the same length and correctly matched
counter =1000
for H_file, a_file, b_file in zip(H_files, a_files, b_files):
    counter = counter + 1
    output_filename = destination_directory+f"joined3_{counter}.png"  # Customize the output filename as needed
    join_images_side_by_side_cv(H_file, a_file, b_file, output_filename)
    print(f'joined {output_filename}')


import subprocess

# Define the ffmpeg command as a list of arguments
ffmpeg_command = [
    'ffmpeg',
    '-framerate', '24',
    '-pattern_type', 'glob',
    '-i', f'{destination_directory}joined3_*.png',
    # '-vf', 'scale=-2:512', # -2 value in the scale parameter is a special value that maintains the aspect ratio of the input video while resizing it
    '-vf', 'scale=1536:512',
    '-c:v', 'libx264',
    '-profile:v', 'high',
    '-b:v', '5M',
    '-crf', '17',
    '-pix_fmt', 'yuv420p',
    f'{destination_directory}joined3output.mp4'
]

# Execute the ffmpeg command, automatically confirming any prompts
subprocess.run(ffmpeg_command, text=True, input='y\n')
