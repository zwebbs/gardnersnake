# File Name: pathutils.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: methods for handling paths in snakemake configs

# module imports
from pathlib import Path
from .exceptions import UserError

# globals
# -----------------------------------------------------------------------------
ACCEPTED_DTYPES = ["dir", "directory", "folder"]
ACCEPTED_FTYPES = ["file", "fp"]
ACCEPTED_TYPES = ["unknown", *ACCEPTED_DTYPES, *ACCEPTED_FTYPES]


# functions
# ------------------------------------------------------------------------------

# define a function to return a verified, expanded path
def get_verified_path(path, pathtype, strict=False):
    pobj = Path(path).expanduser().resolve()  # generate a pathlib Path object
    exists = False  # flag for whether or not the file or directory exists

    # handle the existence check depending on the type of path
    try:
        if pathtype.lower() in ACCEPTED_DTYPES:
            exists = pobj.is_dir()
        elif pathtype.lower() in ACCEPTED_FTYPES:
            exists = pobj.is_file()
        elif pathtype.lower() in ACCEPTED_TYPES:
            exists = pobj.exists()
        else:
            msg1 = f"\nUnknown path type for {path}."
            msg2 = f"\nMust be one of: {ACCEPTED_TYPES}"
            msg3 = f"\nPassed path type (pathtype=): {pathtype}"
            raise UserError("".join([msg1, msg2, msg3]))
    except AttributeError as ae:
        msg4 = "Please pass a string type to argument pathtype"
        raise UserError(msg4) from ae
    # resolve the path object
    if exists and strict:
        return pobj
    elif not strict:
        return pobj
    else:
        msg = f"\nUnable to validate that {path} of type: {pathtype} exists."
        raise UserError(msg)

# EOF
