# this script facilitates the validation phase (adjustment of filters/validation parameters to identify bad vectors)
# this is done in two phases first a bunch of image pairs are processed to generate a sample of piv results, then in
# phase 2 different filter parameters can be tried out to find appropriate values for them through trial and error.

# after phase 2, it should be checked if a single pass of replacing bad vectors "filters.replace_outliers()"
# can effectively replace all the empty spots or instead a multiple pass is required.

from openpiv import tools, pyprocess, validation, filters
import os, glob
import numpy as np
from functools import partial

def preprocess( args, run_name ):
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
    save_file = tools.create_path(file_a, 'Analysis/Validation')
    tools.save(x, y, u, v, sig2noise, save_file+'.dat')
    return (counter)

def validate ( args, run_name ):
    """the function to filter bad vectors"""

    #unpacking the arguments
    file_a, file_b, counter = args
    print(counter+1)

    # validation process
    save_file = tools.create_path(file_a, 'Analysis/Validation')
    x, y, u, v, sig2noise = tools.read_data(save_file+'.dat')
    u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
    u1, v1 = u.copy(), v.copy()
    u, v, mask1 = validation.sig2noise_val( u, v, sig2noise, threshold = 1.0 )
    u, v, mask2 = validation.global_val( u, v, (-2000, 2000), (-2000, 4000) )
    u, v, mask3 = validation.local_median_val(u, v, 500, 500, size=2)
    #u, v, mask4 = validation.global_std(u, v, std_threshold=3)
    mask = mask1 | mask2 | mask3
    tools.save(x, y, u1, v1, mask, save_file+'_Validated.dat')


if __name__ == '__main__':
    directory = 'C:\\Users\\Asus\\Desktop'
    experiments = ['UI']
    runs = ['Dummy Data']
    for experiment in experiments:
        for run in runs:
            Run_path = os.path.join(directory, experiment + f'/{run}')
            RawData_path = os.path.join(Run_path, 'Raw Data')

            Analysis_path = tools.create_directory(Run_path) #creates the Analysis folder if not already there
            validation_path = tools.create_directory(Run_path, 'Analysis/Validation') #creates the Validation folder if not already there
            print(f'Processing experiment: {Run_path}')

            task = tools.Multiprocesser( data_dir=RawData_path, pattern_a='*LA.TIF', pattern_b='*LB.TIF' )
            task.n_files = 4
            phase1 = partial(preprocess, run_name=run)
            phase2 = partial(validate, run_name=run)
            res = task.run( func = phase1, n_cpus=2)
            print(res)
