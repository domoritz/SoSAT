import matplotlib.pyplot as plt
import numpy as np
from pylab import figure, cm
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator, LogFormatter 
from mpl_toolkits.axes_grid1 import ImageGrid

def get_demo_image():
    import numpy as np
    z = np.array([[12.704, 13.204, 7.094, 7.335, 8.020, 11.808, 13.329, 15.012, 14.884, 16.644], [38.979, 38.896, 28.965, 30.775, 3.655, 4.616, 4.448, 4.873, 5.713, 6.724], [4.894, 4.870, 4.616, 4.681, 6.786, 6.134, 7.686, 9.412, 9.340, 10.054], [7.538, 7.540, 7.511, 7.529, 7.423, 7.513, 7.631, 8.003, 8.653, 8.853], [78.95,78.95,78.95,78.95,78.95,78.95,78.95,78.95,78.95,78.95], [9.842,9.842,9.842,9.842,9.842,9.842,9.842,9.842,10.385, 10.082], [4.31,4.31,4.31,4.31,4.31,4.31,4.31,4.31,4.31,4.31],[6.11, 6, 5.953, 6.158, 5.769, 6.282, 5.583, 5.887, 6.061, 5.656], [4.551, 4.352, 4.602, 4.512, 4.477, 4.427, 4.475, 4.422, 4.511, 4.563], [8.313,8.313,8.313,8.313,8.313,8.313,8.313,8.313,8.313,8.313], [15.184,15.184,15.184,15.184,15.184,15.184,15.184,15.184,15.184,15.184]])
    return z/3.0 

fig = plt.figure()
Z = get_demo_image() # demo image


vmin, vmax = 1, 80/3.0
ax = fig.add_subplot(111)
#im = ax.imshow(Z, origin="lower", vmin=vmin, vmax=vmax, interpolation="nearest")
im = ax.matshow(Z, vmin=vmin, extent=(1,11,11,0), vmax=vmax, norm=LogNorm(vmin=vmin, vmax=vmax))
l_f = LogFormatter(15, labelOnlyBase=False) 
cb = plt.colorbar(im, format=l_f, ticks=[1,1.5,2,2.5,3,4,5,6,8,10,12.5,15,25])
cb.set_label("runtime (seconds)")
ax.set_xlabel("number of threads")
ax.set_xticks(np.arange(10)+1)
ax.set_ylabel("number of factorings")
ax.set_yticks(np.arange(11))

plt.show()

