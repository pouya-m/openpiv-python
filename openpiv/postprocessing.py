# Compilation of tools to do post processing of data,
# including calculations of vorticity and temporal analysis such as calculation of mean and fluctuating velocity components, turbulent kinetic energy and Reynolds stresses
# Vorticity calculations are accurate! it has been validated against base Matlab code and Tecplot calculaions. All calculations are performed using vector calculus to reduce run time.
# By: Pouya Mohtat
# Revision 0.2: Nov, 2020

# To do:
# ------------
# 1- A second order difference method can be implimented to calculate vorticity. It may increase the robustness of the vorticity results to noisy velocity signals.

# 2- This script takes the unvalidated piv outputs and does post processing on those results. in the GUI we are doing the same thing only that we are doing it on 
#    x, y, u, v results directly instead of reading it from files (to increase speed, obviously). so there is some duplicate code that could be refracted.


import numpy as np
from openpiv import tools, validation, smoothn, filters, scaling
import matplotlib.pyplot as plt
import os, glob
import multiprocessing
from functools import partial


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


def postProcess(file_name, pro, pos, saveLoc=None, header=None):
    """Carries out the post processing for a minimall output. does the following:
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
    #read file
    x, y, u, v, s2n = tools.read_data(file_name)
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
    if saveLoc != None:
        save_name = os.path.join(saveLoc, basename)
        tools.save(x, y, filename=save_name, variables=[u, v, mask, vor, velMag], header=header)

    return basename, u, v, mask, vor, velMag


def simpleOutput(file_list, pro, pos):
    """Manages the post processing for a minimall output and saves the results
    """
    Analysis_folder = os.path.dirname(os.path.dirname(file_list[0]))
    header = '"x", "y", "u", "v", "mask", "vorticity", "velocity magnitude"'
    
    pool = multiprocessing.Pool(processes=int(pro['nc']))
    func = partial(postProcess, pro=pro, pos=pos, saveLoc=Analysis_folder, header=header)
    pool.map(func, file_list)   


def extendedOutput(file_list, pro, pos):
    """Carries out the post processing for an extended output with temporal analysis and saves the results
    """
    
    # initialize variables to hold data
    Nt = len(file_list)
    x, y, u, v, mask = tools.read_data(file_list[0])
    # do field manipulation and scaling on x and y
    if pos['fm_st'] == 'True':
        for fm in pos['fm_in'].split(','):
            x, y, u, v, mask = tools.manipulate_field(x, y, u, v, mask, mode=fm.strip())
    scale = float(pro['sc'])
    x, y = x/scale, y/scale
    u, v, mask, vor, velMag = np.zeros((5, x.shape[0], x.shape[1], Nt), np.float)
    # get all the data
    #for n, fl in enumerate(file_list):
    #    *_, u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n] = postProcess(fl, pro, pos)
    basename = np.zeros((Nt,), 'U50')
    pool = multiprocessing.Pool(processes=int(pro['nc']))
    func = partial(postProcess, pro=pro, pos=pos, saveLoc=None, header=None)
    data = pool.map(func, file_list)
    for n, D in enumerate(data):
        basename[n], u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n] = D
    del(data)

    # calculate mean values
    um, vm, vorm = u.mean(axis=2), v.mean(axis=2), vor.mean(axis=2)
    # calculate fluctuations
    up = u - um[...,np.newaxis]
    vp = v - vm[...,np.newaxis]
    upvp = up * vp
    TKE = 0.5 * (up*up + vp*vp)
    #TKEm = TKE.mean(axis=2) (this is the same as TKE_rms but has more computational cost to calculate)
    upupm = (up*up).mean(axis=2)
    vpvpm = (vp*vp).mean(axis=2)
    upvpm = upvp.mean(axis=2)
    TKE_rms = 0.5 * (upupm + vpvpm)
    # save the results
    Analysis_folder = os.path.dirname(os.path.dirname(file_list[0]))
    avg_file = os.path.join(Analysis_folder, 'AVG.dat')
    header = '"x", "y", "u_avg", "v_avg", "vorticity_avg", "upup_avg", "vpvp_avg", "upvp_avg", "TKE_rms"'
    tools.save( x, y, filename=avg_file, variables=[um, vm, vorm, upupm, vpvpm, upvpm, TKE_rms], header=header )

    header = '"x", "y", "u", "v", "mask", "vorticity", "velocity magnitude", "up", "vp", "upvp", "TKE"'
    for n, bn in enumerate(basename):
        save_name = os.path.join(Analysis_folder, bn)
        tools.save( x, y, filename=save_name, variables=[u[:,:,n], v[:,:,n], mask[:,:,n], vor[:,:,n], velMag[:,:,n], up[:,:,n], vp[:,:,n], upvp[:,:,n], TKE[:,:,n]], header=header )


def saveSettings(exp, pre, pro, pos, file_name):
    """Saves the settings given in exp, pre, pro and pos dictionaries to the file_name
    """
    with open(file_name, 'w') as fh:
        fh.write('Process settings:\n\n')
        fh.write('Experiment:\n\t{0:<30};'.format('Directory:'))
        fh.write('{0}\n\t{1:<30};{2}\n\t{3:<30};{4}\n'.format(exp['dir'], 'Experiments:', exp['exp'], 'Runs:', exp['run']))
        fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15}\n\n'.format('Files:', exp['patA'], exp['patB'], exp['nf']))
        fh.write('Pre-Process:\n\t{0:<30};{1:<15};{2:<15};{3:<15};{4:<15}\n'.format('Remove Background:', pre['bg_st'], pre['bg_nf'], pre['bg_cs'], pre['bg_nc']))
        fh.write('\t{0:<30};{1:<15};{2:<15}\n'.format('Static Mask:', pre['sm_st'], pre['sm_pa']))
        fh.write('\t{0:<30};{1:<15}\n\n'.format('Dynamic Mask:', pre['dm_st']))
        fh.write('Process:\n\t{0:<30};{1:<15}\n\t{2:<30};{3:<15}\n\t{4:<30};{5:<15}\n'.format('Window Size:', pro['ws'], 'Search Area Size:', pro['sa'], 'Overlap:', pro['ol']))
        fh.write('\t{0:<30};{1:<15}\n\t{2:<30};{3:<15}\n\t{4:<30};{5:<15}\n'.format('Signal/Noise Method:', pro['s2n'], 'Time Step:', pro['ts'], 'Scale:', pro['sc']))
        fh.write('\t{0:<30};{1:<15}\n\n'.format('Number of CPUs:', pro['nc']))
        fh.write('Post-process:\n\t{0:<30};{1:<15};{2:<15}\n'.format('Signal/Noise:', pos['s2n_st'], pos['s2n_ra']))
        fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15}\n'.format('Global Velocity:', pos['gv_st'], pos['gv_ul'], pos['gv_vl']))
        fh.write('\t{0:<30};{1:<15};{2:<15}\n'.format('Global Standard Deviation:', pos['std_st'], pos['std_ra']))
        fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15}\n'.format('Local Velocity:', pos['lv_st'], pos['lv_df'], pos['lv_kr']))
        fh.write('\t{0:<30};{1:<15};{2:<15};{3:<15};{4:<15}\n'.format('Bad Vector Replacement:', pos['bv_st'], pos['bv_mt'], pos['bv_ni'], pos['bv_kr']))
        fh.write('\t{0:<30};{1:<15};{2:<15}\n\t{3:<30};{4:<15};{5:<15}\n'.format('Vector Smoothing:', pos['sm_st'], pos['sm_ra'], 'Field Manipulation:', pos['fm_st'], pos['fm_in']))
        fh.write('\t{0:<30};{1:<15}\n'.format('Output Mode:', pos['out_m']))


def loadSettings(file_name):
    """Loads the settings and returns exp, pre, pro and pos dictionaries
    """
    lines = []
    with open(file_name, 'r') as fh:
        for line in fh:
            lines.append(line[:-1])
    #extract and set values
    exp, pre, pro, pos = {}, {}, {}, {}
    *_, exp['dir'] = lines[3].split(';')
    *_, exp['exp'] = lines[4].split(';')
    *_, exp['run'] = lines[5].split(';')
    *_, exp['patA'], exp['patB'], exp['nf'] = [lines[6].split(';')[i].strip() for i in range(4)]
    *_, pre['bg_st'], pre['bg_nf'], pre['bg_cs'], pre['bg_nc'] = [lines[9].split(';')[i].strip() for i in range(5)]
    *_, pre['sm_st'], pre['sm_pa'] = [lines[10].split(';')[i].strip() for i in range(3)]
    *_, pre['dm_st'] = [lines[11].split(';')[i].strip() for i in range(2)]
    *_, pro['ws'] = [lines[14].split(';')[i].strip() for i in range(2)]
    *_, pro['sa'] = [lines[15].split(';')[i].strip() for i in range(2)]
    *_, pro['ol'] = [lines[16].split(';')[i].strip() for i in range(2)]
    *_, pro['s2n'] = [lines[17].split(';')[i].strip() for i in range(2)]
    *_, pro['ts'] = [lines[18].split(';')[i].strip() for i in range(2)]
    *_, pro['sc'] = [lines[19].split(';')[i].strip() for i in range(2)]
    *_, pro['nc'] = [lines[20].split(';')[i].strip() for i in range(2)]
    *_, pos['s2n_st'], pos['s2n_ra'] = [lines[23].split(';')[i].strip() for i in range(3)]
    *_, pos['gv_st'], pos['gv_ul'], pos['gv_vl'] = [lines[24].split(';')[i].strip() for i in range(4)]
    *_, pos['std_st'], pos['std_ra'] = [lines[25].split(';')[i].strip() for i in range(3)]
    *_, pos['lv_st'], pos['lv_df'], pos['lv_kr'] = [lines[26].split(';')[i].strip() for i in range(4)]
    *_, pos['bv_st'], pos['bv_mt'], pos['bv_ni'], pos['bv_kr'] = [lines[27].split(';')[i].strip() for i in range(5)]
    *_, pos['sm_st'], pos['sm_ra'] = [lines[28].split(';')[i].strip() for i in range(3)]
    *_, pos['fm_st'], pos['fm_in'] = [lines[29].split(';')[i].strip() for i in range(3)]
    *_, pos['out_m'] = [lines[30].split(';')[i].strip() for i in range(2)]

    return exp, pre, pro, pos
    

# code to test functions
if __name__ == "__main__":
    r'''
    # vorticity
    filename = r'C:\Users\Asus\Desktop\UI\Dummy Data\fixed000001n.dat'
    x, y, u, v, mask = tools.read_data(filename)
    vor = vorticity(u,v,2.16215,2.16215)
    plt.imshow(vor,cmap='viridis', vmin=-40, vmax=40, interpolation='spline16', origin='lower', extent=(x.min(),x.max(),y.min(),y.max()))
    plt.show()
    
    # AVG
    path = r'E:\Temp\Zoomed in Cylinder\Fixed180\Analysis'
    file_list = glob.glob(path+'\Theta1800deg000???.dat')
    file_list.sort()
    u_avg, v_avg, vor_avg = calcAvgField(file_list, col_list=[2,3,4])
    x, y, u, v, mask = tools.read_data(file_list[0])
    save_file = os.path.join(path, 'AVG.dat')
    tools.save(x, y, u_avg, v_avg, vor_avg, save_file)
    plt.quiver(x,y,u_avg,v_avg)
    plt.show()
    
    # save data
    filename = r'C:\Users\Asus\Desktop\UI\Dummy Data\fixed000001n.dat'
    x, y, u, v, mask = tools.read_data(filename)
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
    '''
    # test output
    setting_file = r'E:\Temp\Processing_Settings.dat'
    exp, pre, pro, pos = loadSettings(setting_file)
    import time
    t1 = time.time()
    for experiment in exp['exp'].split(','):
        for run in exp['run'].split(','):
            experiment, run = experiment.strip(), run.strip()
            path = os.path.join(exp['dir'], experiment, run, 'Analysis', 'Unvalidated')
            file_list = glob.glob(path+'\*.dat')
            file_list.sort()
            Nfiles = int(exp['nf'])
            if Nfiles != 0:
                file_list = file_list[0:Nfiles]
            extendedOutput(file_list, pro, pos)
    print(time.time()-t1)
    '''
    # read data
    datafile = r'E:\Temp\Zoomed in Cylinder\Fixed180\Analysis\Theta1800deg000001.dat'
    x, y, u, v, mask, vor, velMag = tools.read_data(datafile, 7)
    plt.imshow(vor,cmap='viridis', vmin=-100, vmax=100, interpolation='spline16', origin='lower')
    plt.show()
    '''