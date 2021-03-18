# Fourier Analysis Script
# By: Pouya Mohtat
# Created: Aug. 2020
# Last update: Mar. 2021

# Change Log:
# - .h5 file support was added which reduces the run time significantly
# - added function to perform global short-time fourier analysis which reveals both 'spacial' and 'temporal' variation of frequency fields
# - code refracted and wrapped into a neat analysis object
# - more efficient data reads (prevent reading the data files multiple times, instead the data is kept in memory)

# To do:
# - add ensemble averaging for fft -> (we can use scipy.signal.welsh for this)
# - add an output parameter to show what is the maximum Su at each frequency (regardless of where in the flow field). this is usefull when looking at the data
#   trying to see which frequencies are important. we can do this by looking at the point fft result but that's only for a specific point! we want this for GAS. -> done


import numpy as np
import scipy.signal as signal
import os, glob, time
from collections import OrderedDict
from configparser import ConfigParser
import matplotlib.pyplot as plt
from openpivtk import tools



class FrequencyAnalysis():
    """class for performing Frequency Analysis. creates the 'Frequency Analysis' folder

    Parameters
    ----------
    path: str
        absolute path to the data files

    nfiles: int
        number of files to use for the analysis

    pattern: str
        the data file naming pattern

    fs: float, optional
        data aquisition frequency, defaults to 1

    dim: float, optional
        scale factor used to nondimentionalize frequency, can be set
        to D/V (D:length scale, V:velocity) to get the Strouhal numb.,
        default is 1 in which case the frequency values are in Hz
    """

    def __init__(self, path, nfiles, pattern, fs=1, dim=1):
        
        file_list = glob.glob(os.path.join(path, pattern))
        file_list.sort()
        *_, ext = os.path.splitext(file_list[0])
        if ext == '.h5':
            self.fmode = 'h5'
            self.file_list = file_list
            temp, *_ = tools.load_h5(self.file_list[0], mode='1D', ntime=1, ds=['x', 'y'])
            self.xy = temp[:,:,0]
        elif ext == '.dat':
            self.fmode = 'dat'
            self.file_list = file_list[:nfiles]
            temp = np.loadtxt(self.file_list[0], skiprows=1)
            self.xy = temp[:,0:2]
        self.nxy = len(self.xy[:,0])
        self.N = nfiles
        self.fs = fs
        self.dim = dim
        self.dir = os.path.join(path, 'Frequency Analysis')
        if os.path.isdir(self.dir) == False:
            os.mkdir(self.dir)


    def point_fft(self, u, v):
        """perfomrs FFT for a single point in the flow, saves the results
        and returns frequency and spectral amplitude 
        
        Parameters
        ----------
        u, v : 1D.ndarray
            velocity data at the point

        Returns
        -------
        St : 1d np.ndarray
            Strouhal number or frequency values in Hz

        Su, Sv : 1d np.ndarray
            spectral density values

        """
        Su = abs(np.fft.rfft(u))*2/self.N   #devide by (number of points/2)
        Sv = abs(np.fft.rfft(v))*2/self.N
        St = np.fft.rfftfreq(self.N, 1/self.fs)*self.dim
        Su[0] = Sv[0] = 0    # first values are thrown out
        #saving results in the "Spectral Analysis" directory
        self.saveData(mode='point_fft', data=[St, Su, Sv])
        
        return St, Su, Sv


    def point_stft(self, u, v, nperseg, noverlap):
        """ performs short-time fft for a single point in the flow, saves the results
        and returns frequency, time and spectral amplitudes
        
        Parameters
        ----------
        u, v: 1D.ndarray
            velocity data at the point

        nperseg: int
            number of points in each window

        noverlap: int
            number of points that overlap between each window

        Returns
        -------
        St : 1d np.ndarray
            array containing Strouhal number or frequency in Hz

        t : 1d np.ndarray
            array containing time values

        Su : 1d np.ndarray
            array containing spectral density values

        """
        #run STFT
        f, t, Su = signal.stft(u, fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
        return_onesided=True, padded=False)
        f, t, Sv = signal.stft(v, fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
        return_onesided=True, padded=False)
        Su[0,:] = Sv[0,:] = 0   #the first value is thrown out
        St = f*self.dim
        Su = abs(Su)*2
        Sv = abs(Sv)*2
        #saving results
        self.saveData(mode='point_stft', data=[t, St, Su, Sv])
        
        return t, St, Su, Sv


    def global_fft(self, flim, velocity=None):
        """ performs the global Autospectral density (GAS) analysis for velocity data, saves the results
        and returns global specra and the maximum value of GAS at each point
        
        Parameters
        ----------
        flim : float
            the frequecy limit, results for frequencies higher than flim are not saved

        velocity: 2D.ndarray
            velocity array of the shape (nxy, 2). the two columns are u nd v velocity values

        Returns
        -------
        Su_map, Sv_map : 2d np.ndarray
            arrays containing the map of Su and Sv values at different frequencies, 
            each row represents Su values at a specific frequency
        
        Su_max, Sv_max : 2d np.ndarray
            arrays of maximum Su and Sv values and their corresponding frequency
            at each point

        Su_f, Sv_f : 2d np.ndarray
            arrays conraining the maximum Su and Sv values at each frequency regardless
            of their location in the flow field

        St : 1d np.ndarray
            Strouhal number or Frequency data in Hz

        """
        #initialize arrays
        St = np.fft.rfftfreq(self.N, 1/self.fs)*self.dim
        nfreq = sum(St<flim)                                # number of frequencies that are smaller than the flim
        St = St[0:nfreq]
        Su_max = np.zeros((self.nxy, 4))                         # maximum Su and its' corresponding frequency at each point
        Su_map = np.zeros((self.nxy, 2+nfreq))                   # Su values at each frequency (each column corresponds to a certain frequency)
        Su_map[:,0:2] = Su_max[:,0:2] = self.xy                  # the first two columns are x and y values
        Sv_max = np.zeros((self.nxy, 4))
        Sv_map = np.zeros((self.nxy, 2+nfreq))
        Sv_map[:,0:2] = Sv_max[:,0:2] = self.xy
        #read velocity data
        if velocity is None:
            velocity = self.getGlobalVelocity()
        #take the fft
        for i in range(self.nxy):
            Su = abs(np.fft.rfft(velocity[i,0,:])*2/self.N)
            Sv = abs(np.fft.rfft(velocity[i,1,:])*2/self.N)
            Su = Su[0:nfreq]
            Sv = Sv[0:nfreq]
            Su[0] = Sv[0] = 0   #first value gets thrown out
            Su_map[i, 2:] = Su
            Su_max[i, 3] = np.amax(Su)
            Su_max[i, 2] = St[np.argmax(Su)]
            Sv_map[i, 2:] = Sv
            Sv_max[i, 3] = np.amax(Sv)
            Sv_max[i, 2] = St[np.argmax(Sv)]
        # find the maximum Su and Sv at each frequency (regardless of their location in the field)
        Su_f, Sv_f = np.zeros((2, len(St), 2), Su_map.dtype)
        Su_f[:,0], Sv_f[:,0] = St, St
        Su_f[:,1] = np.max(Su_map[:,2:], axis=0)
        Sv_f[:,1] = np.max(Sv_map[:,2:], axis=0)
        #saving the results
        self.saveData(mode='global_fft', data=[Su_max, Su_map, Sv_max, Sv_map, St, Su_f, Sv_f])
        
        return Su_map, Sv_map, Su_max, Sv_max, Su_f, Sv_f, St


    def global_stft(self, nperseg, noverlap, flim, velocity=None):
        #read velocity data
        if velocity is None:
            velocity = self.getGlobalVelocity()
        #initialize values
        sample_f, sample_t, sample_Su = signal.stft(velocity[self.nxy//2], fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
            return_onesided=True, padded=False)
        St = sample_f*self.dim
        nfreq = sum(St<flim)                                            # number of frequencies that are smaller than the flim
        St = St[0:nfreq]
        ntime = len(sample_t)
        Su_map = np.zeros((self.nxy,nfreq+2,ntime), float)                   # Su values at each frequency (each column corresponds to a certain frequency and the third axis is time)
        Sv_map = np.zeros((self.nxy,nfreq+2,ntime), float)                   # the same...
        Su_map[:,0:2,:] = Sv_map[:,0:2,:] = self.xy[:,0:2,np.newaxis]    # the first two columns hold values for x and y
        #take the stft
        for i in range(self.nxy):
            f, t, Su = signal.stft(velocity[i,0,:], fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
                return_onesided=True, padded=False)
            f, t, Sv = signal.stft(velocity[i,1,:], fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
                return_onesided=True, padded=False)
            Su_map[i,2:,:] = abs(Su[:nfreq,:])*2
            Sv_map[i,2:,:] = abs(Sv[:nfreq,:])*2
        #saving the results
        self.saveData(mode='global_stft', data=[t, St, Su_map, Sv_map])

        return t[0:nfreq], St, Su_map, Sv_map


    def getPointVelocity(self, gx, gy, velocity=None):
        
        ind = ((self.xy[:,0] - gx)**2 + (self.xy[:,1] - gy)**2).argmin()
        self.gx, self.gy = self.xy[ind,0], self.xy[ind,1]

        #loop to read files and collect time data
        if velocity is None:
            if self.fmode == 'dat':
                u = np.zeros(self.N)
                v = np.zeros(self.N)
                for i in range(self.N):
                    data = np.loadtxt(self.file_list[i], skiprows=1)
                    u[i] = data[ind, 2]
                    v[i] = data[ind, 3]
            elif self.fmode == 'h5':
                data, *_ = tools.load_h5(self.file_list[0], mode='1D', ntime=self.N, ds=['u', 'v'])
                u = data[ind, 0, :]
                v = data[ind, 1, :]
        else:
            u = velocity[ind,0,:]
            v = velocity[ind,1,:]

        return u, v


    def getGlobalVelocity(self):
        if self.fmode == 'dat':
            velocity = np.zeros((self.nxy, 2, self.N))
            for i in range(self.N):
                velocity[:,:,i] = np.loadtxt(self.file_list[i], skiprows=1)[:,2:4]
        elif self.fmode == 'h5':
            velocity, dss = tools.load_h5(self.file_list[0], mode='1D', ntime=self.N, ds=['u', 'v'])
            # print(dss)

        return velocity


    def saveData(self, mode, data=None):
        if mode == 'point_fft':
            St, Su, Sv = data
            out_u = np.vstack([St, Su])
            out_v = np.vstack([St, Sv])
            headerline = f'TITLE="U_fft for Point=({self.gx},{self.gy})" VARIABLES="St", "Su"'
            np.savetxt(os.path.join(self.dir, f'U_fft_Point ({self.gx},{self.gy}).dat'), out_u.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="V_fft for Point=({self.gx},{self.gy})" VARIABLES="St", "Sv"'
            np.savetxt(os.path.join(self.dir, f'V_fft_Point ({self.gx},{self.gy}).dat'), out_v.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            return

        if mode == 'point_stft':
            t, St, Su, Sv = data
            t_mesh, St_mesh = np.meshgrid(t, St)
            out_u = np.vstack([t_mesh.ravel(), St_mesh.ravel(), Su.ravel(), Su.ravel()/np.max(Su)])
            out_v = np.vstack([t_mesh.ravel(), St_mesh.ravel(), Sv.ravel(), Sv.ravel()/np.max(Sv)])
            headerline = f'TITLE="U_short_time_fft Point=({self.gx},{self.gy})" VARIABLES="t", "St", "Su", "Su_nondim" ZONE I={t.size}, J={St.size}'
            np.savetxt(os.path.join(self.dir, f'U_stft_Point ({self.gx},{self.gy}).dat'), out_u.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="V_short_time_fft Point=({self.gx},{self.gy})" VARIABLES="t", "St", "Sv", "Sv_nondim" ZONE I={t.size}, J={St.size}'
            np.savetxt(os.path.join(self.dir, f'V_stft_Point ({self.gx},{self.gy}).dat'), out_v.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            return

        
        nx = len(np.unique(self.xy[:,0]))
        ny = self.nxy//nx

        if mode == 'global_fft':
            Su_max, Su_map, Sv_max, Sv_map, St, Su_f, Sv_f = data
            nfreq = Su_map.shape[1] - 2

            headerline = 'TITLE="Su_map" VARIABLES="x", "y"'
            for n in range(nfreq):
                headerline += (f', "Su for St={St[n]:0.3}"')
            headerline += f' ZONE I={nx}, J={ny}'
            np.savetxt(os.path.join(self.dir, 'Global_Su_map.dat') , Su_map, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="Su_max" VARIABLES="x", "y", "St", "Su" ZONE I={nx}, J={ny}'
            np.savetxt(os.path.join(self.dir, 'Global_Su_max.dat'), Su_max, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

            headerline = 'TITLE="Sv_map" VARIABLES="x", "y"'
            for n in range(nfreq):
                headerline += (f', "Sv for St={St[n]:0.3}"')
            headerline += f' ZONE I={nx}, J={ny}'
            np.savetxt(os.path.join(self.dir, 'Global_Sv_map.dat') , Sv_map, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="Sv_max" VARIABLES="x", "y", "St", "Sv" ZONE I={nx}, J={ny}'
            np.savetxt(os.path.join(self.dir, 'Global_Sv_max.dat'), Sv_max, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

            headerline = f'TITLE="Su_max_freq" VARIABLES="St", "Su_max"'
            np.savetxt(os.path.join(self.dir, 'Global_Su_max_freq.dat'), Su_f, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="Sv_max_freq" VARIABLES="St", "Sv_max"'
            np.savetxt(os.path.join(self.dir, 'Global_Sv_max_freq.dat'), Sv_f, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

            return

        if mode == 'global_stft':
            t, St, Su_map, Sv_map = data
            nfreq = Su_map.shape[1] - 2

            if self.fmode == 'dat':
                fpath = os.path.join(self.dir, 'STFT Fields')
                if os.path.isdir(fpath) == False:
                    os.mkdir(fpath)
                for i, t in enumerate(t):
                    headerline = f'TITLE="Su_map for time={t:0.3}" VARIABLES="x", "y"'
                    for n in range(nfreq):
                        headerline += (f', "Su for St={St[n]:0.3}"')
                    headerline += f' ZONE I={nx}, J={ny}'
                    np.savetxt(os.path.join(fpath, f'Global_Su_map_t{t:0.3}.dat') , Su_map[:,:,i], fmt='%8.4f', delimiter='\t', header=headerline, comments='')
                    headerline = f'TITLE="Sv_map for time={t:0.3}" VARIABLES="x", "y"'
                    for n in range(nfreq):
                        headerline += (f', "Sv for St={St[n]:0.3}"')
                    headerline += f' ZONE I={nx}, J={ny}'
                    np.savetxt(os.path.join(fpath, f'Global_Sv_map_t{t:0.3}.dat') , Sv_map[:,:,i], fmt='%8.4f', delimiter='\t', header=headerline, comments='')

            elif self.fmode == 'h5':
                variables = ['x', 'y'] + [f'St={St[n]:.3f}' for n in range(nfreq)]
                grps = [f't{i:0>7.3f}' for i in t]
                tools.save_h5(os.path.join(self.dir, f'Global_stft_Su_map.h5'), Su_map, variables, mode='1D', grp_names=grps, naming=1)
                tools.save_h5(os.path.join(self.dir, f'Global_stft_Sv_map.h5'), Sv_map, variables, mode='1D', grp_names=grps, naming=1)
            
            return


    @staticmethod
    def saveSettings(exp, analysis, stg_file):
        settings = ConfigParser()
        settings['Experiment'] = exp
        settings['Analysis'] = analysis
        with open(stg_file, 'w') as fl:
            fl.write('# Spectral Analysis Settings:\n\n')
            settings.write(fl)

    @staticmethod
    def loadSettings(stg_file):
        settings = ConfigParser()
        settings.read(stg_file)
        
        return settings['Experiment'], settings['Analysis']
        


#code to test functions
if __name__ == "__main__":
    
    # exp, analysis = OrderedDict(), OrderedDict()
    # exp, analysis = FrequencyAnalysis.loadSettings('E:\Temp\Re11_medium\Frequency_sttings.ini')
    # t1 = time.time()

    # experiments = glob.glob(os.path.join(exp['dir'], exp['exp']))
    # for experiment in experiments:
    #     runs = glob.glob(os.path.join(experiment, exp['run']))
    #     for run in runs:
    #         path = os.path.join(run, 'Analysis')
    #         print('initializing...')
    #         spectral = FrequencyAnalysis(path, int(exp['nf']), exp['pat'], fs=float(analysis['fs']), dim=float(analysis['dim']))
    #         velocity = None

    #         if eval(analysis['gb_fft']) or eval(analysis['gb_stft']):
    #             print('reading velocity...')
    #             velocity = spectral.getGlobalVelocity()
    #             if eval(analysis['gb_fft']):
    #                 print('runing global fft...')
    #                 spectral.global_fft(flim=float(analysis['flim']), velocity=velocity)
    #             if eval(analysis['gb_stft']):
    #                 print('runing global stft...')
    #                 spectral.global_stft(nperseg=int(analysis['nperseg']), noverlap=int(analysis['noverlap']), flim=float(analysis['flim']), velocity=velocity)
            
    #         if eval(analysis['pt_fft']) or eval(analysis['pt_stft']):
    #             print('getting u, v values...')
    #             if analysis['pt_mode'] == 'specified point':
    #                 gx, gy = map(float, analysis['pt'].split(','))
    #             elif analysis['pt_mode'] == 'Max Global Su':
    #                 fname = os.path.join(path, 'Frequency Analysis', 'Global_Su_max.dat')
    #                 if os.path.exists(fname):
    #                     data = np.loadtxt(fname, skiprows=1)
    #                     amax = np.argmax(data[:,3])
    #                     gx, gy = data[amax,0], data[amax,1]
    #                 else:
    #                     print('No Su data found! skiped, point spectra was not calculated.')
    #                     gx, gy = None, None       
    #             elif analysis['pt_mode'] == 'Sv_max':
    #                 fname = os.path.join(path, 'Frequency Analysis', 'Global_Sv_max.dat')
    #                 if os.path.exists(fname):
    #                     data = np.loadtxt(fname, skiprows=1)
    #                     amax = np.argmax(data[:,3])
    #                     gx, gy = data[amax,0], data[amax,1]
    #                 else:
    #                     print('No Sv data found! skiped, point spectra was not calculated.')
    #                     gx, gy = None, None
    #             if gy is not None:
    #                 u, v = spectral.getPointVelocity(gx, gy, velocity=velocity)
    #                 if eval(analysis['pt_fft']):
    #                     print('runing point fft...')
    #                     spectral.point_fft(u, v)
    #                 if eval(analysis['pt_stft']):
    #                     print('runing point stft...')
    #                     spectral.point_stft(u, v, nperseg=analysis['nperseg'], noverlap=analysis['noverlap'])

    # print(f'frequency analysis finished in {time.time()-t1} sec')
    path = r'C:\Users\Asus\Desktop\Dummy Data\exp1\run1\Analysis'
    # fa = FrequencyAnalysis(path, 4, '*.h5')
    fa = FrequencyAnalysis(path, 4, 'Theta1800deg000*.dat')
    velocity = fa.getGlobalVelocity()
    u, v = fa.getPointVelocity(640, 1020, velocity)
    print(u)
    print(f'gx={fa.gx}, gy={fa.gy}')