# CalView
CalView is a visualization tool for DSS files. Currently, Calsim, temperature (HEC5Q), and salinity (DSM2) versions have been developed.

# To Set Up an Environment

To create an environment to launch a run or compile the executable, run the line:

`conda env create -f environment.yml`

To activate the environment, run the line:

`conda activate calview`

# To Launch a Run

In the environment, run the line: 

`python calview_calsim.py`

or

`python calview_temperature.py`

or

`python calview_salinity.py`

# To Compile the Executable 

In the environment, run the line:

`pyinstaller build_calview_calsim.spec`

or

`pyinstaller build_calview_temperature.spec`

or 

`pyinstaller build_calview_salinity.spec`

The compiled executable will be created in a folder called *dist*. Double-click on the executable to launch it.

# Files

* The *environment.yml* file is to create an environment to run and compile the apps in
* *calview_calsim.py*, *calview_temperature.py*, and *calview_salinity.py* are the main files for each version
* The three *.spec* files are for compiling the executables
* The *src* folder has the other python files with the code for the apps
  * *cs3_plotlib.py* has the plotting functions
  * *csdss_readlib_fullfile.py* has the functions that support reading in DSS files
  * *hook-panel.py* is for the compilation of the executable
  * *widgets.py* has functions that support the widgets of the apps
* The *inputs* folder has the inputs required for the apps
  * Each version has a *TR_fields.txt* file that has the default fields to be read in
  * The USBR logo is also in this folder