# test of static masking and the best value for intensity of inside-boundary points (zero or mean?)
# seems like setting it to zero produces the best results!

from openpiv import tools, pyprocess
import numpy as np
from imageio import imread, imsave
import skimage.draw as skdraw
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


# create the mask
mask = np.zeros((1192, 1600), dtype=np.uint8)
rr, cc = skdraw.disk((1192-350,200), 100, shape=mask.shape)
mask[rr, cc] = 255
imsave('pouya\mask.TIF', mask)

# apply the mask with inside points set to zero
mask = imread('pouya\mask.TIF')
frame_a = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LA.TIF')
frame_b = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LB.TIF')
frame_a[mask == 255] = 0
frame_b[mask == 255] = 0
u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=32, overlap=16, dt=0.0015, search_area_size=32, sig2noise_method='peak2peak')
x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=32, overlap=16 )
fig, ax = plt.subplots(1,3)
ax[0].quiver(x, y, u, v, units='xy')
circle = plt.Circle((200,350), 100, fill=False)
ax[0].add_artist(circle)
ax[0].set_title('Inside points set to zero')

# apply the mask with inside points set to the mean value
mask = imread('pouya\mask.TIF')
frame_a = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LA.TIF')
frame_b = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LB.TIF')
frame_a[mask == 255] = frame_a.mean()
frame_b[mask == 255] = frame_b.mean()
u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=32, overlap=16, dt=0.0015, search_area_size=32, sig2noise_method='peak2peak')
x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=32, overlap=16 )
ax[1].quiver(x, y, u, v, units='xy')
circle2 = plt.Circle((200,350), 100, fill=False)
ax[1].add_artist(circle2)
ax[1].set_title('Inside points set to mean value')

# original vector field without any masks
frame_a = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LA.TIF')
frame_b = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LB.TIF')
u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=32, overlap=16, dt=0.0015, search_area_size=32, sig2noise_method='peak2peak')
x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=32, overlap=16 )
ax[2].quiver(x, y, u, v, units='xy')
circle3 = plt.Circle((200,350), 100, fill=False)
ax[2].add_artist(circle3)
ax[2].set_title('No boundary set')

plt.show()

