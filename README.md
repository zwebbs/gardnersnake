# gardnersnake
__Utilities for writing concise snakemake workflows__


## Table of Contents

1. [Class Objects] (#class_objects) 
2. [Command Line Tools] (#commandline_tools)

## Class Objects <a>name="class_objects"</a>

## Command Line Tools <a>name="commandline_tools" </a>
### check_directory

Many bioinformatics tools produce directories of various structure with large numbers of output files. Rather than require Snakemake to keep track of these outputs as global outputs, the `check_directory` command-line utility validates output directories against a known set of files, and returns a small file containing a return code (0) if the directory of interest was successfully validated. `check_directory` throws an error and does not return the return code file if it is unable to validate the contents according to the given requirements.

```bash
check_directory --help
usage: check_directory [-h] [--strict] [-o OUT] FILES [FILES ...] DIR

validates dynamic directory contents against expectations

positional arguments:
  FILES                 set of filepaths to check against dir contents
  DIR                   filepath of directory to verify

optional arguments:
  -h, --help            show this help message and exit
  --strict              directory should contain only the passed files
  -o OUT, --output OUT  name of return code output filei
```

Typical usage may look like:

```bash
check_dir -o rc.out --strict output1.txt output2.txt ~/myanalysis/outputs/
```

which should return a file called `rc.out` if the folder `~/myanalysis/outputs/` has exactly two files -- `output1.txt` and `output2.txt`


