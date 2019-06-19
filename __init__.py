import sys
import os

# add this directory to sys.path, before importing stuff
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir)

import Map, Tileset

# clean up after import
sys.path.remove(this_dir)
del this_dir
del os
del sys

VERSION = "1.0.1"
