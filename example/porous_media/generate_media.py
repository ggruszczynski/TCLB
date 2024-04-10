import numpy as np
import matplotlib.pyplot as plt
from noise import pnoise2

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
            noise_value = pnoise2(i * scale, j * scale)
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
                                     scale=0.05, minmax_range=minmax_range, 
                                     threshold=0.5, binary=False)

# Calculate the figure size in inches for a given DPI (e.g., 100)
dpi = 207
fig_width = width_in_pixels / dpi  # Width in inches
fig_height = height_in_pixels / dpi  # Height in inches

plt.figure(figsize=(fig_width, fig_height), dpi=dpi)

plt.imshow(porous_media, cmap='gray', vmin=0, vmax=1)


# Save the figure without any decorations
plt.axis('off')
# plt.title('Simulated Porous Media')
# plt.colorbar()
# plt.grid()
# plt.show()
plt.savefig('generated_porous_media.png', bbox_inches='tight', pad_inches=0, dpi=dpi)
plt.close()
