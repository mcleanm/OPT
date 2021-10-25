'''
OpticalTrapVideoAnalysis2.py

Combines the functions of PILBeadTracking2.py and TrapAnalysis.py in a single
file to allow for direct analysis of a video of a bead. Implements a GUI.

Author: Christopher Dydula, University of Toronto   -   18 May 2011
   with use of content from PILBeadTracking.py (Donald Woodbry)

   Last Modification:  20 June 2011 by Christopher Dydula
'''

import PILBeadTracking2 as pbt
import TrapAnalysis as ta
import numpy as np
import tkinter as tk
import tkinter.filedialog as tfd

def get_file(root):
    '''Ask for a filename and assign it to the global variable Tiff_file_name.
    '''

    Tiff_file_name.set(tfd.askopenfilename(
        parent=root,
        filetypes=[('TIFF', '*.tif;*.tiff')],
        title='Open a video to analyze...'))

def get_dir(root):
    '''Ask for a directory and assign it to the global variable directory.
    '''

    directory.set(tfd.askdirectory(
        parent=root,
        title='Select directory to save frames to...'))

def analyze():
    '''Collect the x and y positions of the bead to be tracked in each frame
       and calculate the trap stiffness from this data. Various data plots are
       displayed. Option to display and/or save tracked frames.
    '''

    #____Collecting the data___#

    im = pbt.Image.open(Tiff_file_name.get())

    # finding the initial location of the spot by creating an Image_clicker
    # object

    dialog_text.set(">>> Select spot location (may take a while if saving or"
                    " displaying frames)")

    first_image = pbt.ImageSequence.Iterator(im)[start_frame.get()]
    clicker = pbt.Image_clicker(first_image, window)
    first_spot = clicker.click
    clicker.root.destroy()

    # a grid is no longer used to find initial spot location
    '''
    box = pbt.find_starting_box(first_image, grid_size.get(),
                                grid_thickness.get(), window, dialog_text,
                                input_text, waiter)
    '''

    input_text.set("")
    dialog_text.set(">>> Tracking...")

    # obtain bead position data
    spot_track = pbt.track_spot(im, first_spot, max_displacement.get(),
                            spot_size.get(), min_net_brightness.get(),
                            start_frame.get(), stop_frame.get(),
                            file_type.get()) 
    dialog_text.set(">>> Tracking complete.")

    #___Displaying and saving the data___#

    if display_frames.get() or save_frames.get():
        im = pbt.Image.open(Tiff_file_name.get())
        dialog_text.set(">>> Saving frames...")

        # 2 is the size in pixels of the dot showing tracking results.
        # Originally a variable was passed.
        directory1 = pbt.save_frame(im, directory.get(), spot_track,
                                    start_frame.get(), stop_frame.get(), 2)
        dialog_text.set(">>> Saving frames complete.")
        dialog_text.set(">>> Check to see if the bead was tracked correctly."
                        " Close the popup to continue (may take a while if"
                        " not saving frames)")
        display = pbt.Display_Results(directory1, plot_title, start_frame.get(),
                        stop_frame.get(), save_frames.get(), window)
        display.root.destroy()

    #___Analyzing the data___#

    x = np.zeros((stop_frame.get() - start_frame.get()))
    y = np.zeros((stop_frame.get() - start_frame.get()))
    for i in range(stop_frame.get() - start_frame.get()):
        x[i] = spot_track[i][0]
        y[i] = spot_track[i][1]

    # x is an array_like type holding the x positions of each frame and y
    # is holding the y positions of each frame. The remaining code may be
    # edited to analyze this data however one wishes.

    # r is the trap stiffness, delta is the error in the result
    (r, x1, y1, delta) = ta.analyze(x, y, temp.get())

    #dialog_text.set("The trap stiffness in the x direction is %9.4e N/m" % x1)
    #dialog_text.set(dialog_text.get()
    #           + "\nThe trap stiffness in the y direction is %9.4e N/m" % y1)
    print("The trap stiffness is "
                    "%9.4e +/- %9.4e N/m" % (r, delta))
    
def update(): # unused
    waiter.set(1)

if __name__ == "__main__":

    # Create the application
    window = tk.Tk()
    window.wm_title("Optical Trap Video Analysis")
    outer_frame = tk.Frame(window, borderwidth=4, relief=tk.GROOVE)
    outer_frame.grid(row=0, column=0)

    # Video information
    Tiff_file_name = tk.StringVar()
    file_type = tk.StringVar()
    file_type.set("8-bit")
    start_frame = tk.IntVar()
    start_frame.set(0)
    stop_frame = tk.IntVar()
    stop_frame.set(100)
    
    video_frame = tk.Frame(outer_frame)
    video_frame.grid(row=0, column=0, stick=tk.W, pady=5)

    label = tk.Label(video_frame, text="Enter information for video to"
                                        " be analyzed:",
                     font=("Helvetica", 8, "bold"))
    label.grid(row=0, column=0, columnspan=2, sticky=tk.W)

    label = tk.Label(video_frame, text="Open a TIFF file:")
    label.grid(row=1, column=0)

    entry = tk.Entry(video_frame, textvariable=Tiff_file_name, width=40)
    entry.grid(row=1, column=1, padx=1)

    button = tk.Button(video_frame, text="Browse", \
                       command=lambda: get_file(window))
    button.grid(row=1, column=2, padx=5)

    # Excessive spaces for text parameters added for visual formatting reasons
    label = tk.Label(video_frame, text="            File Type:")
    label.grid(row=1, column=3)

    optmenu = tk.OptionMenu(video_frame, file_type, "8-bit", "RGB")
    optmenu.grid(row=1, column=4)

    label = tk.Label(video_frame, text="            Start frame:")
    label.grid(row=1, column=5)

    entry = tk.Entry(video_frame, textvariable=start_frame, width=4)
    entry.grid(row=1, column=6, padx=1)

    label = tk.Label(video_frame, text="            Stop frame:")
    label.grid(row=1, column=7)

    entry = tk.Entry(video_frame, textvariable=stop_frame, width=4)
    entry.grid(row=1, column=8, padx=1)

    # Grid and spot parameters

    # a grid is no longer used to find initial spot location
    '''
    grid_size = tk.IntVar()
    grid_size.set(4)
    grid_thickness = tk.IntVar()
    grid_thickness.set(1)
    '''

    spot_size = tk.IntVar() # radius of spot in pixels
    spot_size.set(7)
    max_displacement = tk.IntVar() # the furthest distance the pixel can travel
                                   #  between frames
    max_displacement.set(5)
    min_net_brightness = tk.IntVar()
    min_net_brightness.set(150) # the minimum value a pixel may have after the
                                # average value of the other colour channels is
                                # subtracted or, for greyscale, the minimum
                                # brightness, (0-255)

    param_frame = tk.Frame(outer_frame)
    param_frame.grid(row=1, column=0, sticky=tk.W, pady=10)

    label = tk.Label(param_frame, text="Enter the parameters for the grid"
                                        " used to initialize motion tracking"
                                        " and the properties of the spot:",
                     font=("Helvetica", 8, "bold"))
    label.grid(row=0, column=0, columnspan=6, sticky=tk.W)

    # a grid is no longer used to find initial spot location
    '''
    label = tk.Label(param_frame, text="Grid size:")
    label.grid(row=1, column=0, sticky=tk.W)

    entry = tk.Entry(param_frame, textvariable=grid_size, width=4)
    entry.grid(row=1, column=1, padx=1, sticky=tk.W)

    label = tk.Label(param_frame, text="Grid thickness:")
    label.grid(row=1, column=2, sticky=tk.W)

    entry = tk.Entry(param_frame, textvariable=grid_thickness, width=4)
    entry.grid(row=1, column=3, padx=1, sticky=tk.W)
    '''

    label = tk.Label(param_frame, text="Spot size (radius in px):")
    label.grid(row=2, column=0, sticky=tk.W)

    entry = tk.Entry(param_frame, textvariable=spot_size, width=4)
    entry.grid(row=2, column=1, padx=1, sticky=tk.W)

    label = tk.Label(param_frame, text="Max displacement (px):")
    label.grid(row=2, column=2, sticky=tk.W)

    entry = tk.Entry(param_frame, textvariable=max_displacement, width=4)
    entry.grid(row=2, column=3, padx=1, sticky=tk.W)

    label = tk.Label(param_frame, text="Minimum net brightness (0-255):")
    label.grid(row=2, column=4, sticky=tk.W)

    entry = tk.Entry(param_frame, textvariable=min_net_brightness, width=4)
    entry.grid(row=2, column=5, padx=1, sticky=tk.W)

    # an explanation of Minimum net brightness. Found it to be too long and
    # out of place in the GUI so have it commented out.
    '''
    label = tk.Label(param_frame, text = "Minimum net brightness - "
                     "the minimum value a pixel may have after the average "
                     "value "
                     "of the \n other colour channels is subtracted, or, "
                     "for greyscale, the minimum brightness (0-255)")
    label.grid(row=3, column=0, columnspan=6, sticky=tk.W)
    '''

    # Saved image parameters
    plot_title = Tiff_file_name.get().split('.')[0]+ \
                 ', frames %d-%d' % (start_frame.get(), stop_frame.get())
    save_frames = tk.IntVar()
    save_frames.set(0)
    display_frames = tk.IntVar()
    display_frames.set(1)
    directory =tk.StringVar()
    directory.set("Only necessary if 'Save frames' or 'Display frames' is"
                  " selected")

    saved_frame = tk.Frame(outer_frame)
    saved_frame.grid(row=2, column=0, sticky=tk.W, pady=5)

    label = tk.Label(saved_frame, text="Enter the information for"
                     " saving or displaying the frames of a tracked video:",
                     font=("Helvetica", 8, "bold"))
    label.grid(row=0, column=0, sticky=tk.W, columnspan=4)

    check = tk.Checkbutton(saved_frame, text='Save frames', \
                           variable=save_frames)
    check.grid(row=1, column=0, sticky=tk.W, padx=3)

    check = tk.Checkbutton(saved_frame, text='Display frames', \
                           variable=display_frames)
    check.grid(row=1, column=1, sticky=tk.W, padx=3)

    label = tk.Label(saved_frame, text="Directory to save to:")
    label.grid(row=1, column=2, padx=2, sticky=tk.W)

    entry = tk.Entry(saved_frame, textvariable=directory, width=54)
    entry.grid(row=1, column=3, padx=1, sticky=tk.W)

    button = tk.Button(saved_frame, text="Browse", \
                       command=lambda: get_dir(window))
    button.grid(row=1, column=4, padx=5, sticky=tk.W)

    # Trap analysis parameters
    temp = tk.DoubleVar()
    temp.set(293.15)
    # add additional variables for trap analysis here

    trap_frame = tk.Frame(outer_frame)
    trap_frame.grid(row=3, column=0, sticky=tk.W, pady=10)

    label = tk.Label(trap_frame, text="Enter the variables for"
                     " trap analysis:", font=("Helvetica", 8, "bold"))
    label.grid(row=0, column=0, sticky=tk.W, columnspan=2)

    label = tk.Label(trap_frame, text="Temperature (K):")
    label.grid(row=1, column=0, sticky=tk.W)

    entry = tk.Entry(trap_frame, textvariable=temp, width=6)
    entry.grid(row=1, column=1, stick=tk.W)

    # add additional widgets for entering values for variables here. Just follow
    # the above two widgets.

    # Start analysis button

    button_frame = tk.Frame(outer_frame)
    button_frame.grid(row=4, column=0, sticky=tk.W, pady=5)

    button = tk.Button(button_frame, text="Start Analyzing",
                       font=("Helvetica", 8, "bold"),
                       command=lambda: analyze())
    button.grid(row=0, column=0, sticky=tk.W)

    # Interaction
    dialog_text = tk.StringVar()
    dialog_text.set(">>> Enter all required information above and click 'Start"
                    " Analyzing'")
    input_text = tk.StringVar() # unused
    waiter = tk.IntVar() # unused

    inter_frame = tk.Frame(outer_frame)
    inter_frame.grid(row=6, column=0, sticky=tk.W, pady=15)

    label = tk.Label(inter_frame, text="Dialog:", fg="red",
                     font=("Helvetica", 10, "bold"))
    label.grid(row=0, column=0, sticky=tk.W)

    label = tk.Label(inter_frame, textvariable=dialog_text, fg="maroon")
    label.grid(row=0, column=1, sticky=tk.W, columnspan=2)

    # user text input no longer needed without grid method for finding initial
    # spot location.
    '''
    label = tk.Label(inter_frame, text="Input:", fg="green",
                     font=("Helvetica", 10, "bold"))
    label.grid(row=1, column=0, sticky=tk.W)

    entry = tk.Entry(inter_frame, textvariable=input_text, width=40)
    entry.grid(row=1, column=1, sticky=tk.W)

    button = tk.Button(inter_frame, text="Enter", command=lambda: update())
    button.grid(row=1, column=2, sticky=tk.W)
    '''

    window.mainloop()
