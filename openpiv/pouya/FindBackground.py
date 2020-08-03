# this script investigates the best/fastest way to find the background image
# I added a module in the tools.multiprocesser to calculate the background image faster
# utilizing multiprocessing capabilities

from openpiv import tools
import os, glob, time
import numpy as np
import matplotlib.pyplot as plt
from imageio import imread, imsave
import multiprocessing

'''
if __name__ == '__main__':
    directory = 'F:\Pouya'
    experiments = ['Insight_vs_OpenPIV']
    runs = ['free vibration']
    for experiment in experiments:
        for run in runs:
            run_path = os.path.join(os.path.join(directory, experiment), run)
            analysis_path = tools.create_directory(run_path) #creates the Analysis folder if not already there
            print(f'Processing experiment: {run_path}')
            data_dir = os.path.join(run_path, 'RawData')
            task = tools.Multiprocesser( data_dir=data_dir, pattern_a='*LA.TIF', pattern_b='*LB.TIF' )

            t1 = time.time()
            background_a, background_b = task.find_background(n_files=200, chunk_size=20, n_cpus=6)
            imsave(os.path.join(analysis_path, 'background_aa.TIF'), background_a)
            imsave(os.path.join(analysis_path, 'background_bb.TIF'), background_b)
            t2 = time.time()
            print(f'multiprocessing finished in: {(t2-t1):.2f}sec')

            background_a = tools.mark_background2(task.files_a[0:200], os.path.join(analysis_path, 'background_aa.TIF'))
            background_b = tools.mark_background2(task.files_b[0:200], os.path.join(analysis_path, 'background_bb.TIF'))
            t3 = time.time()
            print(f'single core finished in: {(t3-t2):.2f}sec')

# multiprocessing finishes in 96 sec, while single core takes 210 sec


'''
background = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\Analysis\\background_b_200.TIF')
img = imread('F:\\Pouya\\Insight_vs_OpenPIV\\free vibration\\RawData\\free vibration000001.T000.D000.P000.H000.LB.TIF')
fig, ax = plt.subplots(1,2)
np.clip(img, a_min=0, a_max=200,out=img)
ax[0].imshow(img, cmap='gray')
np.clip(img-background, a_min=0, a_max=200, out=img)
ax[1].imshow(img, cmap='gray')
plt.show()