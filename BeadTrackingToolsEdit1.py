'''
BeadTrackingToolsEdit1.py

This file defines a series of functions to be used in the main spot tracking
file PILBeadTracking2.py

Author: Donald Woodbry, University of Toronto

    Last Modification: 20 June 2011 by Christopher Dydula
'''

from tkinter import *
from PIL import Image, ImageSequence, ImageDraw, ImageTk
from numpy import average
import pylab
import os, shutil

class Image_clicker(object):
    def __init__(self, image, parent = None):
        self.root = Toplevel(master=parent)

        size = image.size
        
        label = Label(self.root, text="Select Spot Location:", anchor = 'n')
        label.pack()

        frame = Frame(self.root)
        frame.pack()
        
        canvas = Canvas(frame, width=size[0], height=size[1])
        canvas.pack()

        tkimg = ImageTk.PhotoImage(image)

        display_image = canvas.create_image(0,0,image=tkimg,anchor="nw")

        canvas.bind("<Button-1>", self.return_pos)

        self.root.mainloop()

    def return_pos(self, event):
        self.click = (event.x, event.y)
        self.root.quit()

class Display_Results(object):
    def __init__(self, im_dir, plot_title, start_frame, end_frame, \
                 save_frames = False, parent = None):

        self.im_dir = im_dir
        self.root = Toplevel(master=parent)

        track_image = Image.open(os.path.join(self.im_dir, 'Frame%d.jpg' % (start_frame+1)))
        self.tk_track = ImageTk.PhotoImage(track_image)
        xsize, ysize = track_image.size
        
        frame = Frame(self.root)
        frame.pack()

        self.canvas = Canvas(frame, width = xsize, height = ysize)
        self.canvas.pack()
        
        display_image = self.canvas.create_image(0,0,image=self.tk_track,anchor="nw")
        
        min_slider = Scale(frame, command=self.update_image, label="Frame Number",\
                           length=xsize, orient=HORIZONTAL,\
                           from_=start_frame, to=end_frame)
        min_slider.pack()

        if not save_frames:
            self.root.protocol("WM_DELETE_WINDOW", self.del_dir)
        else:
            self.root.protocol("WM_DELETE_WINDOW", self.end_disp)
        self.root.mainloop()

    def update_image(self, frame_num):
        track_image = Image.open(os.path.join(self.im_dir, 'Frame%d.jpg' % (int(frame_num)+1)))
        self.tk_track.paste(track_image)
        
    def del_dir(self):
        shutil.rmtree(self.im_dir)
        self.root.quit()

    def end_disp(self):
        self.root.quit()

def save_frame(im, directory, track, start_frame, end_frame, dot_size):
    '''creates a new folder under the directory and then
        saves and numbers the frames from im within it,
        marking the point where the object was tracked'''

    # checks to see if the directory already exists and if it doesn't \
    # a new one is created

    directory1 = directory

    i = 1
    
    while os.path.exists(directory1):
        directory1 = os.path.join(directory, '-' + str(i))
        i += 1

    os.makedirs(directory1)

    # iterating over all frames in the sequence and drawing a dot
    # where the program has determined the particle is

    j = 0    
    for frame in ImageSequence.Iterator(im):
        frame = frame.convert('RGB')
        if start_frame -1 < j < end_frame+1:
            frame_num = j-start_frame

            d = dot_size/2
            x, y = track[frame_num]
            draw = ImageDraw.Draw(frame)
            draw.rectangle((x-d, y-d, x+d, y+d), fill = 'Blue')
            #saving the image in the directory under the name 'Framej.jpg'                  
            frame.save(os.path.join(directory1, 'Frame%d.jpg' % (j+1)))

        j += 1

    return directory1

def new_zip(points):
    '''Returns a list consisting of a list of x coordinates and a
        list of y coordinates when given a list of x,y tuples'''
    x = []
    y = []
    
    for point in points:
        x.append(point[0])
        y.append(point[1])

    return [x,y]

def cluster_center(points):
    '''returns the vector average the (x,y) tuples in the list points.'''
    
    x, y = new_zip(points)
    
    xavg = average(x)
    yavg = average(y)

    return [xavg, yavg]

def plot_xy(spot_track, title, savefig = False):
    '''launches a pylab plot of the list of x, y tuples in spot_track
        and if savefig == True, it saves a copy of the file under title'''


    #converting the list of (x, y) tuples representing the centroid of the data
    #in each frame into an array of the x coordinates and a list of the y coordinates
    
    x_track = pylab.array(new_zip(spot_track)[0])
    y_track = pylab.array(new_zip(spot_track)[1])

    #plotting the data
    
    pylab.plot(x_track, -y_track)
    pylab.xlabel('x Position (Pixels)')
    pylab.ylabel('y Position (Pixels)')
    pylab.title(title)

    if savefig:
        pylab.savefig(title)
        print ('Plot Saved.')

    pylab.show()
