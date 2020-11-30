from openpiv import tools
import os, glob, time
import numpy as np
import matplotlib.pyplot as plt
from imageio import imsave

if __name__ == "__main__":
    path = r'F:\Re11_small\theta000deg\RawData'
    t1 = time.time()
    task = tools.Multiprocesser(path, '*LA.TIF', '*LB.TIF')
    # bga, bgb = task.find_background(250, 100, 6)
    bga, bgb = task.find_background2(250)
    print(f'finished in {time.time()-t1} sec')
    imsave(os.path.join(path, 'background_a.TIFF'), bga)
    imsave(os.path.join(path, 'background_b.TIFF'), bgb)

    bga = tools.imread(os.path.join(path, 'background_b.TIFF'))
    A = tools.imread(os.path.join(path, 'theta000deg000001.T000.D000.P000.H000.LB.TIF'))
    plt.subplot(121)
    plt.imshow(A, cmap='gray',vmin=0,vmax=400)
    plt.subplot(122)
    plt.imshow(A-bga, cmap='gray',vmin=0,vmax=400)
    plt.show()