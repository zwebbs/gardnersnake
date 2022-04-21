# File Name: misc.py
# Created By: ZW
# Created On: 2022-04-21
# Purpose: Defines miscillaneous utility functions in gardnersnake
#   until they are rewritten into more comprehensive features

# module imports
#------------------------------------------------------------------------------
from .exceptions import UserError


# function Definitions
#------------------------------------------------------------------------------

# define read_manifest_txt(): takes a text file path pointing to a
# file manifest, reads it in and returns a list of files with
# whitespace stripped. 
# a manifest of file names ()
def read_manifest_txt(filepath):
    with open(filepath, 'r') as manifest:
        files = [line.strip() for line in manifest if len(line.strip()) != 0]
        return files

