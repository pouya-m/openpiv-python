
import numpy as np
import scipy.signal as signal
import warnings
import os
import glob


def point_fft(file_list, gx, gy, fs=1, dim_ratio=1):
    """ Calculates FFT for a single point in the flow from list of files,
    saves results in a folder called "Spectral Analysis" and returns frequency
    and spectral amplitude 
    
    
    Parameters
    ----------
    file_list : List of strings
        absolute path to the files containing flow data

    gx : int or float
        x position of the desired point for fft analysis, can be
        in pixels or dimentional

    gy : int or float
        y position of the desired point for fft analysis, can be
        in pixels or dimentional

    fs : float, optional
        data aquisition frequency, defaults to 1

    dim_ratio: float, optional
        scale factor used to nondimentionalize frequency, can be set
        to D/V (D:length scale, V:velocity scale of the flow) to get the
        Strouhal numb., default is 1 in which case the function returns
        frequency values in Hz

    Returns
    -------
    St : 1d np.ndarray
        array containing Strouhal number or frequency in Hz

    Su : 1d np.ndarray
        array containing spectral density values

    """

    npoints = len(file_list)
    u = np.zeros(npoints)
    v = np.zeros(npoints)
    sample = np.loadtxt(file_list[0], skiprows=1)
    index, = np.where((sample[:,0]==gx) & (sample[:,1]==gy))
    ind = int(index)

    #loop to read files and collect time data
    for i in range(npoints):
        data = np.loadtxt(file_list[i], skiprows=1)
        u[i] = data[ind, 2]
        v[i] = data[ind, 3]

    Su = abs(np.fft.rfft(u))*2/npoints   #devide by (number of points/2)
    Sv = abs(np.fft.rfft(v))*2/npoints
    Fr = np.fft.rfftfreq(npoints, 1/fs)*dim_ratio
    Su[0] = Sv[0] = 0    # first values are thrown out

    #saving results in the "Spectral Analysis" directory
    save_dir = os.path.join(os.path.dirname(file_list[0]), 'spectral Analysis')
    if os.path.isdir(save_dir)==False:
        os.mkdir(save_dir)
    out_u = np.vstack([Fr, Su])
    out_v = np.vstack([Fr, Sv])
    headerline = f'TITLE="U_fft for Point=({gx},{gy})" VARIABLES="Fr", "Su"'
    np.savetxt(os.path.join(save_dir, f'U_fft_Point ({gx},{gy}).txt'), out_u.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    headerline = f'TITLE="V_fft for Point=({gx},{gy})" VARIABLES="Fr", "Sv"'
    np.savetxt(os.path.join(save_dir, f'V_fft_Point ({gx},{gy}).txt'), out_v.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    
    return Fr, Su, Sv


#code to test point_fft:
path = os.path.dirname(os.path.abspath(__file__))
file_list = glob.glob(path+'\Dummy Data\dp*.txt')
file_list.sort()
point_fft(file_list, 64, 16, fs=10, dim_ratio=1)



def point_stft(file_list, gx, gy, nperseg, noverlap, fs=1, dim_ratio=1):
    """ Calculates Short-Time Fourier Transform for a single point in the flow
    from list of files, saves the results in a folder called "Spectral Analysis"
    and returns frequency, time and spectral amplitudes
    
    
    Parameters
    ----------
    file_list : List of strings
        absolute path to the files containing flow data

    gx : int or float
        x position of the desired point for stft analysis, can be
        in pixels or dimentional

    gy : int or float
        y position of the desired point for stft analysis, can be
        in pixels or dimentional

    nperseg: int
        number of points in each window

    noverlap: int
        number of points that overlap between each window

    fs : float, optional
        data aquisition frequency, defaults to 1

    dim_ratio: float, optional
        scale factor used to nondimentionalize frequency, can be set
        to D/V (D:length scale, V:velocity scale of the flow) to get the
        Strouhal numb., default is 1 in which case the function returns
        frequency values in Hz

    Returns
    -------
    St : 1d np.ndarray
        array containing Strouhal number or frequency in Hz

    t : 1d np.ndarray
        array containing time values

    Su : 1d np.ndarray
        array containing spectral density values

    """
    #initialize variables
    npoints = len(file_list)
    u = np.zeros(npoints)
    v = np.zeros(npoints)
    sample = np.loadtxt(file_list[0], skiprows=1)
    index, = np.where((sample[:,0]==gx) & (sample[:,1]==gy))
    ind = int(index)

    #loop to read files and collect time data
    for i in range(npoints):
        data = np.loadtxt(file_list[i], skiprows=1)
        u[i] = data[int(ind), 2]
        v[i] = data[int(ind), 3]

    #run STFT
    f, t, Su = signal.stft(u, fs=fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
    return_onesided=True, padded=False)
    f, t, Sv = signal.stft(v, fs=fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
    return_onesided=True, padded=False)
    Su[0] = Sv[0] = 0   #the first value is thrown out
    f = f*dim_ratio
    Su = abs(Su)
    Sv = abs(Sv)

    #saving results in the "Spectral Analysis" directory
    save_dir = os.path.join(os.path.dirname(file_list[0]), 'spectral Analysis')
    if os.path.isdir(save_dir)==False:
        os.mkdir(save_dir)
    t_mesh, f_mesh = np.meshgrid(t, f)
    out_u = np.vstack([t_mesh.ravel(), f_mesh.ravel(), Su.ravel()])
    out_v = np.vstack([t_mesh.ravel(), f_mesh.ravel(), Sv.ravel()])
    
    headerline = f'TITLE="U_short_time_fft Point=({gx},{gy})" VARIABLES="t", "Fr", "Su" ZONE I={t.size}, J={f.size}'
    np.savetxt(os.path.join(save_dir, f'U_short_time_fft_Point ({gx},{gy}).txt'), out_u.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    headerline = f'TITLE="V_short_time_fft Point=({gx},{gy})" VARIABLES="t", "Fr", "Sv" ZONE I={t.size}, J={f.size}'
    np.savetxt(os.path.join(save_dir, f'V_short_time_fft_Point ({gx},{gy}).txt'), out_v.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    
    return t, f, Su, Sv


#code to test point_stft
path = os.path.dirname(os.path.abspath(__file__))
file_list = glob.glob(path+'\Dummy Data\dp*.txt')
file_list.sort()
point_stft(file_list, 64, 16, 16, 10, fs=10)



def global_spectra(file_list, nx, nfreq, fs=1, dim_ratio=1):
    """ Calculates the global Autospectral density (GAS) for u and v from list of files,
    returns global specra and the maximum value of GAS at each point and saves the results
    in a folder called "Spectral Analysis".
    
    
    Parameters
    ----------
    file_list : List of strings
        absolute path to the files containing flow data

    nx : int
        number of horizontal points in the grid

    nfrq : int
        desired number of frequencies to calculate

    fs : float, optional
        data aquisition frequency, defaults to 1

    dim_ratio: float, optional
        scale factor used to nondimentionalize frequency, can be set
        to D/V (D:length scale, V:velocity scale of the flow) to get the
        Strouhal numb., default is 1 in which case the function returns
        frequency values in Hz

    Returns
    -------
    Su_max : 2d np.ndarray
        array containing maximum Su values and their respective frequency
        at each point

    Su_map : 2d np.ndarray
        array containing the map of Su values (for each point) at 
        different frequencis each row represents Su values at a specific
        frequency

    Sv_max : 2d np.ndarray
        array containing maximum Sv values and their respective frequency
        at each point

    Sv_map : 2d np.ndarray
        array containing the map of Sv values (for each point) at different
        frequencis each row represents Sv values at a specific frequency

    Fr : 1d np.ndarray
        array containing Strouhal number or Frequency data in Hz

    """
    #initialize arrays
    sample = np.loadtxt(file_list[0], skiprows=1)
    ntime = len(file_list)
    #check if (nfreq <= ntime/2+1)
    if nfreq > (ntime//2+1):
        warnings.warn(f'nfreq cannot be larger than (number of files/2)+1. \
            nfreq was lowered to its maximum possible value: {ntime//2+1}', Warning)
        nfreq = ntime//2 + 1
    nxy = sample.shape[0]
    data = np.zeros((nxy, sample.shape[1], ntime))
    Su_max = np.zeros((nxy, 4))
    Su_map = np.zeros((nxy, 2+nfreq))
    Su_map[:,0:2] = Su_max[:,0:2] = sample[:,0:2]
    Sv_max = np.zeros((nxy, 4))
    Sv_map = np.zeros((nxy, 2+nfreq))
    Sv_map[:,0:2] = Sv_max[:,0:2] = sample[:,0:2]
    #read all the data
    for i in range(ntime):
        data[:,:,i] = np.loadtxt(file_list[i], skiprows=1)
    #take the fft
    for i in range(nxy):
        Su = abs(np.fft.rfft(data[i,2,:])*2/ntime)
        Sv = abs(np.fft.rfft(data[i,3,:])*2/ntime)
        Su[0] = Sv[0] = 0   #first value gets thrown out
        Fr = np.fft.rfftfreq(ntime, 1/fs)*dim_ratio
        Su_map[i, 2:] = Su[0:nfreq]
        Su_max[i, 3] = np.amax(Su)
        Su_max[i, 2] = Fr[np.argmax(Su)]
        Sv_map[i, 2:] = Sv[0:nfreq]
        Sv_max[i, 3] = np.amax(Sv)
        Sv_max[i, 2] = Fr[np.argmax(Sv)]
    #saving the results in the "Spectral Analysis" directory
    ny = nxy//nx
    save_dir = os.path.join(os.path.dirname(file_list[0]), 'spectral Analysis')
    if os.path.isdir(save_dir)==False:
        os.mkdir(save_dir)
    
    headerline = 'TITLE="Su_map" VARIABLES="x", "y"'
    for n in range(nfreq):
        headerline += (f', "Su for Fr={Fr[n]}"')
    headerline += f' ZONE I={nx}, J={ny}'
    np.savetxt(os.path.join(save_dir, 'Global_Su_map.txt') , Su_map, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    
    headerline = f'TITLE="Su_max" VARIABLES="x", "y", "Fr", "Su" ZONE I={nx}, J={ny}'
    np.savetxt(os.path.join(save_dir, 'Global_Su_max.txt'), Su_max, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    
    headerline = 'TITLE="Sv_map" VARIABLES="x", "y"'
    for n in range(nfreq):
        headerline += (f', "Sv for Fr={Fr[n]}"')
    headerline += f' ZONE I={nx}, J={ny}'
    np.savetxt(os.path.join(save_dir, 'Global_Sv_map.txt') , Sv_map, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    
    headerline = f'TITLE="Sv_max" VARIABLES="x", "y", "Fr", "Sv" ZONE I={nx}, J={ny}'
    np.savetxt(os.path.join(save_dir, 'Global_Sv_max.txt'), Sv_max, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    
    return Su_max, Su_map, Sv_max, Sv_map, Fr


#code to test GAS
path = os.path.dirname(os.path.abspath(__file__))
file_list = glob.glob(path+'\Dummy Data\dp*.txt')
file_list.sort()
nfreq = 16
fs = 10
nx = 52
Su_max, Su_map, Sv_max, Sv_map, Fr = global_spectra (file_list, nx, nfreq, fs)
