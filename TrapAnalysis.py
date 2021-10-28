'''
 TrapAnalysis.py

 Functions for analyzing position data obtained from the video of
 a trapped bead. Produces information about the optical trap.

 Author: Christopher Dydula, University of Toronto    -    May 23, 2011
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

def my_show():
    '''Display a figure. Same as show() in backend_tkagg.py but without
    Tk.mainloop.
    '''
    for manager in plt._pylab_helpers.Gcf.get_all_fig_managers():
        manager.show()
    
def positions_plot(x, y, frames):
    '''Create a 3d plot of the x and y positions vs frame from the position data
       of a trapped bead video.

       x: array_like
          Array containing the x positions
       y: array_like
          Array containing the y positions
       frames: array_like
          Array containing the frame numbers
    '''

    fig = plt.figure(1)
    ax = Axes3D(fig)
    ax.scatter(x, y, frames, label='Positions', c=frames)
    #ax.legend(loc=9) # legend is placed at top centre, acts as title

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('Frame')
    ax.set_title('Position vs. frame')

    return fig
   # my_show()

def disp_v_frame(direc, frames, varp, name):
    '''Create a plot of a vector of positions in the direction direc vs a
       vector of frames.

       direc: array_like
              Array of positions in the desired direction (x, y or radial)
       frames: array_like
              Array of frame numbers
       varp: array_like
              An array with n variances for the positions in direc, where
              n is the length of direc and frames
       name: string
              Either 'x', 'y' or 'r' for the three respective directions
    '''
    plt.plot(frames, direc, frames, varp, linewidth=0.5)
    plt.xlabel('Frame')
    if name == 'x':
        plt.ylabel('x (m)')
        plt.title('x displacement vs. frame')
        plt.legend(('x for individual frames', '$<x^2>$ = %9.4e' % varp[0]))
    elif name == 'y':
        plt.ylabel('y (m)')
        plt.title('y displacement vs. frame')
        plt.legend(('y for individual frames', '$<y^2>$ = %9.4e' % varp[0]))
    elif name == 'r':
        plt.ylabel('$r^2 (m^2)$')
        plt.title('Radial displacement vs. frame')
        plt.legend(('$r^2$ for individual frames', '$<r^2>$ = %9.4e' % varp[0]))
    plt.grid()

def disp_distr(direc, bins, name):
    '''Create a histogram showing the distribution of the displacements in the
       direction direc (x, y or radial)
       
       direc: array_like
              Array of positions in the desired direction (x, y or radial)
        bins: positive integer
              The number of bins for the histogram
        name: string
              Either 'x', 'y' or 'r' for the three respective directions
    '''
    plt.hist(direc, bins)
    plt.ylabel('Count')
    if name == 'x':
        plt.title('Distribution of x displacements')
        plt.xlabel('Displacement (m)')
    elif name == 'y':
        plt.title('Distribution of y displacements')
        plt.xlabel('Displacement (m)')
    elif name == 'r':
        plt.title('Distribution of radial displacements')
        plt.xlabel('Displacement ($m^2$)')

def rms(x):
    '''Return the root mean square of the values in the array vector x.

       x: array_like
          Array of a numbers
    '''
    return (np.sum(x**2) / np.size(x)) ** (0.5)

def analyze(x, y, temp, psize_um, deltemp, delpsize_um):
    '''Given x and y pixel position data of a bead from a video, convert
       pixel units to metric. Produce 7 plots in two figure windows, a 3d
       position plot in the first and 3 position plots and 3 displacement
       distrubution histograms in the second. Calculate and return trap
       stiffness in the x, y and radial direction.

       x: array_like
          Array containing the x positions (pixels)
       y: array_like
          Array containing the y positions (pixels)

       x and y must be of the same length
    '''
    kb = 1.38065e-23 # [m^2*kg*s^-2*K^-1], boltzmann constant
    T = temp # [K], temperature in room at time of recording of video
    delT = deltemp
    degfree = 2 # number of degrees of freedom

    # pixel sizes and uncertainties in metres
    # by default, every 14.5 pixels in the image is one micrometre, approximately
    # (1 micrometre is 14.5 +/- 0.3 px)
    psize_m = psize_um * 1e-6
    delpsize_m = delpsize_um * 1e-6

    # zero-mean postions in metres
    x -= np.mean(x)
    y -= np.mean(y)
    x_m = x * psize_m
    y_m = y * psize_m
    # x_m -= np.mean(x_m)
    # y_m -= np.mean(y_m)

    # use the standard deviations of x, y as proxies for the pixel uncertainties
    errxpx = np.std(x)
    errypx = np.std(y)

    # uncertainties in x, y values (metres)
    delx_m = ( (psize_m * errxpx)**2 + (x * delpsize_m)**2 )**(0.5)
    dely_m = ( (psize_m * errypx)**2 + (y * delpsize_m)**2 )**(0.5)

    # uncertainty in <r^2>
    delrvar_m = (2/(np.size(x))) * ( np.sum((delx_m*x_m)**2) + np.sum((dely_m*y_m)**2) )**(0.5)

    # calculate <r^2> and trap stiffness
    r2 = x_m**2 + y_m**2
    rvar = np.sum(r2) / (np.size(r2)) # - 1)
    delk = degfree * kb * np.sqrt( (delT/rvar)**2 + (T*delrvar_m/(rvar**2))**2 )
    ktrap = degfree * kb * T / rvar

    # create a frame vector
    n = np.size(x)
    frames = np.linspace(1,n,n)

    # create a 3d plot of the x and y positions vs frame
    mpl.rcParams['legend.fontsize'] = 8
    mpl.rcParams['figure.subplot.left'] = 0.07
    mpl.rcParams['figure.subplot.right'] = .95
    mpl.rcParams['figure.subplot.hspace'] = .2
    mpl.rcParams['ytick.labelsize'] = 8
    mpl.rcParams['xtick.labelsize'] = 8
    mpl.rcParams['font.size'] = 10
    fig1 = positions_plot(x_m, y_m, frames)

    # plot the x, y and radial displacements vs frame as well as histograms
    # of the x, y and radial distributions in the same figure
    fig2 = plt.figure(2, figsize=(12,8))

    xvar = np.var(x_m)
    yvar = np.var(y_m)
    rvar = rvar
    xvarp = xvar * np.ones((n,1)) # a vector with n xvar's
    yvarp = yvar * np.ones((n,1)) # a vector with n yvar's
    rvarp = rvar * np.ones((n,1)) # a vector with n rvar's

    plt.subplot(2,3,1)
    disp_v_frame(x_m, frames, xvarp, 'x')
    plt.subplot(2,3,2)
    disp_v_frame(y_m, frames, yvarp, 'y')
    plt.subplot(2,3,3)
    disp_v_frame(r2, frames, rvarp, 'r')

    bins = n // 10 # the number of bins for the histograms; may be changed

    plt.subplot(2,3,4)
    disp_distr(x_m, bins, 'x')
    plt.subplot(2,3,5)
    disp_distr(y_m, bins, 'y')
    plt.subplot(2,3,6)
    disp_distr(r2, bins, 'r')
    plt.tight_layout()

    figs = [fig1, fig2]

    return ktrap, delk, figs
