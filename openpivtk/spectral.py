# Fourier Analysis Script
# By: Pouya Mohtat
# Created: Aug. 2020
# Last update: Nov. 2020

# Change Log:
# - added function to perform global short-time fourier analysis which reveals both 'spacial' and 'temporal' variation of frequency fields
# - code refracted and wrapped into a neat analysis object
# - added frequency limit for saved results to keep the output cleaner
# - more efficient data reads (prevent reading the data files multiple times, instead the data is kept in memory)
# - added functions to load and save setting files and logic to run analysis based on this settings

# To do:
# - add ensemble averaging for fft


import numpy as np
import scipy.signal as signal
import os, glob, time
from collections import OrderedDict
from configparser import ConfigParser
import matplotlib.pyplot as plt



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
        self.N = nfiles
        file_list = glob.glob(os.path.join(path, pattern))
        file_list.sort()
        self.file_list = file_list[:nfiles]
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
        self.saveData(mode='point_fft', St=St, Su=Su, Sv=Sv)
        
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
        Su = abs(Su)
        Sv = abs(Sv)
        #saving results
        self.saveData(mode='point_stft', t=t, St=St, Su=Su, Sv=Sv)
        
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
        Su_max : 2d np.ndarray
            array of maximum Su values and their corresponding frequency
            at each point

        Su_map : 2d np.ndarray
            array containing the map of Su values at different frequencies, 
            each row represents Su values at a specific frequency

        Sv_max : 2d np.ndarray
            array of maximum Sv values and their corresponding frequency
            at each point

        Sv_map : 2d np.ndarray
            array containing the map of Sv values at different frequencies,
            each row represents Sv values at a specific frequency

        St : 1d np.ndarray
            Strouhal number or Frequency data in Hz

        """
        #initialize arrays
        sample = np.loadtxt(self.file_list[0], skiprows=1)
        nxy = sample.shape[0]
        St = np.fft.rfftfreq(self.N, 1/self.fs)*self.dim
        nfreq = sum(St<flim)                                # number of frequencies that are smaller than the flim
        St = St[0:nfreq]
        Su_max = np.zeros((nxy, 4))                         # maximum Su and its' corresponding frequency at each point
        Su_map = np.zeros((nxy, 2+nfreq))                   # Su values at each frequency (each column corresponds to a certain frequency)
        Su_map[:,0:2] = Su_max[:,0:2] = sample[:,0:2]       # the first two columns are x and y values
        Sv_max = np.zeros((nxy, 4))
        Sv_map = np.zeros((nxy, 2+nfreq))
        Sv_map[:,0:2] = Sv_max[:,0:2] = sample[:,0:2]
        #read velocity data
        if velocity is None:
            velocity = self.getGlobalVelocity()
        #take the fft
        for i in range(nxy):
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
        #saving the results
        self.saveData(mode='global_fft', Su_max=Su_max, Su_map=Su_map, Sv_max=Sv_max, Sv_map=Sv_map, St=St)
        
        return Su_max, Su_map, Sv_max, Sv_map, St


    def global_stft(self, nperseg, noverlap, flim, velocity=None):
        #read velocity data
        if velocity is None:
            velocity = self.getGlobalVelocity()
        #initialize values
        sample = np.loadtxt(self.file_list[0], skiprows=1)
        nxy = sample.shape[0]
        sample_f, sample_t, sample_Su = signal.stft(velocity[nxy//2], fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
            return_onesided=True, padded=False)
        St = sample_f*self.dim
        nfreq = sum(St<flim)                                            # number of frequencies that are smaller than the flim
        St = St[0:nfreq]
        ntime = len(sample_t)
        Su_map = np.zeros((nxy,nfreq+2,ntime), float)                   # Su values at each frequency (each column corresponds to a certain frequency and the third axis is time)
        Sv_map = np.zeros((nxy,nfreq+2,ntime), float)                   # the same...
        Su_map[:,0:2,:] = Sv_map[:,0:2,:] = sample[:,0:2,np.newaxis]    # the first two columns hold values for x and y
        #take the stft
        for i in range(nxy):
            f, t, Su = signal.stft(velocity[i,0,:], fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
                return_onesided=True, padded=False)
            f, t, Sv = signal.stft(velocity[i,1,:], fs=self.fs, window='hann', nperseg=nperseg, noverlap=noverlap, \
                return_onesided=True, padded=False)
            Su_map[i,2:,:] = abs(Su[:nfreq,:])
            Sv_map[i,2:,:] = abs(Sv[:nfreq,:])
        #saving the results
        self.saveData(mode='global_stft', t=t, St=St, Su_map=Su_map, Sv_map=Sv_map)

        return t[0:nfreq], St, Su_map, Sv_map


    def getPointVelocity(self, gx, gy, velocity=None):
        self.gx, self.gy = gx, gy
        sample = np.loadtxt(self.file_list[0], skiprows=1)
        index, = np.where((sample[:,0]==self.gx) & (sample[:,1]==self.gy))
        ind = int(index)

        #loop to read files and collect time data
        if velocity is None:
            u = np.zeros(self.N)
            v = np.zeros(self.N)
            for i in range(self.N):
                data = np.loadtxt(self.file_list[i], skiprows=1)
                u[i] = data[ind, 2]
                v[i] = data[ind, 3]
        else:
            u = velocity[ind,0,:]
            v = velocity[ind,1,:]

        return u, v


    def getGlobalVelocity(self):
        sample = np.loadtxt(self.file_list[0], skiprows=1)
        nxy = sample.shape[0]
        velocity = np.zeros((nxy, 2, self.N))
        for i in range(self.N):
            velocity[:,:,i] = np.loadtxt(self.file_list[i], skiprows=1)[:,2:4]
        return velocity


    def saveData(self, mode, t=None, St=None, Su=None, Sv=None, Su_map=None, Su_max=None, Sv_map=None, Sv_max=None):
        if mode == 'point_fft':
            out_u = np.vstack([St, Su])
            out_v = np.vstack([St, Sv])
            headerline = f'TITLE="U_fft for Point=({self.gx},{self.gy})" VARIABLES="St", "Su"'
            np.savetxt(os.path.join(self.dir, f'U_fft_Point ({self.gx},{self.gy}).dat'), out_u.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="V_fft for Point=({self.gx},{self.gy})" VARIABLES="St", "Sv"'
            np.savetxt(os.path.join(self.dir, f'V_fft_Point ({self.gx},{self.gy}).dat'), out_v.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            return

        if mode == 'point_stft':
            t_mesh, St_mesh = np.meshgrid(t, St)
            out_u = np.vstack([t_mesh.ravel(), St_mesh.ravel(), Su.ravel(), Su.ravel()/np.max(Su)])
            out_v = np.vstack([t_mesh.ravel(), St_mesh.ravel(), Sv.ravel(), Sv.ravel()/np.max(Sv)])
            headerline = f'TITLE="U_short_time_fft Point=({self.gx},{self.gy})" VARIABLES="t", "St", "Su", "Su_nondim" ZONE I={t.size}, J={St.size}'
            np.savetxt(os.path.join(self.dir, f'U_stft_Point ({self.gx},{self.gy}).dat'), out_u.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="V_short_time_fft Point=({self.gx},{self.gy})" VARIABLES="t", "St", "Sv", "Sv_nondim" ZONE I={t.size}, J={St.size}'
            np.savetxt(os.path.join(self.dir, f'V_stft_Point ({self.gx},{self.gy}).dat'), out_v.T, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
            return

        sample = np.loadtxt(self.file_list[0], skiprows=1)
        nx = len(np.unique(sample[:,0]))
        ny = sample.shape[0]//nx
        nfreq = Su_map.shape[1] - 2

        if mode == 'global_fft':
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
            return

        if mode == 'global_stft':
            for i, t in enumerate(t):
                headerline = f'TITLE="Su_map for time={t:0.3}" VARIABLES="x", "y"'
                for n in range(nfreq):
                    headerline += (f', "Su for St={St[n]:0.3}"')
                headerline += f' ZONE I={nx}, J={ny}'
                np.savetxt(os.path.join(self.dir, f'Global_Su_map_t{t:0.3}.dat') , Su_map[:,:,i], fmt='%8.4f', delimiter='\t', header=headerline, comments='')
                headerline = f'TITLE="Sv_map for time={t:0.3}" VARIABLES="x", "y"'
                for n in range(nfreq):
                    headerline += (f', "Sv for St={St[n]:0.3}"')
                headerline += f' ZONE I={nx}, J={ny}'
                np.savetxt(os.path.join(self.dir, f'Global_Sv_map_t{t:0.3}.dat') , Sv_map[:,:,i], fmt='%8.4f', delimiter='\t', header=headerline, comments='')
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
    
    exp, analysis = OrderedDict(), OrderedDict()
    exp, analysis = FrequencyAnalysis.loadSettings('E:\Temp\Re11_medium\Frequency_sttings.ini')
    t1 = time.time()

    experiments = glob.glob(os.path.join(exp['dir'], exp['exp']))
    for experiment in experiments:
        runs = glob.glob(os.path.join(experiment, exp['run']))
        for run in runs:
            path = os.path.join(run, 'Analysis')
            print('initializing...')
            spectral = FrequencyAnalysis(path, int(exp['nf']), exp['pat'], fs=float(analysis['fs']), dim=float(analysis['dim']))
            velocity = None

            if eval(analysis['gb_fft']) or eval(analysis['gb_stft']):
                print('reading velocity...')
                velocity = spectral.getGlobalVelocity()
                if eval(analysis['gb_fft']):
                    print('runing global fft...')
                    spectral.global_fft(flim=float(analysis['flim']), velocity=velocity)
                if eval(analysis['gb_stft']):
                    print('runing global stft...')
                    spectral.global_stft(nperseg=int(analysis['nperseg']), noverlap=int(analysis['noverlap']), flim=float(analysis['flim']), velocity=velocity)
            
            if eval(analysis['pt_fft']) or eval(analysis['pt_stft']):
                print('getting u, v values...')
                if analysis['pt_mode'] == 'specified point':
                    gx, gy = map(float, analysis['pt'].split(','))
                elif analysis['pt_mode'] == 'Max Global Su':
                    fname = os.path.join(path, 'Frequency Analysis', 'Global_Su_max.dat')
                    if os.path.exists(fname):
                        data = np.loadtxt(fname, skiprows=1)
                        amax = np.argmax(data[:,3])
                        gx, gy = data[amax,0], data[amax,1]
                    else:
                        print('No Su data found! skiped, point spectra was not calculated.')
                        gx, gy = None, None       
                elif analysis['pt_mode'] == 'Sv_max':
                    fname = os.path.join(path, 'Frequency Analysis', 'Global_Sv_max.dat')
                    if os.path.exists(fname):
                        data = np.loadtxt(fname, skiprows=1)
                        amax = np.argmax(data[:,3])
                        gx, gy = data[amax,0], data[amax,1]
                    else:
                        print('No Sv data found! skiped, point spectra was not calculated.')
                        gx, gy = None, None
                if gy is not None:
                    u, v = spectral.getPointVelocity(gx, gy, velocity=velocity)
                    if eval(analysis['pt_fft']):
                        print('runing point fft...')
                        spectral.point_fft(u, v)
                    if eval(analysis['pt_stft']):
                        print('runing point stft...')
                        spectral.point_stft(u, v, nperseg=analysis['nperseg'], noverlap=analysis['noverlap'])

    print(f'frequency analysis finished in {time.time()-t1} sec')