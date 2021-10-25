'''
PILBeadTracking2.py

This file contains a program that takes an animated image sequence and
tracks a spot of user defined colour and size

Author: Donald Woodbry, University of Toronto

   Last Modification: 20 June 2011 by Christopher Dydula
   This program is no longer useable on its own, only as a library for
   OpticalTrapVideoAnalysis2.py
 
'''

from BeadTrackingToolsEdit1 import *
from PIL import Image, ImageSequence, ImageDraw
from numpy import average
import pylab
import os
import tkinter as tk

def select_points(imag, threshold, file_type, box, colour = None):
    '''returns a list of (x,y) tuples containing the points
        in the given image (imag) contained in the box (box) where the
        colour in the user selected colour channel exceeds the average
        value of the other two colour channels by the threshold value.
        If no points are found, an empty list is returned.'''

    #iterating over all of the pixels in the box to find the coloured points
    points = []
    
    for x in range(max(box[0], 0), min(box[2], imag.size[0])):
        for y in range(max(box[1], 0), min(box[3], imag.size[1])):

            # adding all points to the list points whose, user selected,
            # colour chanel value is greater than the average value
            # of the other two colour channels by the threshold
            if file_type == '8-bit':
                d = imag.getpixel((x,y))
            elif file_type == 'RGB':
                r, g, b = imag.getpixel((x,y))
                if colour == 'r':
                    d = r - (g + b)/2
                elif colour == 'g':
                    d = g - (r + b)/2
                elif colour == 'b':
                    d = b - (g + r)/2
                else:
                    return []
            
            if d > threshold:
                points.append((x,y))
    
    return points

def track_spot(im, first_spot, max_pix, spot_size, spot_brightness, \
               start_frame, stop_frame, file_type):
    '''returns a list of (x,y) tuples containing the centroids of the spots
        located in each frame.

        max_pix defines the furthest distance the spot may travel between frames
        and colour defines the colour of the particle to be tracked
    '''

    #iterating over the fames in the image sequence to find the
    #coloured pixels in each frame and their centroid

    spot_track = []
    
    i = 0 # frame counter
    j = 2 # counter for sequential frames with no spots found (starting at two)

    #default location of the spot
    centroid = first_spot

    for frame in ImageSequence.Iterator(im):
        
        d_box = max_pix + spot_size # defines the size of the box in which
                                    # the program will search for the spot

        #initializing the box to search
            
        box = [int(centroid[0]) - d_box, int(centroid[1]) - d_box, \
               int(centroid[0]) + d_box, int(centroid[1]) + d_box]

        # this if statement limits the analysis to only
        # the frames [start_frame, stop_frame) 
        if start_frame -1< i < stop_frame+1:
            #collecting the coloured points contained inside the given
            #box inside a given frame and defining their centroid
            
            points = select_points(frame, spot_brightness, file_type, box)
            if points == []:        #if no points are found, the centroid is
                d_box = d_box*j     #defined as in the previous frame and the
                                    #box is expanded by a factor of j
                print ('Cannot find spot in frame %d' % i)
            else:
                centroid = cluster_center(points)
                j = 2 #resents the counter
            spot_track.append(centroid)

        i += 1
        
    return spot_track

if "__main__" == __name__:

    #__________setting parameters__________#

    #defining the properties of the spot and its motion

    spot_size = 7 #radius of spot in pixels
    max_displacement = 5 #the furthest distance the pixel can travel between frames
    min_net_brightness = 150 #the minimum value a pixel may have after the
                            #average value of the other colour channels is subtracted
                            #or, for greyscale, the minimum brightness, (0-255)

    #defining the data to be analysed

    Tiff_file_name = '650nm_1;50000_100ma_B_b_18.tif'
    file_type = '8-bit'
    start_frame = 0
    stop_frame = 101

    #defining the plot and saved image parameters
    
    plot_title = Tiff_file_name.split('.')[0]+ \
                 ', frames %d-%d' % (start_frame, stop_frame)
    savefig = False

    save_frames = False
    display_frames = True
    directory = 'D:\SURF OPT AFM\Tracking\\' + plot_title
    dot_size = 2
    #_________Analysing the data_________#
    
    im = Image.open(Tiff_file_name)

    # finding the initial location of the spot by creating an Image_clicker
    # object

    first_image = ImageSequence.Iterator(im)[start_frame]
    first_spot = Image_clicker(first_image).click

    print ('Tracking Spot...')
    
    spot_track = track_spot(im, first_spot, max_displacement, spot_size, \
                            min_net_brightness,start_frame, stop_frame, \
                            file_type) 
    print ('Tracking Complete.')


    
    #________plotting and saving the data_________#

    if display_frames:
        im = Image.open(Tiff_file_name)
        print ('Saving Frames...')
        directory1 = save_frame(im, directory, spot_track, \
                                start_frame, stop_frame, dot_size)
        print ('Saving frames complete.')
        Display_Results(directory1, plot_title, start_frame, \
                    stop_frame, save_frames)

    #print 'plotting track...'

    #plot_xy(spot_track, plot_title, savefig)
