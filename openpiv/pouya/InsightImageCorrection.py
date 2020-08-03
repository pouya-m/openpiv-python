# this script investigates the quality of our PIV images and why they can not be viewed properly.
# the problem turns out to be the scaling of the intensity value. the intensity range in our images is 
# from 0 to 4095, but there is hardly any data (info) above 500. so if we cap the data around 500 or limit
# the viewing range to this value the images become more clear.

from openpiv import tools
import matplotlib.pyplot as plt
import skimage.exposure as ski_expo


img = tools.imread('E:\\Data\\PIV_Comparison\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LB.TIF')

fig, ax = plt.subplots(2, 2)
val, center = ski_expo.histogram(img)
ax[0,0].imshow(img,cmap='gray')
ax[0,1].plot(center, val)
img_correccted = ski_expo.rescale_intensity(img, in_range=(0,600), out_range=(0,4095))
#img = ski_expo.adjust_gamma(img, gamma=0.9)
val, center = ski_expo.histogram(img_correccted)
ax[1,0].imshow(img_correccted,cmap='gray')
ax[1,1].plot(center, val)
plt.tight_layout()
plt.show()

# the difference is huge, is this gonna have a significant effect on the PIV results?
# Let's try to clip the values above 600 and see if the results are similar:

fig, ax = plt.subplots(1, 2)
ax[0].imshow(img_correccted, cmap='gray')

n=0
img_clipped = img.copy()
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img_clipped[i, j] > 600:
            img_clipped[i, j] = 600
            n += 1
ax[1].imshow(img_clipped, cmap='gray')
plt.tight_layout()
plt.show()
print(n)

# the similarity of the these plots indicate that the effect is probably only aesthetic and it has
# probably little effect on the PIV results. only the scale of the plot is different. Also only about 8200
# points had intensity higher than 600 which acounts for less than 0.5 percent of the points. insignificant!
# infact we can just limit the color map extent:

plt.imshow(img, cmap='gray', vmin=0, vmax=500)
plt.tight_layout()
plt.show()
