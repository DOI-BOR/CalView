# To Set Up an Environment

To create an environment to launch a run or compile the executable run the line:

`conda env create -f environment.yml`

Then, to activate the environment run the line:

`conda activate calview`

# To Launch a Run

Run the line: 

`python cs3_viz_app_main.py`

# To Compile the Executable 

Run the line:

`pyinstaller cs_visualizer.spec`

The compiles executable will be created in a folder called *dist*. Double-click on the executable to launch it.