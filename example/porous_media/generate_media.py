# %% imports

import numpy as np
import matplotlib.pyplot as plt
import noise
from utils import make_plot, save_img, make_histogram, linear_rescale
import cv2



# %% Attempt 2

# defaults
# shape = (256,1024)
# scale = 100.0
# octaves = 6
# persistence = 0.5
# lacunarity = 2.0
# defaults
shape = (1024,1536) # (heigh, width)


# Generate a random base each time
def make_world(shape, randbaseint=0):
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
                                        repeatx=shape[0], 
                                        repeaty=shape[1], 
                                        base=randbaseint)
            
    return world

world1 = make_world(shape, randbaseint=0)
world2 = make_world(shape, randbaseint=1)

make_plot(world1,title='Porosity - normal distribution', cmap='gray')
make_histogram(world1, title="Porosity - normal distribution ")  

velocity = np.sqrt(world1**2 + world2 **2)
make_plot(velocity,title='Porosity - Boltzmann (Chi) distribution', cmap='gray')
make_histogram(velocity, title="Porosity - Boltzmann (Chi) distribution") 

save_img(velocity, h=shape[0], w=shape[1], cmap='gist_gray', title='generated_porosity_chi_distribution.png')


# Adjusted Kozeny-Carman equation to include epsilon in the denominator
def Kozeny_Carman(phi,K=1E0,S=1E-0, epsilon = 1E-2):
    return (phi**3) / (K * ((1 - phi)**2 + epsilon)) * (1/S**2)

kc_world = Kozeny_Carman(velocity)
make_histogram(kc_world, title="Raw KC permability from Chi distributed porosity")
make_plot(kc_world, title='Raw KC permability from Chi distributed porosity', cmap='gray')


def tanh_limiter(signal, threshold):
    return np.tanh(signal / threshold)

kc_world_compressed = tanh_limiter(kc_world, 0.2)
# kc_world_compressed= np.log(np.abs(kc_world)+1E-2)
make_histogram(kc_world_compressed, title="kc_world_compressed")
make_plot(kc_world_compressed,title='kc_world_compressed', cmap='gray')
save_img(kc_world_compressed, h=shape[0], w=shape[1], cmap='gist_gray', title='kc_generated_permability.png')
# %%


# image = cv2.imread('porous_media_1024x512.png')
image = cv2.imread('porosity.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
float_image = gray_image.astype(np.float32)
normalized_image = float_image / 255.0 # Rescale to 0-1 range

make_histogram(normalized_image, title="ground truth guess")

# %%
