import numpy as np
import matplotlib.pyplot as plt
import cv2


# %% 
path= '/home/grzegorz/GITHUB/LBM/TCLB/example/porous_media/'
image = cv2.imread(path+'porous_media_contrast_1024x256.png') 
# image = cv2.imread('japan_1024x640.png') 

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
# gray_image = image
# np_gray_image = np.array(gray_image)
# Convert to float
float_image = gray_image.astype(np.float32)

# Rescale to 0-1 range
normalized_image = float_image / 255.0

shape = gray_image.shape
print(f"input shape: {shape}")


# %% 
# Parameters for the Kozeny-Carman equation
K = 1.  # Kozeny constant, arbitrary choice for demonstration
S = 1.  # Specific surface area, arbitrary choice for demonstration

# Epsilon values to prevent division by zero in the denominator
epsilon = 1E-2

# Porosity range from 0 to 1 (not including 1 to avoid division by zero in the original equation)
phi = normalized_image #np.linspace(0.0, 0.9, 200)

# Prepare the plot


# Calculate and plot permeability for each epsilon value

def make_plot(x, title, cmap):
    plt.figure(figsize=(10, 7))
    plt.imshow(x, cmap=cmap)
    plt.colorbar()
    plt.title(f'{title}')
    plt.show()
    plt.close()

def save_img(x, h, w, cmap, title='generated_permability.png'):
    
#     plt.figure(figsize=(3.841, 7.195), dpi=100)
# ( your code ...)
# plt.savefig('myfig.png', dpi=1000)
    # plt.figure(figsize=(5.12, 1.024), dpi=100)
    # plt.axis('off')
    # plt.imshow(x, cmap='gist_gray') #  vmax=1000

    # plt.savefig(f'{title}', bbox_inches='tight', pad_inches=0, dpi=100)
    # plt.close()
    
    # w = 1000
    # h = 512
    # im_np = numpy.random.rand(h, w)
    
    
    my_dpi = 100
    fig = plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
    
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.imshow(x, cmap=cmap)
    fig.add_axes(ax)
    # plt.imshow(x, cmap='gist_gray')
    
    plt.axis('off')
    plt.savefig(f'{title}', bbox_inches='tight', pad_inches=0, dpi=my_dpi)
    


def rescale(background, new_min, new_max):
    # new_min = 0.01 +  1* np.min(background) # Define new minimum value
    # new_max = 0.99 * np.max(background)  # Define new maximum value
    min  = np.min(background)
    max = np.max(background)
    new_backgroud = new_min + ((background - min) * (new_max - new_min)) / (max - min)
    return new_backgroud
    
    
# Define the smooth limiter function based on the given C code
def smooth_limiter(x, max=10, steepness = 0.1):
    result = x*(3*x + 1)/(x+1)**2
    # result = max / (1 + np.exp(-steepness * (x - max)))
    return result


    # Adjusted Kozeny-Carman equation to include epsilon in the denominator
def Kozeny_Carman(phi,K,S):
    return (phi**3) / (K * ((1 - phi)**2 + epsilon)) * (1/S**2)

rephi = rescale(phi, 0.01, 0.99)
k = Kozeny_Carman(rephi,K,S)

make_plot(rephi, 'Input Porosity', 'gist_gray')
make_plot(k, 'Permability', 'gist_gray')

# ks = rescale(k, 0.01, 1000) 
# make_plot(ks, 'RescaledPermability')
# h, w, c = k.shape
h, w = k.shape
save_img(k, h, w, 'gist_gray')

# %%

# x = np.linspace(0,10,1000)
# y = smooth_limiter(x, max=10, steepness= 1)

# plt.plot(x,y)
# plt.plot(x,x)
# plt.grid()
