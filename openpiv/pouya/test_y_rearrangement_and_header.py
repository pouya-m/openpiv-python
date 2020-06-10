
from openpiv import tools, process, scaling, pyprocess, validation, filters
import numpy as np
import time
import os
import pylab

path = os.path.dirname(os.path.abspath(__file__))
frame_a  = tools.imread( os.path.join(path,'./00020359.bmp'))
frame_b  = tools.imread( os.path.join(path,'./00020360.bmp'))
#pylab.imshow(frame_a,cmap='gray')
#pylab.show()

ws=32
ol=16
sa=64

'''
t0=time.time()
u, v, sig2noise = process.extended_search_area_piv( frame_a.astype(np.int32), frame_b.astype(np.int32), \
    window_size=ws, overlap=ol, dt=0.02, sig2noise_method='peak2peak' )
x, y = process.get_coordinates( image_size=frame_a.shape, window_size=ws, overlap=ol )
u, v, mask = validation.sig2noise_val( u, v, sig2noise, threshold = 1.3 )
u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = 96.52 )
tools.save(x, y, u, v, mask, os.path.join(path,'./exp1_001_c64.txt'))
t1=time.time()
tools.display_vector_field(os.path.join(path,'./exp1_001_c64.txt'), scale=50, width=0.0035)

'''
t2=time.time()
u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, corr_method='fft', window_size=ws, \
    overlap=ol, dt=0.02, sig2noise_method='peak2peak' )
x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=ws, overlap=ol )
#tools.display_windows_sampling( x, y, ws, skip=1,  method='standard')
u, v, mask = validation.sig2noise_val( u, v, sig2noise, threshold = 1.3 )
u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = 96.52 )
tools.save(x, y, u, v, mask, os.path.join(path,'./res_fft.txt'))
t3=time.time()
tools.display_vector_field(os.path.join(path,'./res_fft.txt'), on_img=True, negative_img=False, \
    image_name=os.path.join(path,'./00020359.bmp'), scaling_factor=96.52,scale=40, width=0.0035)


#print("---process %s seconds---" % (t1-t0))
print("---pyprocess %s seconds---" % (t3-t2))
