# this script facilitates the Main Processing phase of our PIV data analysis
# basically this includes piv process, detection and replacement of bad vectors, 
# smoothing ,scalling and field manipulations. 

from openpiv import tools, pyprocess, validation, filters, smoothn, scaling
import os, glob, time
import numpy as np
from functools import partial
from imageio import imread, imsave
import warnings
warnings.filterwarnings("ignore")


def ProcessPIV( args, bg_a, bg_b):
    """The function to process the image pairs."""

    #unpacking the arguments
    file_a, file_b, counter = args
    
    # read images into numpy arrays
    frame_a  = imread( file_a ) - bg_a
    frame_b  = imread( file_b ) - bg_b
    print(counter+1)
    
    # process image pair with piv algorithm.
    u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, \
        window_size=32, overlap=16, dt=0.0015, search_area_size=32, sig2noise_method='peak2peak')
    x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=32, overlap=16 )

    # validation process
    u, v, mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = 1.0 )
    u, v, mask2 = validation.global_val( u, v, (-2000, 2000), (-2000, 4000) )
    u, v, mask3 = validation.local_median_val(u, v, 500, 500, size=2)
    #u, v, mask4 = validation.global_std(u, v, std_threshold=3)
    mask = mask1 | mask2 | mask3
    u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
    u, *_ = smoothn.smoothn(u, s=0.5)
    v, *_ = smoothn.smoothn(v, s=0.5)
    x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = 7.4 )
    x, y, u, v, sig2noise = tools.manipulate_field(x, y, u, v, sig2noise, mode='rotateCW')
    #x, y, u, v, sig2noise = tools.manipulate_field(x, y, u, v, sig2noise, mode='flipUD')
    save_file = tools.create_path(file_a)
    tools.save(x, y, u, v, sig2noise, save_file+'.dat')


if __name__ == '__main__':
    directory = 'F:\Pouya'
    experiments = ['Insight_vs_OpenPIV']
    runs = ['free vibration']
    t1 = time.time()
    for experiment in experiments:
        for run in runs:
            run_path = os.path.join(os.path.join(directory, experiment), run)
            analysis_path = tools.create_directory(run_path) #creates the Analysis folder if not already there
            print(f'Processing run: {experiment} / {run}')
            data_dir = os.path.join(run_path, 'RawData')
            task = tools.Multiprocesser( data_dir=data_dir, pattern_a='*LA.TIF', pattern_b='*LB.TIF' )
            background_a, background_b = task.find_background(n_files=200, chunk_size=20, n_cpus=6)
            imsave(os.path.join(analysis_path, 'background_a.TIF'), background_a)
            imsave(os.path.join(analysis_path, 'background_b.TIF'), background_b)
            #background_a = imread(os.path.join(analysis_path, 'background_a.TIF'))
            #background_b = imread(os.path.join(analysis_path, 'background_b.TIF'))
            task.n_files = 10
            Process = partial(ProcessPIV, bg_a=background_a, bg_b=background_b)
            task.run( func = Process, n_cpus=6 )

    t2 = time.time()
    print(f'process finished in: {(t2-t1):.2f}sec')