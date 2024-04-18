# %% imports

import numpy as np
import matplotlib.pyplot as plt
import noise
from utils import make_plot, save_img
import cv2

# %% attempt 1 

def generate_porous_media(width, height, scale=0.1, minmax_range=(0, 1.), threshold=0.5, binary=False):
    """
    Generates a 2D porous media using Perlin noise.

    Parameters:
    - width, height: dimensions of the generated media.
    - scale: controls the level of detail of the noise.
    - threshold: threshold to decide if a point is part of the pore space or solid.

    Returns:
    - A 2D numpy array representing the porous media.
    """
    porosity = np.zeros((height, width))
    
    for i in range(height):
        for j in range(width):
            noise_value = noise.pnoise2(i * scale, j * scale)
            porosity[i, j] = noise_value
            if binary:
              if noise_value < threshold:
                  porosity[i, j] = 1  # Pore space
              else:
                  porosity[i, j] = 0  # Solid
    
    min_value, max_value = minmax_range
    porosity_norm = (porosity - np.min(porosity)) / (np.max(porosity) - np.min(porosity))
    porosity_squeezed = min_value + (max_value - min_value) * porosity_norm

    return porosity_squeezed

# Example usage
minmax_range=(0.01, 0.999)
width_in_pixels, height_in_pixels = 1024, 256
porous_media = generate_porous_media(width_in_pixels, 
                                     height_in_pixels, 
                                     scale=0.1, minmax_range=minmax_range, 
                                     threshold=0.5, binary=False)


make_plot(porous_media,title='Attempt v0', cmap='gray')


# %% Attempt 2

# defaults
# shape = (1024,1024)
# scale = 100.0
# octaves = 6
# persistence = 0.5
# lacunarity = 2.0
# defaults
shape = (1024,1024)
scale = 100.0
octaves = 10
persistence = 0.7
lacunarity = 2.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=1024, 
                                    repeaty=1024, 
                                    base=0)
        
make_plot(world,title='Attempt v1', cmap='gray')
        
save_img(world, shape[0], shape[1], 'gist_gray')
        
# toimage(world).show()


# plt.imshow(world, cmap='gray') #, vmin=0, vmax=1)
# plt.colorbar()
# %%

import cv2

# read image
image = cv2.imread('porous_media_1024x512.png')
# calculate mean value from RGB channels and flatten to 1D array
# vals = im.mean(axis=2).flatten()

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
float_image = gray_image.astype(np.float32)
normalized_image = float_image / 255.0 # Rescale to 0-1 range

def make_histogram(img, nbins = 256):
    fig, ax = plt.subplots()
    ax.set_title("Grayscale Histogram")
    ax.set_xlabel("grayscale value")
    ax.set_ylabel("pixel count")
    # ax.set_xlim([-1.0, 1.0])  # <- named arguments do not work here
    # ax.plot(bin_edges[:-1], histogram)  # <- or here
    x = img.flatten()

    # the histogram of the data
    n, bins, patches = ax.hist(x, nbins, density=True)

make_histogram(normalized_image)
