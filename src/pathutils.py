# File Name: pathutils.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: methods for handling paths in snakemake configs

# module imports
from pathlib import Path
from .exceptions import UserError, eprint

# globals
ACCEPTED_DTYPES = ["dir", "directory", "folder"]
ACCEPTED_FTYPES = ["file", "fp"]
ACCEPTED_TYPES = ["unknown", *ACCEPTED_DTYPES, *ACCEPTED_FTYPES]

# define a function to return a verified, expanded path
def get_verified_path(path, pathtype, strict=False):
    pobj = Path(path).expanduser().resolve() # generate a pathlib Path object
    exists = False # flag for whether or not the file or directory exists
    method_err = "Error in pathutils.get_verified_path()"

    # handle the existence check depending on the type of path
    if pathtype.lower() in ACCEPTED_DTYPES: exists = pobj.is_dir()
    elif pathtype.lower() in ACCEPTED_FTYPES: exists = pobj.is_file()
    elif pathtype.lower() in ACCEPTED_TYPES: exists = pobj.exists()
    else:
        eprint(f"Unknown path type for {path}")
        eprint(f"Must be one of: {ACCEPTED_TYPES}")
        eprint(f"Passed path type (pathtype=): {pathtype}")
        raise UserError(method_err)

    # resolve the path object
    if (exists and strict):
        return pobj
    elif (not strict): # always return the path object if not strict
        return pobj
    else:
        eprint(f"exists: {exists}, strict: {strict}")
        eprint(f"Unable to validate that {path} of type: {pathtype} exists.")
        raise FileNotFoundError(method_err)
