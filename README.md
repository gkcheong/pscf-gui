# pscf-gui
Graphical user interface for PSCF (https://github.com/dmorse/pscf)
This program is a GUI wrapper written using python's Tkinter package
for PSCF, a self-consistent field theory solver.

To run the program type `python gui.py` on the terminal.
The program requires PSCF set up and Matlab for additional data processing.
The linkage to both PSCF and Matlab will need to be edited directly through the first 2 lines of the code.

The program natively runs assuming an input seed is present for the PSCF code.
<img src=https://github.com/gkcheong/pscf-gui/blob/master/Image/image1.png /> <br />
However the `Omega Wizard` allows one to generate input seed by inputting the 
fractional coordinates of the particles separated by semicolons.
<img src=https://github.com/gkcheong/pscf-gui/blob/master/Image/image2.png /> 
