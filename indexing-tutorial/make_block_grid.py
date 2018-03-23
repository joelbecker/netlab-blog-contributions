"""
Adapted from https://stackoverflow.com/questions/19586828/drawing-grid-pattern-in-matplotlib
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

N = 10

# make base data sets
data_1 = np.ones((N, N//2)) * 2
data_2 = np.ones((N, N//2)) * np.nan

# fill in some fake data_2
r1 = range(0, 4)
for i in r1:
    for j in range(0,2):
        data_2[i, j] = 1

r2 = range(4, 6)
for i in r2:
    for j in range(2, 3):
        data_2[i, j] = 2

r3 = range(6, 10)
for i in r3:
    for j in range(3, 5):
        data_2[i, j] = 3

# make a figure + axes
fig, ax = plt.subplots(1, 1, tight_layout=True)

# make color map
my_cmap = matplotlib.colors.ListedColormap([plt.get_cmap('tab20c').colors[6],
                                            plt.get_cmap('tab20c').colors[2],
                                            plt.get_cmap('tab20c').colors[14]])

# set the 'bad' values (nan) to be white and transparent
my_cmap.set_bad(color='w', alpha=0)

# draw the grid
for x in range(N + 1):
    ax.axhline(x, lw=2, color='w', zorder=5)
    ax.axvline(x, lw=2, color='w', zorder=5)

# Which version do you want to draw?
# Set draw = 1 for "full index" visualization
# Set draw = 2 for "blocked index" visualization
draw = 1

# draw the boxes
if draw is 1:
    ax.imshow(data_1, interpolation='none', cmap=my_cmap, extent=[0, N, 0, N//2], zorder=0)
    ax.axis('off')
    plt.savefig('block_index_1.png', transparent=True)
if draw is 2:
    ax.imshow(data_2, interpolation='none', cmap=my_cmap, extent=[0, N, 0, N//2], zorder=0)
    ax.axis('off')
    plt.savefig('block_index_2.png', transparent=True)
