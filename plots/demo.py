import matplotlib.pyplot as plt
import numpy as np

def log_transform(im):
    '''returns log(image) scaled to the interval [0,1]'''
    try:
        (min, max) = (im[im > 0].min(), im.max())
        if (max > min) and (max > 0):
            return (np.log(im.clip(min, max)) - np.log(min)) / (np.log(max) - np.log(min))
    except:
        pass
    return im

a = np.ones((100,100))
for i in range(100): a[i] = i
f = plt.figure()
ax = f.add_subplot(111)
res = ax.imshow(log_transform(a))
# the colorbar drawn shows [0-1], but I want to see [0-99]
cb = f.colorbar(res)

plt.show()

