# File Name: check_directory.py
# Created By: ZW
# Created On: 2022-04-20
# Purpose: Script to quickly check directory outputs, returning a small file
#   containing a return code (0) if successful, otherwise throwing an error


# Module Imports
# -----------------------------------------------------------------------------
import argparse
from gardnersnake.core import Configuration
from gardnersnake.core.exceptions import UserError
from pathlib import Path
from sys import stderr
from typing import Union


# Global Constants
# -----------------------------------------------------------------------------
## Define a set of keywords for use with the function <def get_verified_path>
## These types specify whether the path passed represents a file, directory,
## or unknown type.
ACCEPTED_DTYPES = ["dir", "directory", "folder"]
ACCEPTED_FTYPES = ["file", "fp"]
ACCEPTED_TYPES = ["unknown", *ACCEPTED_DTYPES, *ACCEPTED_FTYPES]


# Type Definitions
# -----------------------------------------------------------------------------
PATH_T = Union[str, Path]  # type alias for filepaths (either string or Path)


# Error and Exception Definitions
# -----------------------------------------------------------------------------

## Define an Error for the function <def get_verified_path> which is thrown
## when path cannot be verified --normally arising from instances when existence
## is required but the object cannot be found
class PathVerificationError(UserError):
    def __init__ (self, message, *args, **kw):
        super(UserError, self).__init__(message, *args, **kw)
        self.message = message

    def __str__(self) -> str:
        return self.message



# Function Definitions
# -----------------------------------------------------------------------------

## Defines <def get_verified_path> which checks to see if a given path
## is well-formed and [optionally, using strict=True] exists. Throws an
## error if the path cannot be resolved and/or does not exist under strict=True
def get_verified_path(path, pathtype, strict=False):
    pobj = Path(path).expanduser().resolve()  # generate a pathlib Path object
    exists = False  # flag for whether or not the file or directory exists
    try:  # handle the existence check depending on the type of path
        if pathtype.lower() in ACCEPTED_DTYPES: exists = pobj.is_dir()
        elif pathtype.lower() in ACCEPTED_FTYPES: exists = pobj.is_file()
        elif pathtype.lower() in ACCEPTED_TYPES: exists = pobj.exists()
        else:
            errmsg = f"""
            Error. Unknown path type for {path}.
            Must be one of: {ACCEPTED_TYPES}
            Passed path type (pathtype=): {pathtype}
            """
            raise PathVerificationError(errmsg)
    except AttributeError as ae:
        errmsg = "Error. Please pass a string to arugment path"
        raise PathVerificationError(errmsg) from ae
    # resolve the path object
    if exists and strict: return pobj
    elif not strict: return pobj
    else:
        errmsg = f"""
        Error. Unable to validate that {path} of type: {pathtype} exists.
        Exiting...
        """
        raise PathVerificationError(errmsg)

## Defines <def main> which executes the main body of the script. This function
## is the access point for the alias created by setup.py when the package is
## installed by the user
def main():
    # setup CLI for the program
    descr = """
    Validates dynamic directory contents against expectations.
    If each of the required files is present in the directory,
    the program writes '0' to the output file. otherwise, it returns
    an Error
    """
    parser = argparse.ArgumentParser(description=descr, prog="check_directory")
    parser.add_argument("contents", type=str, nargs='+',metavar='FILES',
                        help="set of filepaths to check against dir contents")
    parser.add_argument("directory", type=str, metavar="DIR",
                        help="filepath of directory to verify")
    parser.add_argument("-o","--output", type=str, metavar="OUT",
                        help="name of return code output file")

    args = parser.parse_args()
    # check the directory contents
    dir_object = get_verified_path(args.directory, "dir", strict=True)
    dir_paths = [f for f in dir_object.glob("**/*") if f.is_file()]
    paths_to_check = [dir_object / f for f in args.contents]

    for filecheck in paths_to_check:
        if filecheck not in dir_paths:
            errmsg = f"""
            Error. Could not verify contents of {args.directory}
            Could not find {filecheck} in {args.directory}
            """
            raise PathVerificationError(errmsg)

    # write out the successful returncode
    if args.output:
        with open(args.output, 'w') as outfile:
            outfile.write('0')
    else:
        errmsg = """
        Error. Please pass a file for output
        use the --output <file.out> or -o <file.out> flags
        to pass a return code file.
        """
        raise ArgumentError(errmsg)

