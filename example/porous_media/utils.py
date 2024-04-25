import matplotlib
import matplotlib.pyplot as plt
import numpy as np

SMALL_SIZE = 16
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


def linear_rescale(background, new_min, new_max):
    # new_min = 0.01 +  1* np.min(background) # Define new minimum value
    # new_max = 0.99 * np.max(background)  # Define new maximum value
    min  = np.min(background)
    max = np.max(background)
    new_backgroud = new_min + ((background - min) * (new_max - new_min)) / (max - min)
    return new_backgroud


def make_histogram(img, nbins = 100, title="Grayscale Histogram", output_name="Histogram.png"):
    # fig, ax = plt.subplots()

    my_dpi = 100
    fig = plt.figure(figsize=(512/my_dpi, 512/my_dpi), dpi=my_dpi)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    

    # ax.set_title(f"{title}")
    ax.set_xlabel("Grayscale value")
    # ax.set_ylabel("Count")
    # ax.set_xlim([-1.0, 1.0])  # <- named arguments do not work here
    # ax.plot(bin_edges[:-1], histogram)  # <- or here

    
    # Turn off tick labels
    ax.set_yticklabels([])
    # ax.set_xticklabels([])
    # to remove the tick marks as well as the label
    # ax.set_xticks([])
    ax.set_yticks([])
    
    # Turn off y-axis ticks and labels
    # ax.yaxis.set_visible(False)
    ax.yaxis.set_ticklabels([])
    
    
    # plt.gca().axes.get_yaxis().set_visible(False)
    # plt.gca().axes.yaxis.set_ticklabels([])
    # the histogram of the data
    x = img.flatten()
    n, bins, patches = ax.hist(x, nbins, density=True)
    fig.add_axes(ax)
    #densityTrue, draw and return a probability density: each bin will display the bin's raw count divided by the total number of counts and the bin width (density = counts / (sum(counts) * np.diff(bins))), so that the area under the histogram integrates to 1 (np.sum(density * np.diff(bins)) == 1)
    # plt.hist(x, nbins, density=True)
    # plt.axis('off')
    plt.savefig(f'{output_name}', bbox_inches='tight',pad_inches=0, dpi=my_dpi)
    plt.show()
    plt.close()
    

def make_plot(x, title, cmap, vmin=None, vmax=None, ticks =[0, 25, 50, 75, 100] ):
    plt.figure(figsize=(10, 7))
    plt.imshow(x, vmin=vmin, vmax=vmax, cmap=cmap)
    colorbar = plt.colorbar()
    colorbar.set_ticks(ticks)
    plt.title(f'{title}')
    plt.show()
    plt.close()
    
def save_img(x, h, w, cmap, vmin=None, vmax=None, title='generated_permability.png'):
    
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
    ax.imshow(x, vmin=vmin, vmax=vmax, cmap=cmap)
    fig.add_axes(ax)
    # plt.imshow(x, cmap='gist_gray')
    
    plt.axis('off')
    plt.savefig(f'{title}', bbox_inches='tight', pad_inches=0, dpi=my_dpi)
    plt.close()    