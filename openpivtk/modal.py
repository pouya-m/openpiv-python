# Proper Orthogonal Decomposition
# By: Pouya Mohtat
# Created: Sep. 2020
# Last modified: Mar. 2021 

# This script assumes the data grid to be uniform. If data spacing is not uniform then 'weights' should be included in 
# the data matrix to account for the grid volume at each point...

# what's new:
# 1- added support for .h5 files which reduces the run time significantly
# 2- Added spectral POD analysis gives spectral modes that develop coherently over time and space separated both by their frequency and spacial variation
# 3- Added specific frequency field extraction using fft giving a field that varies at only one or more specific frequencies (averaged over time)
# 4- Added specific frequency field extraction using short-time fft which also shows variations over time

# to do:
# 1 - make the 'spectral pod analysis' and 'frequency fields extraction' functions available in GUI. -> done.
# 2 - the reconstruction stage does not add the average flow to the results. thus the reconstructed fields are actually flow
#     fluctuations (up, vp) not the flow field (u, v)


import os, glob, warnings, time
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from openpivtk import tools
from collections import OrderedDict
from configparser import ConfigParser
# import random


class ModalAnalysis():

    def __init__(self, path, nfiles, pattern):
        self.N = nfiles
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
        self.npoints = len(self.xy[:,0])
        self.M = 2 * self.npoints
        self.dir = os.path.join(path, 'Modal Analysis')
        if os.path.isdir(self.dir) == False:
            os.mkdir(self.dir)
        print('reading data...')
        self.A = self.constructDataMatrix()


    def svd(self, nmode='all'):
        """runs the SVD analysis and returns modes with temporal coefficients and
        their power distribution

        Parameters
        ----------
        nmode : int or 'all', optional
            number of modes to calculate and save. the default is 'all'

        Returns
        -------
        u, a : 2d np.ndarray
            mode array and coefficient array respectively
        
        w, p : 1d np.ndarray
            singular values and power density array respectively
        """

        #find singular values and sort them
        u, w, vh = np.linalg.svd(self.A, full_matrices=False)
        w, u, p = self.sortEignvalues(w**2, u)
        #calculate the coefficients
        if nmode != 'all':
            u = u[:,0:nmode]
        a = np.matmul(u.T, self.A)
        self.saveData(u, w, p, a)

        return u, w, a, p


    def snapshot(self, nmode='all'):
        """runs the modal analysis with snapshot method and returns modes with
        temporal coefficients and their power distribution

        Parameters
        ----------
        nmode : int or 'all', optional
            number of modes to calculate and save. the default is 'all'

        Returns
        -------
        u, a : 2d np.ndarray
            mode array and coefficient array respectively
        
        w, p : 1d np.ndarray
            singular values and power density array respectively
        """
        #find eignvalues and eignvectors of temporal correlation matrix
        C = np.matmul(self.A.T, self.A)
        w, v = np.linalg.eig(C)
        #sort the modes (use sqrt(w) to get power levels reflecting values for matrix A instead of C)
        w, v , p = self.sortEignvalues(w, v)
        #calculate the eign vectors of A
        if nmode == 'all':
            nmode = self.A.shape[1]    
        u = np.zeros((self.A.shape[0], nmode))
        for i in range(nmode):
            for j in range(self.A.shape[1]):
                u[:,i] += v[j,i] * self.A[:,j]
            u[:,i] /= np.sqrt(w[i])
        #calculate coefficients
        a = np.matmul(u.T, self.A)
        self.saveData(u, w, p, a)
        return u, w, a, p
    

    def spectralpod(self, nperseg, noverlap, fs, flim=1, windowing='hamming', fdim=1):
        """performs a compelete spectral pod analysis and returns spectral modes
        and eignvalues

        Parameters
        ----------
        nperseg, noverlap : int
            number of data points in each section and number of overlapping data

        fs, flim : float
            data aquisition frequency and the maximum frequency (higher frequencies 
            will not be calculated, will be discarded)

        windowing : str, optional
            a string passed to scipy.signal.get_window to get the windowing function
            used to reduce the bleeding effect in short-time fft. 

        fdim : float, optional
            a dimention factor to convert Hz to Strouhal (Diameter/Velocity)

        Returns
        -------
        Phi, Lam  : 3d and 2d np.ndarray
            mode array and eigenvalue array respectively. Phi is (M*Nb*Nflim) while
            Lam is (Nb,Nflim)
        
        freq, p : 1d np.ndarray
            frequency array and power percentage array respectively
        """

        # get data matrix and build the spectral matrix by looping over data blocks
        Nb = (self.N-nperseg)//(nperseg-noverlap) + 1
        freq = np.fft.rfftfreq(nperseg, 1.0/fs)*fdim
        Nf = len(freq)
        Nflim = sum(freq<flim)
        Xfk = np.zeros((self.M, Nb, Nf), float)
        # window = self.hammwin(nperseg)
        window = signal.get_window(windowing, nperseg)
        weight = 1/np.mean(window)
        print('looping over blocks and calculating fft...')
        for nb in range(Nb):
            ncurrent = nb*(nperseg-noverlap)
            Blk = self.A[:,ncurrent:ncurrent+nperseg]*window[np.newaxis,:]
            Xfk[:,nb,:] = abs(np.fft.rfft(Blk, axis=1))*2*weight/nperseg

        # loop over frequencies and calculate SPOD (only for f<flim)
        print('looping over frequencies and calculating SPOD')
        Lam = np.zeros((Nb,Nflim), float)
        Phi = np.zeros((self.M,Nb,Nflim), float)
        for f in range(Nflim):
            Xf = np.squeeze(Xfk[:,:,f])
            Sf = np.matmul(Xf.T, Xf)/Nb
            w, v = np.linalg.eig(Sf)
            w, v, *_ = self.sortEignvalues(w, v)
            lam = np.diag(np.power(w, -1/2.0)/np.sqrt(Nb))
            Phi[:,:,f] = np.matmul(np.matmul(Xf,v), lam)
            Lam[:,f] = w
        p = Lam*100/np.sum(Lam)
        freq = freq[0:Nflim]
        
        # save data
        self.saveData(spod=[Phi, Lam, freq, p])

        return Phi, Lam, freq, p


    def hammwin(self, N):
        """simple hamming window coefficients"""
        win = np.cos(2*np.pi*np.arange(0,N)/(N-1))
        return 0.54 - 0.46 * win


    def extractSingleFreqAvg(self, fd, fs, fdim=1):
        """limits the frequency content in the flow field such that the remaining field varies only
         at the desired frequency given by fd, shortcut to calculate phi=psi*exp(i2pift). this is averaged
         over time as it uses fft of the whole signal. consider using 'extractFreqField' function bellow instead..."""

        Af = np.fft.rfft(self.A, axis=1)*2/self.N
        f = np.fft.rfftfreq(self.A.shape[1], 1.0/fs)*fdim

        t = np.linspace(0,self.N/fs,self.N, endpoint=True)
        ind = np.argmin(abs(f-fd))
        # Ar = Su * exp(2(pi)f(i)t) :
        Ar = np.real(np.matmul(Af[:,ind,np.newaxis], np.exp(2*np.pi*fd*1j*t[:,np.newaxis].T)))

        # save the filtered field
        self.saveData(A_r=Ar)
        return Ar


    def extractFreqField(self, fd, fs, nperseg=None, noverlap=None, windowing='hamming', fdim=1, method='STFT'):
        """limits the frequency content in the flow field such that the remaining field varies only
         at the desired frequencies given by fd (it can be a single frequency or multiple frequencies).
         this uses either stft or fft methods to either keep time dependency or provide an averaged result"""

        if method == 'STFT':
            f, t, Af = signal.stft(self.A, fs=fs, window=windowing, nperseg=nperseg, noverlap=noverlap, \
                return_onesided=True, padded=False, axis=1)
            f = f*fdim
            Afd = np.zeros(Af.shape, Af.dtype)
            for fi in fd:
                ind = np.argmin(abs(f-fi))
                Afd[:,ind,:] = Af[:,ind,:]
            tr, Ar = signal.istft(Afd, fs=fs, window=windowing, nperseg=nperseg, noverlap=noverlap, input_onesided=True)

        elif method == 'FFT':
            Af = np.fft.rfft(self.A, axis=1)
            f = np.fft.rfftfreq(self.A.shape[1], 1.0/fs)*fdim
            Afd = np.zeros(Af.shape, Af.dtype)
            for fi in fd:
                ind = np.argmin(abs(f-fi))
                Afd[:,ind] = Af[:,ind]
            Ar = np.fft.irfft(Afd, axis=1)

        # save the filtered field
        self.saveData(A_r=Ar)
        return Ar


    def constructDataMatrix(self):
        """reads all files and returns xy info and the data matrix
        """
        A = np.zeros((self.M, self.N))
        #read all files and collect data matrix
        if self.fmode == 'dat':
            for i in range(self.N):
                data = np.loadtxt(self.file_list[i], skiprows=1)
                A[0:self.M//2, i] = data[:, 7]          # 7th column is u'
                A[self.M//2:self.M, i] = data[:, 8]     # 8th column is v'
        elif self.fmode == 'h5':
            data, *_ = tools.load_h5(self.file_list[0], mode='1D', ntime=self.N, ds=['up', 'vp'])
            A[0:self.M//2, :] = data[:, 0, :]
            A[self.M//2:self.M, :] = data[:, 1,:]
        
        return A


    def sortEignvalues(self, w, u):
        """ Sorts w in descending order and rearranges columns of u accordingly
            also calculates the power density distribution according to eignvalues
        """

        w_sorted = np.sort(np.abs(w))[::-1]
        arg_sort = np.argsort(np.abs(w))[::-1]
        u_sorted = np.zeros(u.shape, u.dtype)
        for i, arg in enumerate (arg_sort):
            u_sorted[:,i] = u[:,arg]
        p = w_sorted*100/np.sum(w_sorted)
        
        return w_sorted, u_sorted, p


    def reconstructField(self, nmode='all', nsp='all'):
        """ reconstructs the field using the given number of modes

        Parameters
        ----------
        nmode : int or 'all', optional
            the desired number of modes to use for reconstruction, if set to 'all' then
            all available modes are used. default is 'all'

        nsp : int or 'all', optional
            number of snapshots to reconstruct, if set to 'all' then all snapshots
            are reconstructed, 'all' is the default.

        Returns
        -------
        A_r : 2d np.ndarray
            the reconstructed field
        """
        #read data from saved files
        ap = np.loadtxt(os.path.join(self.dir, 'Coefficients.dat'), skiprows=1)
        a = ap[:,1:].T
        data = np.loadtxt(os.path.join(self.dir, 'Modes.dat'), skiprows=1)
        # avg = np.loadtxt(os.path.join(os.path.dirname(self.dir), 'AVG.dat'), skiprows=1)
        #check nsp and nmode
        if nsp == 'all':
            nsp = a.shape[1]
        if nsp > a.shape[1]:
            warnings.warn(f'number of snapshots to reconstruct cannot be larger than the original number of snapshots, nsp was set to its maximum possible value: {a.shape[1]}', Warning)
            nsp = a.shape[1]
        if nmode == 'all':
            nmode = a.shape[0]
        if nmode > a.shape[0]:
            warnings.warn(f'number of modes to use cannot be larger than the original number of modes, nmode was set to its maximum possible value: {a.shape[0]}', Warning)
            nmode = a.shape[0]
        # reconstruct the limited u from saved data
        u = np.zeros((self.M, nmode))
        for i in range(nmode):
            u[0:self.M//2,i] = data[:,2*i+2]
            u[self.M//2:self.M,i] = data[:,2*i+3]
        #reconstruct snapshots using u and a
        A_r = np.zeros((self.M, nsp), float)
        # A_avg = np.ndarray.flatten(avg[:,2:4], 'F')
        for i in range(nsp):
            for j in range(nmode):
                A_r[:,i] += a[j,i] * u[:,j] #+ A_avg
        self.saveData(A_r=A_r)

        return A_r


    def saveData(self, u=None, w=None, p=None, a=None, A_r=None, spod=None):
        """write data in the "Modal Analysis" directory
        """
        # get grid info
        nx = len(np.unique(self.xy[:,0]))
        ny = self.npoints//nx

        if u is not None:
            #saving modes data
            modes = np.zeros((self.npoints, 2*u.shape[1]+2))
            modes[:,0:2] = self.xy
            for i in range(u.shape[1]):
                modes[:,2*i+2] = u[0:self.M//2,i]
                modes[:,2*i+3] = u[self.M//2:self.M,i]
            headerline = 'TITLE="Mode Fields" VARIABLES="x", "y", '
            headerline += ', '.join([f'"u{i+1}", "v{i+1}"' for i in range(u.shape[1])])
            headerline += f' ZONE I={nx}, J={ny}'
            np.savetxt(os.path.join(self.dir, 'Modes.dat'), modes, fmt='%8.6f', delimiter='\t', header=headerline, comments='')

        if w is not None:
            #saving w and p data
            wp = np.zeros((w.size,4))
            wp[:,0], wp[:,1], wp[:,2], wp[:,3] = range(w.size), w, p, np.cumsum(p)
            headerline = 'TITLE="eignvalues and energy distribution" VARIABLES="mode", "eignvalue", "energy percentage", "cumulative energy percentage"'
            np.savetxt(os.path.join(self.dir, 'Energy Distribution.dat'), wp, fmt='%8.6f', delimiter='\t', header=headerline, comments='')

        if a is not None:
            #saving temporal coefficients
            ap = np.zeros((a.shape[1], a.shape[0]+1), float)
            ap[:,0] = np.arange(a.shape[1]) + 1
            ap[:,1:] = a.T
            headerline = 'TITLE="temporal coefficients" VARIABLES="snapshot", '
            headerline += ', '.join([f'"a{i}"' for i in range(a.shape[0])])
            np.savetxt(os.path.join(self.dir, 'Coefficients.dat'), ap, fmt='%8.6f', delimiter='\t', header=headerline, comments='')

        if A_r is not None:
            #saving the reconstructed flow fields
            A_rr = np.zeros((self.npoints, 4, A_r.shape[1]))
            A_rr[:,0:2,:] = self.xy[:,:,np.newaxis]
            A_rr[:,2,:] = A_r[0:self.M//2,:]
            A_rr[:,3,:] = A_r[self.M//2:self.M,:]

            if self.fmode == 'dat':
                for i in range(A_r.shape[1]):
                    headerline = f'TITLE="Reconstructed Fields {i+1}" VARIABLES="x", "y", "u", "v" ZONE I={nx}, J={ny}'
                    np.savetxt(os.path.join(self.dir, f'ReconstructedField{i+1:06}.dat'), A_rr[:,:,i], fmt='%8.6f', delimiter='\t', header=headerline, comments='')
            elif self.fmode == 'h5':
                tools.save_h5(os.path.join(self.dir, 'ReconstructedFields.h5'), A_rr, variables=['x', 'y', 'u', 'v'], mode='1D')

        if spod is not None:
            # saving spod results
            Phi, Lam, freq, p = spod
            modes = np.zeros((self.npoints,2*Phi.shape[1]+2,Phi.shape[2]), float)
            modes[:,0:2,:] = self.xy[:,:,np.newaxis]
            for i in range(Phi.shape[1]):
                modes[:,2*i+2,:] = Phi[0:self.M//2,i,:]
                modes[:,2*i+3,:] = Phi[self.M//2:self.M,i,:]
            Lam_s, p_s = np.zeros((2, Lam.shape[1],Lam.shape[0]+1), float)
            Lam_s[:,0], p_s[:,0] = freq, freq
            Lam_s[:,1:], p_s[:,1:] = Lam.T, p.T

            headerline = f'TITLE="Eigenvalues" VARIABLES="frequency", '
            headerline += ', '.join([f'"mode{i+1}"' for i in range(Lam.shape[0])])
            np.savetxt(os.path.join(self.dir, f'EigenValues.dat'), Lam_s, fmt='%8.6f', delimiter='\t', header=headerline, comments='')
            headerline = f'TITLE="Energy Distribution" VARIABLES="frequency", '
            headerline += ', '.join([f'"mode{i+1}"' for i in range(p.shape[0])])
            np.savetxt(os.path.join(self.dir, f'EnergyDistribution.dat'), p_s, fmt='%8.6f', delimiter='\t', header=headerline, comments='')

            if self.fmode == 'dat':
                hl = ', '.join([f'"u{i+1}", "v{i+1}"' for i in range(Phi.shape[1])]) + f' ZONE I={nx}, J={ny}'
                for f in range(Phi.shape[2]):
                    headerline = f'TITLE="Mode Fields for freq={freq[f]}" VARIABLES="x", "y", {hl}'
                    np.savetxt(os.path.join(self.dir, f'modesAtFreq={freq[f]:0.3}.dat'), modes[:,:,f], fmt='%8.6f', delimiter='\t', header=headerline, comments='')
            elif self.fmode == 'h5':
                variables = ['x', 'y']
                for i in range(Phi.shape[1]):
                    variables.append(f'u{i+1}')
                    variables.append(f'v{i+1}')
                grps = [f'mode field at freq={freq[f]:0.3f}' for f in range(Phi.shape[2])]
                tools.save_h5(os.path.join(self.dir, 'spod_modes.h5'), modes, variables, mode='1D', grp_names=grps, naming=1)


    @staticmethod
    def saveSettings(exp, analysis, rec, stg_file):
        settings = ConfigParser()
        settings['Experiment'] = exp
        settings['Analysis'] = analysis
        settings['Reconstruction'] = rec
        with open(stg_file, 'w') as fl:
            fl.write('# Modal Analysis Settings:\n\n')
            settings.write(fl)


    @staticmethod
    def loadSettings(stg_file):
        settings = ConfigParser()
        settings.read(stg_file)
        return settings['Experiment'], settings['Analysis'], settings['Reconstruction']




if __name__ == "__main__":

    #code to run spatial pod analysis with setting file

    t1 = time.time()
    stg_file = r'E:\Temp\Re11_medium\Modal_Settings.ini'
    exp, analysis, rec = OrderedDict(), OrderedDict(), OrderedDict()
    exp, analysis, rec = ModalAnalysis.loadSettings(stg_file)
    experiments = glob.glob(os.path.join(exp['dir'], exp['exp']))
    for experiment in experiments:
        runs = glob.glob(os.path.join(experiment, exp['run']))
        for run in runs:
            path = os.path.join(run, 'Analysis')
            print(f'modal analysis: {run}')
            modal = ModalAnalysis(path, nfiles=int(exp['nf']), pattern=exp['pat'])

            if analysis['mt'] == 'Singular Value Decomposition':
                if analysis['st'] == 'True':
                    print('runing SVD...')
                    modal.svd(nmode=int(analysis['nm']))
                if rec['st'] == 'True':
                    print('reconstructing flow field...')
                    modal.reconstructField(nmode=int(rec['nm']), nsp=int(rec['ns']))
            elif analysis['mt'] == 'Snapshots Method':
                if analysis['st'] == 'True':
                    print('runing snapshots method...')
                    modal.snapshot(nmode=int(analysis['nm']))
                if rec['st'] == 'True':
                    print('reconstructing flow field...')
                    modal.reconstructField(nmode=int(rec['nm']), nsp=int(rec['ns']))
            elif analysis['mt'] == 'Spectral POD':
                if analysis['sst'] == 'True':
                    print('runing SPOD ...')
                    modal.spectralpod(nperseg=int(analysis['nps']), noverlap=int(analysis['nol']), fs=float(analysis['fs']),
                        flim=float(analysis['flim']), windowing=analysis['win'], fdim=float(analysis['fdim']))
                if rec['st'] == 'True':
                    print('extracting frequency fields...')
                    fd = []
                    for f in rec['fd'].split(','):
                        fd.append(float(f))
                    modal.extractFreqField(fd, fs=float(analysis['fs']), nperseg=int(analysis['nps']), noverlap=int(analysis['nol']),
                        windowing=analysis['win'], fdim=float(analysis['fdim']), method=rec['mt'])
    


    t = time.time() - t1
    print(f'Modal Analysis finished in: {t} sec')

    # spectral POD run
    # import time
    # t1 = time.time()
    # path = r'G:\Re11_medium\theta000deg\Analysis'
    # modal = ModalAnalysis(path, 500, '*.h5')
    # modal.spectralpod(nperseg=128, noverlap=108, fs=14.5, flim=0.6, windowing=False, fdim=0.27166)
    # Ar = modal.extractFreqField(fd=[0.185,0.21], fs=14.5, nperseg=128, noverlap=108, fdim=0.26737, method='fft')
    # print(f'done in {time.time()-t1} sec')

