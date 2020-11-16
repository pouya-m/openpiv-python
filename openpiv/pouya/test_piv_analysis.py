# here I test the general piv results and try to improve them

# to do:
# 1- impliment an extra step in the piv algorythm that limits the maximum allowed displacement to a fraction of the window size (1/4 would be a good value), and if the displacement is
#    higher then we could try the second peak to see if that gives a more reasonable value. from my early tests this can impact 2/3 of all the bad vectors and try to 
#    replace them with actuall data (from the second highest peak) rather than conducting an interpolation like we do in the validation process.

# 2- investigate window deformation and multi-stage piv algorythms.

from openpiv import pyprocess, tools
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    path_a = r'C:\Users\Asus\Desktop\Dummy Data\piv comparison\RawData\theta180deg000001.T000.D000.P000.H000.LA.TIF'
    path_b = r'C:\Users\Asus\Desktop\Dummy Data\piv comparison\RawData\theta180deg000001.T000.D000.P000.H000.LB.TIF'
    frame_a = tools.imread(path_a)
    frame_b = tools.imread(path_b)
    u, v, s2n = pyprocess.extended_search_area_piv(frame_a, frame_b, window_size=32, overlap=16, dt=1, search_area_size=32,
        corr_method='fft', sig2noise_method='peak2peak', width=2)
    x, y = pyprocess.get_coordinates(frame_a.shape, 32, 16)
    save_path = r'C:\Users\Asus\Desktop\Dummy Data\piv comparison\Analysis\openpiv_32_16_0.25.dat'
    tools.save(x, y, u, v, s2n, save_path)
    
    x, y, u, v, s2n = tools.read_data(r'C:\Users\Asus\Desktop\Dummy Data\piv comparison\Analysis\openpiv_32_16_0.25.dat')
    secVec = (s2n==-1)
    failed = (s2n==-2)
    reg = (s2n>=0)
    plt.quiver(x[reg], y[reg], u[reg], v[reg], units='xy', scale=0.1, color='b')
    plt.quiver(x[secVec], y[secVec], u[secVec], v[secVec], units='xy', scale=0.1, color='k')
    plt.quiver(x[failed], y[failed], u[failed], v[failed], units='xy', scale=0.1, color='r')
    plt.show()