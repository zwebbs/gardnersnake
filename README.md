# gardnersnake
_Utilities for writing concise snakemake workflows_





## Command line Tools
### check_directory

Many bioinformatics tools produce directories of various structure with large numbers of output files. Rather than require Snakemake to keep track of these outputs as global outputs, the `check_directory` command-line utility validates output directories against a known set of files, and returns a small file containing a return code (0) if the directory of interest was successfully validated. `check_directory` throws an error and does not return the return code file if it is unable to validate the contents according to the given requirements.

The options and requirements are specified in the usage message and can be retrieved using the `-h` or `--help` flags.

```
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

__Positional Options__ \

* `FILES` [_required_] a list of whitespace separated files to search for in the passed directory. these file names should be specified without their path extensions (i.e. a file whose full path is _/home/user/analysis/myoutputs/output1.txt_ should be passed as _output1.txt_ if the `DIR` is indicated to be _/home/user/analysis/myoutputs/_)
* `DIR` [_required_] is the full path of the directory to verify. `~/` conventions are acceptable but shell variable syntax such as `$WORKDIR` are not supported. Relative path functionality remains in active development but is not guaranteed to work as of the current version (0.1.0)

__Flagged Options__ \

* `--ouput -o` [_required_] specifies the name of the file generated (containing the return code) when the passed directory is successfully validated.
* `--strict` [_optional_] indicates that the passed directory should only contain the files listed in the `FILES` positional argument, and no other files or subdirectories. the default setting, _nonstrict_ will validate directories containing extra files so long as the required ones are present. This gives the user the ability to be more or less permissive with their checks. 
Typical usage may look like:


```bash
check_dir -o rc.out --strict output1.txt output2.txt ~/myanalysis/outputs/
```

which should return a file called _rc.out_ if the folder _~/myanalysis/outputs/_ has exactly two files --> _output1.txt_ and _output2.txt_


