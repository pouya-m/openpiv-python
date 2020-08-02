# this script facilitates the Main Processing phase of our PIV data analysis
# basically the same thing will be done as the validation phase but this time 
# we will do it for the whole data set and also bad vector replacement, smoothing 
# ,scalling and field manipulation will be done. 

from openpiv import tools, pyprocess, validation, filters, smoothn, scaling
import os, glob
import numpy as np
from functools import partial
import time

def main_process( args, run_name ):
    """The function to process the image pairs."""

    #unpacking the arguments
    file_a, file_b, counter = args
    
    # read images into numpy arrays
    frame_a  = tools.imread( file_a )
    frame_b  = tools.imread( file_b )
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
    x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode='rotateCW')
    x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode='flipUD')
    save_file = tools.create_path(file_a, run_name, counter)
    tools.save(x, y, u, v, mask, save_file+'.dat')



if __name__ == '__main__':
    directory = 'F:\Pouya'
    experiments = ['OpenPIV_Test1_CleanCylinder']
    runs = ['Fixed', 'Free Vibration']
    t1 = time.time()
    for experiment in experiments:
        for run in runs:
            path = tools.create_directory(directory, experiment, run) #creates the Analysis folder if not already there
            print(f'Processing experiment: {path}')

            task = tools.Multiprocesser( data_dir=path, pattern_a='*LA.TIF', pattern_b='*LB.TIF' )
            #task.n_files = 100
            run_func = partial(main_process, run_name=run)
            task.run( func = run_func, n_cpus=8 )
    t2 = time.time()
    print(f'process finished in: {(t2-t1):.2f}sec')

