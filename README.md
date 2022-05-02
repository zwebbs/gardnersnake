# gardnersnake
_Utilities for writing concise snakemake workflows_

[python_min_version] : 3.7.0

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Class Objects](#class_objects)  
4. [Command Line Tools](#commandline_tools)


## <a name="introduction"></a> 1. Introduction
[Snakemake](https://snakemake.readthedocs.io/en/stable/) is an incredibly powerful workflow manager that enables computational biologists to produce clear, reproducible, and modular analysis pipelines using a familiar Python-based grammar. 
Unfortunately, the bioinformatics tools that we'd like to utilize inside of our Snakemake workflows are often a bit less well-behaved. 
Gardnersnake is a small package built on the python standard library (Python 3.6) that aims to make handling this wide variety of tools easier and more compact, especially when working on cluster-based systems. 

## <a name="installation"></a> 2. Installation

Gardnersnake can be installed most conveniently via pip and the [Python Package Index](https://pypi.org/project/gardnersnake/) (PyPi). Please note that gardnersnake requires Python version [python_min_version] or later.

```bash
pip install gardnersnake
```

This repo can also be cloned, built and installed from source using its `setup.py` file.

```bash
git clone https://github.com/zwebbs/gardnersnake.git
cd gardnersnake
python -m build
pip install dist/gardnersnake-*-py3*.whl
```

## <a name="class_objects"></a> 3. Class Objects
### gardnersnake.ConfigurationHelper()
The foundational object defined in gardnersnake is the __ConfigurationHelper__ Class. At instantiation `ConfigurationHelper` takes a single argument, `cfg_dict`, which should be the `config` snakemake variable capturing the passed workflow configuration file. 




## <a name="commandline_tools"> </a> Command Line Tools
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


