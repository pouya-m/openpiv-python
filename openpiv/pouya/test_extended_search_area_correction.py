
from openpiv import tools, process, scaling, pyprocess, validation, filters
import numpy as np
import os
import pylab as plt

path = os.path.dirname(os.path.abspath(__file__))
frame_a  = tools.imread( os.path.join(path,'./00020360.bmp'))
frame_b  = tools.imread( os.path.join(path,'./00020361.bmp'))

frame_a = (frame_a*1024).astype(np.int32)
frame_b = (frame_b*1024).astype(np.int32)

ws=24
ol=12
sa=36


u, v, sig2noise = pyprocess.extended_search_area_piv( frame_a, frame_b, window_size=ws, corr_method='fft', \
    overlap=ol, search_area_size=sa, dt=0.02, sig2noise_method='peak2peak' )
x, y = pyprocess.get_coordinates( image_size=frame_a.shape, window_size=ws, overlap=ol )
#tools.display_windows_sampling( x, y, ws, skip=1,  method='standard')
u, v, mask = validation.sig2noise_val( u, v, sig2noise, threshold = 1.3 )
u, v = filters.replace_outliers( u, v, method='localmean', max_iter=10, kernel_size=2)
x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = 96.52 )
tools.save(x, y, u, v, mask, os.path.join(path,'./res_fft.txt'))
tools.display_vector_field(os.path.join(path,'./res_fft.txt'), on_img=False, negative_img=False, \
    image_name=os.path.join(path,'./00020359.bmp'), scaling_factor=96.52,scale=40, width=0.0035)

'''
window_a=frame_a[2*ws:3*ws,4*ws:5*ws]
#window_b=frame_a[2*ws:3*ws,4*ws:5*ws]
window_b=frame_a[2*ws-(sa-ws)//2:3*ws+(sa-ws)//2,4*ws-(sa-ws)//2:5*ws+(sa-ws)//2]
#pylab.imshow(window_b,cmap='gray')
#pylab.show()

corr = pyprocess.correlate_windows(window_a, window_b, corr_method='fft')
maxpoint = pyprocess.find_subpixel_peak_position(corr)
print(maxpoint)
pylab.imshow(corr,cmap='gray')
pylab.show()

a=[[1,2],[3,4]]
b=np.pad(a, (2,), mode='constant', constant_values=0)
print(b)

pad = 64
frame_b_padded = np.pad(frame_b, (pad,), mode='constant', constant_values=255)
pylab.imshow(frame_b_padded,cmap='gray')
pylab.show()
'''