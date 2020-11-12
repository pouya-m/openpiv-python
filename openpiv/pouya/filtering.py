# script to test some filtering techniques hopefully leading to better filtering algorythms. 


# issues with the current implimentation:
#---------------------------------------------

# 1- when there is nans in the data (a couple of them in the same area), the filters that evaluate the velocity against the nearby flow field (i.e. local_median filter), don't perform well.

# 2- in the current implimentation, the output from each filter affects the filters that are applied after it (u and v are passed through). this results in unwanted coupling behavior between filters.
# the nans problem mentioned above is a direct result of this. -> this was corrected, now u and v are not passed through and filters are uncoupled. 

# 3- some of the bad vectors can only be detected looking at the nearby flow field. currently, the only filter that does this is the local_median filter. maybe other filtering 
# schemes can be implimented that opperate based on the local flow field.

# 4- the local_median filter takes a global value for "velocity difference threshoulds" that are applied for the whole flow field. this means that small velocity vectors are allowed 
# to change as much as large velocity vectors are allowed. this can be improved by taking the local velocity scale into account, meaning that the threshould itself can depend on the 
# local velocity field! -> look at the enhanced_local_median filter bellow



from openpiv import tools, filters, validation
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter

def enhanced_local_median( u, v, b, m, size=1 ):
    """Detect bad vectors with a local median threshold that varies linearly with the local velocity.

    Parameters
    ----------
    u, v : 2d np.ndarray
        two dimensional arrays containing the u and v velocity components
        
    b : float
        threshould value for zero velocity
        
    m: float
        the slope for threshould value against velocity
        
    size: int
        the median filter kernel size
        
    Returns
    -------
    thr_u, thr_v: np.ndarray
        threshould values for the median filter for u and v velocity components

    mask: np.ndarray
        a boolean array. True elements corresponds to bad vectors
    """
    
    um = median_filter( u, size=2*size+1 )
    vm = median_filter( v, size=2*size+1 )
    thr_u = m*np.abs(um) + b
    thr_v = m*np.abs(vm) + b
    
    ind = ( np.abs( (u-um) ) > thr_u ) | ( np.abs( (v-vm) ) > thr_v )
    
    mask = np.zeros(u.shape, dtype=bool)
    mask[ind] = True
    
    return thr_u, thr_v, mask


if __name__ == "__main__":
    
    # read data
    fpath = r'F:\Re11_medium\theta180deg\Analysis\Unvalidated\theta180deg000005.dat'
    x, y, u, v, s2n = tools.read_data(fpath)

    # apply validation
    #*_, mask1 = validation.global_val(u1, v1, (-2000,2000), (-2000,4000))
    #*_, mask2 = validation.local_median_val(u2, v2, 500, 500, size=2)
    thr_u, thr_v, mask = enhanced_local_median(u, v, 250, 0.2, size=2)
    #plt.quiver(x, y, um, vm, color='b', units='xy', scale=50, width=2, minlength=0.1, minshaft=1.2)
    plt.imshow(np.sqrt(thr_u*thr_u + thr_v*thr_v), cmap='gray', extent=(0,1600,0,1200), vmin=100, vmax=1000, alpha=0.9)
    
    
    # replace bad vectors and show results
    u[mask] = np.nan
    v[mask] = np.nan
    u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
    print(f'\n - number of bad vectors: {sum(sum(mask))}')
    print(f' - u threshoulds: {thr_u.min()}, {thr_u.max()}\n - v thresoulds: {thr_v.min()}, {thr_v.max()}')

    valid = ~mask
    plt.quiver(x[mask], y[mask], u[mask], v[mask], color='r', units='xy', scale=50, width=2, minlength=0.1, minshaft=1.2)
    plt.quiver(x[valid], y[valid], u[valid], v[valid], color='b', units='xy', scale=50, width=2, minlength=0.1, minshaft=1.2)
    plt.show()
    