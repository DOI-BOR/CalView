# CalView
CalView is a visualization tool for DSS files. Currently, Calsim, temperature (HEC5Q), and salinity (DSM2) versions have been developed.

# To Set Up an Environment

To create an environment to launch a run or compile the executable, run the line:

`conda env create -f environment.yml`

To activate the environment, run the line:

`conda activate calview`

# To Launch a Run

In the environment, run the line: 

`python calview_all.py`

# To Compile the Executable 

In the environment, run the line:

`pyinstaller build_calview_all.spec`

The compiled executable will be created in a folder called *dist*. Double-click on the executable to launch it.

# Files

* The *environment.yml* file is to create an environment to run and compile the apps in
* *calview_all.py* is the main file
* *build_calview_all.spec* is for compiling the executable
* The *src* folder has the other python files with the code for the apps
  * *cs3_plotlib.py* has the plotting functions
  * *csdss_readlib_fullfile.py* has the functions that support reading in DSS files
  * *hook-panel.py* and *hook-gdal-runtime.py* is for the compilation of the executable
  * *widgets.py* has functions that support the widgets of the apps
* The *inputs* folder has the inputs required for the apps
  * Each module has a *TR_fields.txt* file that has the default fields to be read in
  * The USBR logo is also in this folder