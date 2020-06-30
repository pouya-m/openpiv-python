import os, warnings
import glob
import numpy as np
import matplotlib.pyplot as plt

def modal_svd(file_list, nmode='all'):
    """runs the svd analysis and returns modes with temporal coefficients and
    their power distribution

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

    #find singular values and sort them
    A = construct_datamatrix(file_list)
    u, w, vh = np.linalg.svd(A, full_matrices=False)
    w, u, p = sort_eignvalues(w, u)
    #calculate the coefficients
    if nmode != 'all':
        u = u[:,0:nmode]
    a = np.matmul(u.T, A)
    write_data(file_list, u, w, p, a)
    return u, w, a, p

def modal_snapshot(file_list, nmode='all'):
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
    A = construct_datamatrix(file_list)
    C = np.matmul(A.T, A)
    w, v = np.linalg.eig(C)
    #sort the modes (use sqrt(w) to get results reflecting values for matrix A instead of C)
    w, v , p = sort_eignvalues(np.sqrt(w), v)
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
    write_data(file_list, u, w, p, a)
    return u, w, a, p

def construct_datamatrix(file_list):
    """reads all files and returns xy info and the data matrix
    """
    N = len(file_list)
    M = np.loadtxt(file_list[0], skiprows=1).shape[0]
    A = np.zeros((2*M, N))

    #loop to read all files and collect data matrix
    for i in range(N):
        data = np.loadtxt(file_list[i], skiprows=1)
        A[0:M, i] = data[:, 2]
        A[M:2*M, i] = data[:, 3]

    return A

def sort_eignvalues(w, u):
    """ Sorts w in descending order and rearranges columns of u accordingly
        also calculates the power density distribution according to eignvalues
    """

    w_sorted = np.sort(w)[::-1]
    arg_sort = np.argsort(w)[::-1]
    u_sorted = np.zeros(u.shape)
    for i, arg in enumerate (arg_sort):
        u_sorted[:,i] = u[:,arg]
    p = np.cumsum(w_sorted)*100/np.sum(w_sorted)
    
    return w_sorted, u_sorted, p

def reconstruct_field(file_list, nmode='all', nsp='all'):
    """ reconstructs the field using the given number of modes

    Parameters
    ----------
    file_list : list of strings
        absolute path to data files

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
    path = os.path.dirname(file_list[0])
    a = np.loadtxt(os.path.join(path,'Modal Analysis/Coefficients.txt'), skiprows=1)
    data = np.loadtxt(os.path.join(path,'Modal Analysis/Modes.txt'), skiprows=1)
    M = 2*data.shape[0]
    N = a.shape[0]
    u = np.zeros((M, N))
    for i in range(N):
        u[0:M//2,i] = data[:,2*i+2]
        u[M//2:M,i] = data[:,2*i+3]
    #check nsp and nmode
    if nsp == 'all':
        nsp = a.shape[1]
    if nsp > a.shape[1]:
        warnings.warn(f'number of snapshots to reconstruct cannot be larger than the original number\
        of snapshots, nsp was set to its maximum possible value: {a.shape[1]}', Warning)
        nsp = a.shape[1]
    if nmode == 'all':
        nmode = a.shape[0]
    if nmode > a.shape[0]:
        warnings.warn(f'number of modes to use cannot be larger than the original number\
        of modes, nmode was set to its maximum possible value: {a.shape[0]}', Warning)
        nmode = a.shape[0]
    #reconstruct snapshots using u and a
    A_r = np.zeros((u.shape[0], nsp))
    for i in range(nsp):
        for j in range(nmode):
            A_r[:,i] += a[j,i] * u[:,j]
    write_data(file_list, A_r=A_r)

    return A_r

def write_data(file_list, u=None, w=None, p=None, a=None, A_r=None):
    """write data in the "Modal Analysis" directory
    """
    #creating directory for modal analysis results
    save_dir = os.path.join(os.path.dirname(file_list[0]), 'Modal Analysis')
    if os.path.isdir(save_dir)==False:
        os.mkdir(save_dir)
    sample = np.loadtxt(file_list[0], skiprows=1)
    nx = int((sample[-1,0]-sample[0,0])/(sample[1,0]-sample[0,0]) + 1)
    M = sample.shape[0]
    if u is not None:
        #saving modes data
        modes = np.zeros((M, 2*u.shape[1]+2))
        modes[:,0:2] = sample[:,0:2]
        for i in range(u.shape[1]):
            modes[:,2*i+2] = u[0:M,i]
            modes[:,2*i+3] = u[M:2*M,i]
        headerline = 'TITLE="Mode Fields" VARIABLES="x", "y", '
        headerline += ', '.join([f'"u{i}", "v{i}"' for i in range(u.shape[1])])
        headerline += f' ZONE I={nx}, J={M//nx}'
        np.savetxt(os.path.join(save_dir, 'Modes.txt'), modes, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    if w is not None:
        #saving w and p data
        wp = np.zeros((w.size,3))
        wp[:,0], wp[:,1], wp[:,2] = range(w.size), w, p
        headerline = 'TITLE="eignvalues and energy distribution" VARIABLES="mode", "eignvalue", "energy percentage"'
        np.savetxt(os.path.join(save_dir, 'Energy Distribution.txt'), wp, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    if a is not None:
        #saving temporal coefficients
        headerline = 'Temporal Coefficients, each row represents the variation of the respective modal coefficient over time'
        np.savetxt(os.path.join(save_dir, 'Coefficients.txt'), a, fmt='%8.4f', delimiter='\t', header=headerline, comments='')
    if A_r is not None:
        #saving the reconstructed flow fields
        A_rr = np.zeros((M, 2*A_r.shape[1]+2))
        A_rr[:,0:2] = sample[:,0:2]
        for i in range(A_r.shape[1]):
            A_rr[:,2*i+2] = A_r[0:M,i]
            A_rr[:,2*i+3] = A_r[M:2*M,i]
        headerline = 'TITLE="Reconstructed Fields" VARIABLES="x", "y", '
        headerline += ', '.join([f'"u{i}", "v{i}"' for i in range(A_r.shape[1])])
        headerline += f' ZONE I={nx}, J={M//nx}'
        np.savetxt(os.path.join(save_dir, 'Reconstructed Fields.txt'), A_rr, fmt='%8.4f', delimiter='\t', header=headerline, comments='')

def draw_field(file_list, draw, nmode, **kwarg):
    """plots the vector field for the given mode/reconstructed snapshot

    Parameters
    ----------
    file_list : string
        absolute path to data files
    
    draw : string
        string indicating the property to draw, acceptable choices
        are: 'modes' or 'reconstructed'

    nmode : int
        number of mode or reconstructed snapshot to plot
    """
    path = os.path.dirname(file_list[0])
    if draw == 'modes':
        filename = os.path.join(path,'Modal Analysis/Modes.txt')
    elif draw == 'reconstructed':
        filename = os.path.join(path,'Modal Analysis/Reconstructed Fields.txt')
    else:
        raise ValueError('only acceptable choices for draw are: "modes" or "reconstructed"')
    data = np.loadtxt(filename, skiprows=1)
    plt.quiver(data[:,0], data[:,1], data[:,2*nmode+2], data[:,2*nmode+3], color='b', **kwarg)
    plt.show()


#code to test svd/snapshot
path = os.path.dirname(os.path.abspath(__file__))
file_list = glob.glob(path+'\Dummy Data\d*.vec')
file_list.sort()

u, w, a, p = modal_snapshot(file_list)
A_r = reconstruct_field(file_list)
draw_field(file_list, 'reconstructed', 1)
#plt.plot(p)
plt.show()

