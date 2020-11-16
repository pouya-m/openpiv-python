# Proper Orthogonal Decomposition
# By: Pouya Mohtat 

import os, glob, warnings, time
import numpy as np
import matplotlib.pyplot as plt
from openpiv import tools


class ModalAnalysis():
    def __init__(self, path, nfiles, pattern):
        self.path = path
        self.N = nfiles
        file_list = glob.glob(os.path.join(path, pattern))
        file_list.sort()
        self.file_list = file_list[:nfiles]
        self.npoints = np.loadtxt(file_list[0], skiprows=1).shape[0]
        self.M = 2 * self.npoints
        self.dir = os.path.join(path, 'Modal Analysis')
        if os.path.isdir(self.dir)==False:
            os.mkdir(self.dir)

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
        A = self.constructDataMatrix()
        u, w, vh = np.linalg.svd(A, full_matrices=False)
        w, u, p = self.sortEignvalues(w, u)
        #calculate the coefficients
        if nmode != 'all':
            u = u[:,0:nmode]
        a = np.matmul(u.T, A)
        self.saveData(u, w, p, a)

        return u, w, a, p

    def snapshot(self, nmode='all'):
        """runs the modal analysis with snapshot method and returns modes with
        temporal coefficients and their power distribution

        Parameters
        ----------
        A : 2d np.ndarray
            field data

        nmode : int or 'all', optional
            number of modes to calculate and save. the default is 'all'

        Returns
        -------
        u, a : 2d np.ndarray
            mode array and coefficient array respectively
        
        w, p : 1d np.ndarray
            singular values and power density array respectively
        """
        #find eignvalues and eignvectors of temporal corelation matrix
        A = self.constructDataMatrix()
        C = np.matmul(A.T, A)
        w, v = np.linalg.eig(C)
        #sort the modes (use sqrt(w) to get power levels reflecting values for matrix A instead of C)
        w, v , p = self.sortEignvalues(np.sqrt(w), v)
        #calculate the eign vectors of A
        if nmode == 'all':
            nmode = A.shape[1]    
        u = np.zeros((A.shape[0], nmode))
        for i in range(nmode):
            for j in range(A.shape[1]):
                u[:,i] += v[j,i] * A[:,j]
            u[:,i] /= w[i]
        #calculate coefficients
        a = np.matmul(u.T, A)
        self.saveData(u, w, p, a)
        return u, w, a, p

    def constructDataMatrix(self):
        """reads all files and returns xy info and the data matrix
        """
        A = np.zeros((self.M, self.N))

        #loop to read all files and collect data matrix
        for i in range(self.N):
            data = np.loadtxt(self.file_list[i], skiprows=1)
            A[0:self.M//2, i] = data[:, 2]
            A[self.M//2:self.M, i] = data[:, 3]

        return A

    def sortEignvalues(self, w, u):
        """ Sorts w in descending order and rearranges columns of u accordingly
            also calculates the power density distribution according to eignvalues
        """

        w_sorted = np.sort(w)[::-1]
        arg_sort = np.argsort(w)[::-1]
        u_sorted = np.zeros(u.shape)
        for i, arg in enumerate (arg_sort):
            u_sorted[:,i] = u[:,arg]
        p = np.cumsum(w_sorted**2)*100/np.sum(w_sorted**2)
        
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
        A_r = np.zeros((self.M, nsp))
        for i in range(nsp):
            for j in range(nmode):
                A_r[:,i] += a[j,i] * u[:,j]
        self.saveData(A_r=A_r)

        return A_r

    def saveData(self, u=None, w=None, p=None, a=None, A_r=None):
        """write data in the "Modal Analysis" directory
        """
        # get grid info
        sample = np.loadtxt(self.file_list[0], skiprows=1)
        nx = len(np.unique(sample[:,0]))
        ny = self.npoints//nx

        if u is not None:
            #saving modes data
            modes = np.zeros((self.npoints, 2*u.shape[1]+2))
            modes[:,0:2] = sample[:,0:2]
            for i in range(u.shape[1]):
                modes[:,2*i+2] = u[0:self.M//2,i]
                modes[:,2*i+3] = u[self.M//2:self.M,i]
            headerline = 'TITLE="Mode Fields" VARIABLES="x", "y", '
            headerline += ', '.join([f'"u{i}", "v{i}"' for i in range(u.shape[1])])
            headerline += f' ZONE I={nx}, J={ny}'
            np.savetxt(os.path.join(self.dir, 'Modes.dat'), modes, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

        if w is not None:
            #saving w and p data
            wp = np.zeros((w.size,3))
            wp[:,0], wp[:,1], wp[:,2] = range(w.size), w, p
            headerline = 'TITLE="eignvalues and energy distribution" VARIABLES="mode", "eignvalue", "energy percentage"'
            np.savetxt(os.path.join(self.dir, 'Energy Distribution.dat'), wp, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

        if a is not None:
            #saving temporal coefficients
            ap = np.zeros((a.shape[1], a.shape[0]+1), float)
            ap[:,0] = np.arange(a.shape[1]) + 1
            ap[:,1:] = a.T
            headerline = 'TITLE="temporal coefficients" VARIABLES="snapshot", '
            headerline += ', '.join([f'"a{i}"' for i in range(a.shape[0])])
            np.savetxt(os.path.join(self.dir, 'Coefficients.dat'), ap, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

        if A_r is not None:
            #saving the reconstructed flow fields
            A_rr = np.zeros((self.npoints, 4))
            A_rr[:,0:2] = sample[:,0:2]
            for i in range(A_r.shape[1]):
                A_rr[:,2] = A_r[0:self.M//2,i]
                A_rr[:,3] = A_r[self.M//2:self.M,i]
                headerline = f'TITLE="Reconstructed Fields {i+1}" VARIABLES="x", "y", "u", "v" ZONE I={nx}, J={ny}'
                np.savetxt(os.path.join(self.dir, f'ReconstructedField{i+1:06}.dat'), A_rr, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

    @staticmethod
    def saveSettings(exp, analysis, reconst, stg_file):
        with open(stg_file, 'w') as fh:
            fh.write('Modal analysis settings:\n')
            fh.write('\nexperiment:\n')
            fh.write('\t{0:<30};{1}\n'.format('directory:', exp['dir']))
            fh.write('\t{0:<30};{1}\n'.format('exp::', exp['exp']))
            fh.write('\t{0:<30};{1}\n'.format('run:', exp['run']))
            fh.write('\t{0:<30};{1:<30};{2}\n'.format('files:', exp['pat'], exp['nf']))
            fh.write('\nAnalysis:\n')
            fh.write('\t{0:<30};{1}\n'.format('state:', analysis['st']))
            fh.write('\t{0:<30};{1}\n'.format('method:', analysis['mt']))
            fh.write('\t{0:<30};{1}\n'.format('number of modes:', analysis['nm']))
            fh.write('\nReconstruction:\n')
            fh.write('\t{0:<30};{1}\n'.format('state:', reconst['st']))
            fh.write('\t{0:<30};{1}\n'.format('number of modes:', reconst['nm']))
            fh.write('\t{0:<30};{1}\n'.format('number of snapshots:', reconst['ns']))

    @staticmethod
    def loadSettings(stg_file):
        lines = []
        with open(stg_file, 'r') as fh:
            for line in fh:
                lines.append(line[:-1])
        #extract and set values
        exp, analysis, reconst = {}, {}, {}
        *_, exp['dir'] = lines[3].split(';')
        *_, exp['exp'] = lines[4].split(';')
        *_, exp['run'] = lines[5].split(';')
        *_, exp['pat'], exp['nf'] = [lines[6].split(';')[i].strip() for i in range(3)]
        *_, analysis['st'] = lines[9].split(';')
        *_, analysis['mt'] = lines[10].split(';')
        *_, analysis['nm'] = lines[11].split(';')
        *_, reconst['st'] = lines[14].split(';')
        *_, reconst['nm'] = lines[15].split(';')
        *_, reconst['ns'] = lines[16].split(';')

        return exp, analysis, reconst



#code to test svd/snapshot
if __name__ == "__main__":
    
    t1 = time.time()

    stg_file = r'E:\Temp\Re11_medium\Modal_Settings.dat'
    exp, analysis, reconst = ModalAnalysis.loadSettings(stg_file)
    for experiment in exp['exp'].split(','):
        for run in exp['run'].split(','):
            experiment = experiment.strip()
            run = run.strip()
            path = os.path.join(exp['dir'], experiment, run, 'Analysis')
            print(f'modal analysis: {experiment}\{run}')
            modal = ModalAnalysis(path, nfiles=int(exp['nf']), pattern=exp['pat'])
            if analysis['st'] == 'True':
                if analysis['mt'] == 'Singular Value Decomposition':
                    print('runing SVD...')
                    modal.svd(nmode=int(analysis['nm']))
                elif analysis['mt'] == 'Snapshots Method':
                    print('runing snapshot method...')
                    modal.snapshot(nmode=int(analysis['nm']))
            if reconst['st'] == 'True':
                print('recontructing flow field...')
                modal.reconstructField(nmode=int(reconst['nm']), nsp=int(reconst['ns']))
    
    t = time.time() - t1
    print(f'Modal Analysis finished in: {t} sec')

