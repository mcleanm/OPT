# Optical Tweezers Analysis Software
Data analysis software for the [Advanced Physics Laboratory Optical Tweezers](https://www.physics.utoronto.ca/~phy326/opt/) experiment. The main script, `OpticalTrapVideoAnalysis2.py` can be run via the command line (`python OpticalTrapVideoAnalysis2.py`) or via the Spyder IDE.

This will open a GUI in which all analysis information can be input (TIFF file, spot radius, maximum displacement, start/stop frames, etc.). By following the instructions on the popup windows, the program will fit a trajectory to the bead via computing its centroid at each frame. The outputs are written to the indicated directory, and include two figures displaying the position of the bead (`fig1.png` and `fig2.png`), the raw position data in pixels (`position_data.txt`), and a summary of all analysis parameters used/computed (`analysis_info.txt`).

Dependencies:
- NumPy
- tkinter
- PIL
- matplotlib

Original Authors:
- Christopher Dydula
- Donald Woodbry

Additional Contributors:
- [Michael McLean](https://github.com/mcleanm)

