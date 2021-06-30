# Compilation of tools to do post processing of data,
# including calculations of vorticity and temporal analysis such as calculation of mean and fluctuating velocity components, turbulent kinetic energy and Reynolds stresses
# Vorticity calculations are accurate! it has been validated against base Matlab code and Tecplot calculaions. All calculations are vectorized to reduce run time.
# By: Pouya Mohtat
# Revision 0.2: Mar, 2021

# Change Log:
# - added .h5 file support which reduces the final file size to half and speeds up the reading of data for other parts of the program significantly
# - some code refracting and cleanup

# To do:
# ------------
# 1- A second order difference method can be implimented to calculate vorticity. It may increase the robustness of the vorticity results to noisy velocity signals.

# 2- This script takes the unvalidated piv outputs and does post processing on those results. in the GUI we are doing the same thing only that we are doing it on 
#    x, y, u, v results directly instead of reading it from files (to increase speed, obviously). so there is some duplicate code that could be refracted. -> done


import numpy as np
from openpivtk import tools, validation, smoothn, filters, scaling
import matplotlib.pyplot as plt
import os, glob
import multiprocessing
from functools import partial
from collections import OrderedDict
from configparser import ConfigParser


def vorticity(u,v,x,y):
    """"Calculates vorticity for a velocity field with coordinates x and y
    the vorticity field is calculated using a first order central difference method

    Parameters
    ----------
    u, v : 2d np.ndarray
        u and v velocity fields

    x, y : 2d np.ndarray
        two dimentional arrays containing x and y coordinates of the mesh grid 

    Returns
    -------
    vor : 2d np.ndarray
        the vorticity field
    """
    dv_dx = np.zeros(x.shape)
    du_dy = np.zeros(y.shape)
    nx = np.unique(x)
    ny = np.unique(y)
    for iy in range(len(ny)):
        dv_dx[iy,:] = getSlope( v[iy,:], x[iy,:] )
    for ix in range(len(nx)):
        du_dy[:,ix] = getSlope( u[:,ix], y[:,ix] )
    return dv_dx - du_dy

def getSlope(y,x):
    """calculates the dy/dx slope: (y(n+1) - y(n)) / (x(n+1) - x(n))

    Parameters
    ----------
    y,x : 1d np.ndarray 
        1 dimentional arrays containing x and y(x) values

    Returns
    -------
    slope : 1d np.ndarray
        the dy/dx array
    """
    xp = np.pad(x, 1, 'edge')
    yp = np.pad(y, 1, 'edge')
    slope = (yp[2:] - yp[:-2])/(xp[2:] - xp[:-2])
    return slope

def calcAvgField(file_list, col_list=[2,3]):
    """Calculates the average field for the given list of columns

    Parameters
    ----------
    file_list : List of strings
        absolute path to the files containing flow data

    col_list : list of columns
        a list of columns for which the average needs to be calculated.
        the default is columns 2 and 3 which represent the u and v velocities respectively.

    Returns
    -------
    AVG : tuple of n arrays
        the average field data. the number of elements in the returned tuple depends on the len(col_list)
    """
    ntime = len(file_list)
    sample = np.loadtxt(file_list[0], skiprows=1)
    AVG = np.zeros((sample.shape[0], len(col_list)), sample.dtype)
    for i in range(ntime):
        data = np.loadtxt(file_list[i], skiprows=1)
        AVG += data[:,col_list]
    AVG = AVG / ntime

    return np.hsplit(AVG, AVG.shape[1])


def postProcess(file_name, pro, pos, data=None):
    """Carries out the post processing for a minimal output. does the following:
        validation and vector replacement, smoothing, field manipulation, scaling 
        and calculation of vorticity and velocity magnitude


    Parameters
    ----------
    file_name : string
        absolute path to the data file

    pro, pos : dictionary
        dictionaries containing processing and postprocessing settings

    saveLoc: string
        absolute path to the folder for saving results. default is None which means
        results are returned without saving to file.

    header: string
        the header line that is saved to the file.

    Returns
    -------
    basename : string
        file name
    
    x, y, u, v, mask, vor, velMag : 2D np.ndarray
        field data
    """
    #read data
    if data is None:
        x, y, u, v, s2n = tools.load(file_name)
    else:
        x, y, u, v, s2n = data
    #validation
    mask = np.zeros(u.shape, dtype=bool)
    if pos['s2n_st'] == 'True':
        mask1 = validation.sig2noise_val( u, v, s2n, threshold = float(pos['s2n_ra']) )
        mask = mask | mask1
    if pos['gv_st'] == 'True':
        umin, umax = map(float, pos['gv_ul'].split(','))
        vmin, vmax = map(float, pos['gv_vl'].split(','))
        mask2 = validation.global_val( u, v, (umin, umax), (vmin, vmax) )
        mask = mask | mask2
    if pos['lv_st'] == 'True':
        udif, vdif = map(float, pos['lv_df'].split(','))
        mask3 = validation.local_median_val(u, v, udif, vdif, size=int(pos['lv_kr']))
        mask = mask | mask3
    if pos['std_st'] == 'True':
        mask4 = validation.global_std(u, v, std_threshold=float(pos['std_ra']))
        mask = mask | mask4
    # vector corrections
    if pos['bv_st'] == 'True':
        u[mask], v[mask] = np.nan, np.nan
        u, v = filters.replace_outliers( u, v, method=pos['bv_mt'], max_iter=int(pos['bv_ni']), kernel_size=int(pos['bv_kr']))
    if pos['sm_st'] == 'True':
        u_ra, v_ra = map(float, pos['sm_ra'].split(','))
        u, *_ = smoothn.smoothn(u, s=u_ra)
        v, *_ = smoothn.smoothn(v, s=v_ra)
    if pos['fm_st'] == 'True':
        for fm in pos['fm_in'].split(','):
            x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode=fm.strip())
    # scaling
    scale = float(pro['sc'])
    x, y, u, v = scaling.uniform(x, y, u, v, scaling_factor = scale)
    # calculate vorticity and velocity magnitude
    vor = vorticity(u, v, x, y)
    velMag = np.sqrt(u*u + v*v)

    basename = os.path.basename(file_name)

    return basename, u, v, mask, vor, velMag


def startPostProcess(file_list, pro, pos, save_type='dat'):
    """Carries out the post processing and saves the results
    """
    # do the post-proccessing
    pool = multiprocessing.Pool(processes=int(pro['nc']))
    func = partial(postProcess, pro=pro, pos=pos)
    data = pool.map(func, file_list)

    # initialize variables to hold data
    Nt = len(file_list)
    x, y, u, v, mask = tools.load(file_list[0])
    # do field manipulation and scaling on x and y
    if pos['fm_st'] == 'True':
        for fm in pos['fm_in'].split(','):
            x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode=fm.strip())
    scale = float(pro['sc'])
    x, y = x/scale, y/scale
    u, v, mask, vor, velMag = np.zeros((5, x.shape[0], x.shape[1], Nt), np.float)
    basename = np.zeros((Nt,), 'U50')
    # unpack data
    for n, D in enumerate(data):
        basename[n], u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n] = D
    del(data)
    # save the results
    analysis_path = os.path.dirname(os.path.dirname(file_list[0]))
    saveResults([x, y, basename, u, v, mask, vor, velMag], pos, analysis_path, save_type)


def saveResults(data, pos, analysis_path, save_type):
    x, y, basename, u, v, mask, vor, velMag = data
    # extended output
    if pos['out_m'] == 'extended':
        # calculate mean values
        um, vm, vorm = u.mean(axis=2), v.mean(axis=2), vor.mean(axis=2)
        # calculate fluctuations
        up = u - um[...,np.newaxis]
        vp = v - vm[...,np.newaxis]
        upvp = up * vp
        TKE = 0.5 * (up*up + vp*vp)
        upupm = (up*up).mean(axis=2)
        vpvpm = (vp*vp).mean(axis=2)
        upvpm = upvp.mean(axis=2)
        TKE_rms = 0.5 * (upupm + vpvpm)
        # save the results
        avg_file = os.path.join(analysis_path, 'AVG.dat')
        header = '"x", "y", "u_avg", "v_avg", "vorticity_avg", "upup_avg", "vpvp_avg", "upvp_avg", "TKE_rms"'
        tools.save( x, y, filename=avg_file, variables=[um, vm, vorm, upupm, vpvpm, upvpm, TKE_rms], header=header )

        if save_type == 'dat':
            header = '"x", "y", "u", "v", "mask", "vorticity", "velocity magnitude", "up", "vp", "upvp", "TKE"'
            for n, bn in enumerate(basename):
                fname = os.path.join(analysis_path, bn+'.dat')
                tools.save( x, y, filename=fname, variables=[u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n], up[:,:,n], vp[:,:,n], upvp[:,:,n], TKE[:,:,n]], header=header )

        elif save_type == 'h5':
            variables=['x', 'y', 'u', 'v', 'mask', 'vorticity', 'velocity magnitude', 'up', 'vp', 'upvp', 'TKE']
            xp = np.repeat(x[...,np.newaxis], len(basename), axis=2)
            yp = np.repeat(y[...,np.newaxis], len(basename), axis=2)
            run = os.path.basename(os.path.dirname(analysis_path))
            fname = os.path.join(analysis_path, f'{run}.h5')
            tools.save_h5(fname, [xp, yp, u, v, mask, vor, velMag, up, vp, upvp, TKE], variables, mode='2D', grp_names=basename, naming='')

    # simple output
    elif pos['out_m'] == 'simple':
        if save_type == 'dat':
            header = '"x", "y", "u", "v", "mask", "vorticity", "velocity magnitude"'
            for n, bn in enumerate(basename):
                fname = os.path.join(analysis_path, bn+'.dat')
                tools.save(x, y, filename=fname, variables=[u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n]], header=header)

        elif save_type == 'h5':
            variables=['x', 'y', 'u', 'v', 'mask', 'vorticity', 'velocity magnitude']
            xp = np.repeat(x[...,np.newaxis], len(basename), axis=2)
            yp = np.repeat(y[...,np.newaxis], len(basename), axis=2)
            run = os.path.basename(os.path.dirname(analysis_path))
            fname = os.path.join(analysis_path, f'{run}.h5')
            tools.save_h5(fname, [xp, yp, u, v, mask, vor, velMag], variables, mode='2D', grp_names=basename, naming='')


def saveSettings(exp, pre, pro, pos, file_name):
    """Saves the settings given in exp, pre, pro and pos dictionaries to the file_name
    """
    settings = ConfigParser()
    settings['Experiment'] = exp
    settings['Pre-process'] = pre
    settings['Process'] = pro
    settings['Post-process'] = pos
    with open(file_name, 'w') as fl:
        fl.write('# PIV Process Settings:\n\n')
        settings.write(fl)


def loadSettings(file_name):
    """Loads the settings and returns exp, pre, pro and pos dictionaries
    """
    settings = ConfigParser()
    settings.read(file_name)
    
    return settings['Experiment'], settings['Pre-process'], settings['Process'], settings['Post-process']


def convert2h5(path, patt, variables, fname):
    file_list = glob.glob(os.path.join(path, patt))
    file_list.sort()
    temp = np.loadtxt(file_list[0], skiprows=1)
    data = np.zeros((temp.shape[0],temp.shape[1],len(file_list)), temp.dtype)
    for i, f in enumerate(file_list):
        data[:,:,i] = np.loadtxt(f, skiprows=1)
    tools.save_h5(fname, data, variables, mode='1D')
    

# code to test functions
if __name__ == "__main__":
    r'''
    # vorticity
    filename = r'C:\Users\Asus\Desktop\UI\Dummy Data\fixed000001n.dat'
    x, y, u, v, mask = tools.load(filename)
    vor = vorticity(u,v,2.16215,2.16215)
    plt.imshow(vor,cmap='viridis', vmin=-40, vmax=40, interpolation='spline16', origin='lower', extent=(x.min(),x.max(),y.min(),y.max()))
    plt.show()
    
    # AVG
    path = r'E:\Temp\Zoomed in Cylinder\Fixed180\Analysis'
    file_list = glob.glob(path+'\Theta1800deg000???.dat')
    file_list.sort()
    u_avg, v_avg, vor_avg = calcAvgField(file_list, col_list=[2,3,4])
    x, y, u, v, mask = tools.load(file_list[0])
    save_file = os.path.join(path, 'AVG.dat')
    tools.save(x, y, u_avg, v_avg, vor_avg, save_file)
    plt.quiver(x,y,u_avg,v_avg)
    plt.show()
    
    # save data
    filename = r'C:\Users\Asus\Desktop\UI\Dummy Data\fixed000001n.dat'
    x, y, u, v, mask = tools.load(filename)
    vor = vorticity(u,v,2.16215,2.16215)
    fname = os.path.join(os.path.dirname(filename), 'test.dat')
    tools.save(x, y, filename=fname, header='"x", "y", "u", "v", "mask", "vorticity"', variables=[u, v, mask, vor])
    
    # settings
    filename = r'E:\repos\openpiv-python\openpiv\pouya\UI\Process_Settings.dat'
    exp, pre, pro, pos = loadSettings(filename)
    
    from collections import defaultdict as ddict
    import pprint

    pprint.pprint(pos)
    pos['out_m'] = 'extended'
    saveSettings(exp, pre, pro, pos, filename)
    exp2, pr2e, pro2, pos2 = loadSettings(filename)
    pprint.pprint(pos2)
    
    exp = ddict(lambda: '')
    pre = ddict(lambda: '')
    pro = ddict(lambda: '')
    filename = r'C:\Users\Asus\Desktop\UI\Dummy Data\test.dat'
    saveSettings(exp, pre, pro, pos, filename)
    exp, pre, pro, pos = loadSettings(filename)
    pprint.pprint(exp)
    pprint.pprint(pos)

    # test convertSaveType
    import time
    t1 = time.time()
    path = r'G:\Re11_medium\theta180deg\Analysis'
    variables = ['x', 'y', 'u', 'v', 'mask', 'vorticity', 'vel_mag', 'up', 'vp', 'upvp', 'TKE']
    convert2h5(path, 'theta*.dat', variables, fname=os.path.join(path, 'data.h5'))
    print(f'conversion took: {time.time()-t1:.2f} sec')
    '''

    # test output
    setting_file = r'C:\Users\Asus\Desktop\Dummy Data\exp1\Processing_Settings.ini'
    exp, pre, pro , pos = OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict()
    exp, pre, pro, pos = loadSettings(setting_file)
    experiments = glob.glob(os.path.join(exp['dir'], exp['exp']))
    experiments.sort()
    for experiment in experiments:
        runs = glob.glob(os.path.join(experiment, exp['run']))
        runs.sort()
        for run in runs:
            print(f'postprocessing: {run}')
            path = os.path.join(run, 'Analysis', 'Unvalidated', '*.dat')
            file_list = glob.glob(path)
            file_list.sort()
            Nfiles = int(exp['nf'])
            if Nfiles != 0:
                file_list = file_list[0:Nfiles]
            startPostProcess(file_list, pro, pos, save_type='h5')
    print('All done!')
