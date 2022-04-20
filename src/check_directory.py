# File Name: check_directory.py
# Created By: ZW
# Created On: 2022-04-20
# Purpose: Script to quickly check directory outputs, returning a small file
#   containing a return code (0) if successful, otherwise throwing an error

# module imports
import argparse
from gardnersnake.pathutils import get_verified_path
from gardnersnake.exceptions import UserError

def main():
    # setup CLI for the program
    descr = " validates dynamic directory contents against expectations"
    parser = argparse.ArgumentParser(description=descr, prog="check_directory")
    parser.add_argument("contents", type=str, nargs='+',metavar='FILES',
                        help="set of filepaths to check against dir contents")
    parser.add_argument("directory", type=str, metavar="DIR",
                        help="filepath of directory to verify")
    parser.add_argument("--strict", action="store_true",
                        help="directory should contain only the passed files")
    parser.set_defaults(strict=False)
    parser.add_argument("-o","--output", type=str, metavar="OUT",
                        help="name of return code output file")

    args = parser.parse_args()
    # check the directory contents
    dir_object = get_verified_path(args.directory, "dir", strict=True)
    dir_paths = [f for f in dir_object.glob("**/*") if f.is_file()]
    paths_to_check = [dir_object / f for f in args.contents]

    for filecheck in paths_to_check:
        if filecheck not in dir_paths:
            msg1 = f"\nError. Could not verify contents of {args.directory}"
            msg2 = f"Could not find {filecheck} in {args.directory}"
            raise UserError("\n".join([msg1,msg2]))

    # handle strict directory verification (extra files fails the check)
    if ((args.strict) and (len(paths_to_check) != len(dir_paths))):
        extra_files = dir_paths.copy()
        for f in paths_to_check: extra_files.remove(f)
        msg1 = f"\nError. Could not verify contents of {args.directory}"
        msg2 = f"Found extra files: {extra_files}, with --strict={args.strict}"
        raise UserError("\n".join([msg1,msg2]))

    else: # write out the successful returncode
        if args.output:
            with open(args.output, 'w') as outfile:
                outfile.write('0')
        else:
            msg = "Error. Please pass a file for output"
            raise UserError(msg)







