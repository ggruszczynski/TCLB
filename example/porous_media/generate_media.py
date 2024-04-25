# %% imports

import numpy as np
import matplotlib.pyplot as plt
import noise
from utils import make_plot, save_img, make_histogram, linear_rescale
import cv2

def smooth_limiter(x, max=10, steepness = 0.1):
    result = x*(3*x + 1)/(x+1)**2
    # result = max / (1 + np.exp(-steepness * (x - max)))
    return result

# Adjusted Kozeny-Carman equation to include epsilon in the denominator
def Kozeny_Carman(phi,K=1E0,S=1E-0, epsilon = 1E-2):
    return (phi**3) / (K * ((1 - phi)**2 + epsilon)) * (1/S**2)

def tanh_limiter(signal, threshold):
    return np.tanh(signal / threshold)

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
# %% Attempt 2

# defaults
# shape = (256,1024)
# scale = 100.0
# octaves = 6
# persistence = 0.5
# lacunarity = 2.0
# defaults
shape = (512,512) # (heigh, width)


# Generate a random base each time
world1 = make_world(shape, randbaseint=0)
world2 = make_world(shape, randbaseint=1)

reworld1 = linear_rescale(world1,0.1,100)
# world2 = linear_rescale(world2,0.1,100)              
make_plot(reworld1,title='Porosity: normal distribution', cmap='gray')
make_histogram(reworld1, output_name="Porosity_normal_distribution.png")  
save_img(reworld1, h=shape[0], w=shape[1], cmap='gist_gray', title=f'generated_porosity_normal_distribution_{shape[1]}x{shape[0]}.png')


velocity = np.sqrt(world1**2 + world2 **2)
revelocity = linear_rescale(velocity,0.1,100)    
make_plot(revelocity,title='Porosity: Chi distribution', cmap='gray')
make_histogram(revelocity, output_name='Porosity_Chi_distribution.png') 
save_img(revelocity, h=shape[0], w=shape[1], cmap='gist_gray', title=f'generated_porosity_chi_distribution_{shape[1]}x{shape[0]}.png')


# kc_normal = Kozeny_Carman(linear_rescale(world1,0,1))
# kc_normal = Kozeny_Carman(world1)
kc_normal = Kozeny_Carman(np.abs(world1))
rekc_normal = linear_rescale(kc_normal,0.1,100)
make_histogram(rekc_normal, output_name="kc_permability_from_abs_normal_porosity.png")
make_plot(rekc_normal, title='generated_kc_abs_normal_permability', cmap='gray')
save_img(rekc_normal, h=shape[0], w=shape[1], cmap='gist_gray', title=f'generated_kc_abs_normal_permability_{shape[1]}x{shape[0]}.png')


kc_chi_world = Kozeny_Carman(velocity)
rekc_chi_world = linear_rescale(kc_chi_world,0.1,100)
make_histogram(rekc_chi_world, output_name="kc_permability_from_Chi_porosity.png")
make_plot(rekc_chi_world, title='generated_kc_chi_permability', cmap='gray')
save_img(rekc_chi_world, h=shape[0], w=shape[1], cmap='gist_gray', title=f'generated_kc_chi_permability_{shape[1]}x{shape[0]}.png')


kc_world_compressed = tanh_limiter(kc_chi_world, 0.2)

# kc_world_compressed= np.log(np.abs(kc_world)+1E-2)
rekc_world_compressed=linear_rescale(kc_world_compressed,0.1,100)
make_histogram(rekc_world_compressed, output_name="tanh_kc_permability_from_Chi_porosity.png")
make_plot(rekc_world_compressed,title='generated_tanh_kc_chi_permability', cmap='gray')
save_img(rekc_world_compressed, h=shape[0], w=shape[1], cmap='gist_gray', title=f'generated_tanh_kc_chi_permability_{shape[1]}x{shape[0]}.png')
# %%


# # image = cv2.imread('porous_media_1024x512.png')
# image = cv2.imread('porosity.png')
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
# float_image = gray_image.astype(np.float32)
# normalized_image = float_image / 255.0 # Rescale to 0-1 range

# make_histogram(normalized_image, title="ground truth guess")

# # %%
