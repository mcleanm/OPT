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
    ax.scatter(x, y, frames, label='Positions')
    #ax.legend(loc=9) # legend is placed at top centre, acts as title

    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('Frame')

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
        plt.title('x displacement vs frame')
        plt.legend(('x for individual frames', '$<x^2>$ = %9.4e' % varp[0]))
    elif name == 'y':
        plt.ylabel('y (m)')
        plt.title('y displacement vs frame')
        plt.legend(('y for individual frames', '$<y^2>$ = %9.4e' % varp[0]))
    elif name == 'r':
        plt.ylabel('$r^2 (m^2)$')
        plt.title('Radial displacement vs frame')
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

def analyze(x, y, temp):
    '''Given x and y pixel position data of a bead from a video, convert
       pixel units to metric. Produce 7 plots in two figure windows, a 3d
       position plot in the first and 3 position plots and 3 displacement
       distrubution histograms in the second. Calculate and return trap
       stiffness in the x, y and radial direction.

       x: array_like
          Array containing the x positions
       y: array_like
          Array containing the y positions

       x and y must be of the same length
    '''

    errxpx = np.std(x)
    errypx = np.std(y)
    x1 = x
    y1 = y

    # every 14.5 pixels in the image is one micrometre, approximately
    # (1 micrometre is 14.5 +/- 0.3 px)
    x /= (14.5 * 1e6)
    y /= (14.5 * 1e6)
    errx = ( (errxpx/(14.5*1e6))**2 + (x1*0.3 / (14.5**2 * 1e6))**2 ) ** (0.5)
    erry = ( (errypx/(14.5*1e6))**2 + (y1*0.3 / (14.5**2 * 1e6))**2 ) ** (0.5)

    # center positions about the origin
    x -= np.mean(x)
    y -= np.mean(y)

    # create vectors of the squares of the x and y positions
    x2 = x**2
    y2 = y**2

    # find the square of the radial displacement from the origin in each frame
    r2 = x2 + y2

    # find the variance of the x, y and radial displacements
    xvar = np.var(x)
    yvar = np.var(y)
    rvar = np.var(r2**(.5))

    # error analysis
    
    #errx = np.std(x)
    #erry = np.std(y)

    r = r2 ** (.5)
    delr = ((x2 * errx**2 + y2 * erry**2) / (x2 + y2)) ** (.5)

    delmeanr = (np.sum((delr / np.size(r)) ** 2)) ** (.5)

    delrvar = (np.sum(((r - np.mean(r)) * delr * 2 / (np.size(r)-1) ) ** 2)) \
              ** (0.5)        

    kb = 1.38065e-23
    delT = 5
    T = temp

    delk = ((kb * delT / rvar) ** 2 + (kb * T * delrvar / rvar**2) ** 2) ** (.5)
    '''
    r = r2**(0.5)
    sigma = np.std(r)

    delrvar = (2*sigma**4)/(np.size(r) - 1)

    kb = 1.38065e-23
    delT = 0
    T = temp

    delk = ((kb * delT / rvar) ** 2 + (kb * T * delrvar / rvar**2) ** 2) ** (.5)
    '''


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
    positions_plot(x, y, frames)

    # plot the x, y and radial displacements vs frame as well as histograms
    # of the x, y and radial distributions in the same figure
    fig2 = plt.figure(2)

    xvarp = xvar * np.ones((n,1)) # a vector with n xvar's
    yvarp = yvar * np.ones((n,1)) # a vector with n yvar's
    rvarp = rvar * np.ones((n,1)) # a vector with n rvar's

    plt.subplot(2,3,1)
    disp_v_frame(x, frames, xvarp, 'x')
    plt.subplot(2,3,2)
    disp_v_frame(y, frames, yvarp, 'y')
    plt.subplot(2,3,3)
    disp_v_frame(r2, frames, rvarp, 'r')

    bins = 15 # the number of bins for the histograms; may be changed

    plt.subplot(2,3,4)
    disp_distr(x, bins, 'x')
    plt.subplot(2,3,5)
    disp_distr(y, bins, 'y')
    plt.subplot(2,3,6)
    disp_distr(r2, bins, 'r')

    #my_show()

    # calculate the trap stiffness using equipartition theorem
    kb = 1.38065e-23 # [m^2*kg*s^-2*K^-1], boltzmann constant
    T = temp # [K], temperature in room at time of recording of video
    degfree = 2 # number of degrees of freedom

    stiffnessx = kb * T / xvar
    stiffnessy = kb * T / yvar
    stiffness = degfree * kb * T / rvar

    delk = 0 # error analysis above is incorrect; if fixed, erase this line

    return stiffness, stiffnessx, stiffnessy, delk
