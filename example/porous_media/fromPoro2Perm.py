import numpy as np
import matplotlib.pyplot as plt
import cv2

image = cv2.imread('porous_media.png') 
# image = cv2.imread('japan_1024x640.png') 

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
np_gray_image = np.array(gray_image)
shape = gray_image.shape


# Parameters for the Kozeny-Carman equation
K = 200  # Kozeny constant, arbitrary choice for demonstration
S = 1  # Specific surface area, arbitrary choice for demonstration

# Epsilon values to prevent division by zero in the denominator
epsilon = 1E-3

# Porosity range from 0 to 1 (not including 1 to avoid division by zero in the original equation)
phi = np_gray_image #np.linspace(0.0, 0.9, 200)

# Prepare the plot
plt.figure(figsize=(10, 7))

# Calculate and plot permeability for each epsilon value


    # Adjusted Kozeny-Carman equation to include epsilon in the denominator
def Kozeny_Carman(phi,K,S):
    return (phi**3) / (K * ((1 - phi)**2 + epsilon)) * (1/S**2)

k = Kozeny_Carman(phi,K,S)


# Define the smooth limiter function based on the given C code
def smooth_limiter(x):
    limit = 1000.0
    steepness = 0.1  # Adjust steepness for a smoother or sharper transition
    result = limit / (1 + np.exp(-steepness * (x - limit)))
    return result


# plt.imshow(gray_image, cmap='gist_gray')
# plt.colorbar()
# plt.title(f'Porosity')
# plt.show()

# plt.imshow(smooth_limiter(k), cmap='gist_gray')
# plt.colorbar()
# plt.title(f'Clipped Permability')
# plt.show()

plt.axis('off')
plt.imshow(k, cmap='gist_gray')
# plt.colorbar()
# plt.title(f'Permability')
# plt.show()

plt.savefig('generated_permability.png', bbox_inches='tight', pad_inches=0, dpi=100)
plt.close()
