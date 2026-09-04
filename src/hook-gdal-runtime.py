import os
import sys
#this file is needed to correctly compile the executable
if getattr(sys, 'frozen', False):
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    os.environ['GDAL_DATA'] = os.path.join(base_dir, 'gdal-data')
    os.environ['PROJ_DATA'] = os.path.join(base_dir, 'proj-data')
    os.environ['PROJ_LIB'] = os.path.join(base_dir, 'proj-data')

    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(base_dir)

    os.environ['PATH'] = base_dir + os.pathsep + os.environ.get('PATH', '')

    try:
        import pyogrio._io

    except Exception as e:
        print(f"[hook-gdal-runtime] pyogrio._io import FAILED: {type(e).__name__}: {e}")