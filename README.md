# gardnersnake
_Utilities for writing concise snakemake workflows_


## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [The Configuration Class](#class_configuration)
5. [Command Line Tools](#commandline_tools)


## <a name="introduction"></a> 1. Introduction
[Snakemake](https://snakemake.readthedocs.io/en/stable/) is an incredibly powerful workflow manager that enables computational biologists to produce clear, reproducible, and modular analysis pipelines using a familiar Python-based grammar. 
Unfortunately, the bioinformatics tools that we'd like to utilize inside of our Snakemake workflows are often a bit less well-behaved. 
Gardnersnake is a small package built on the python standard library that aims to make handling this wide variety of tools easier and more compact, especially when working on cluster-based systems. 


## <a name="requirements"></a> 2. Requirements

The gardnersnake package requires Python >= 3.7.0. Additionally, gardnersnake depends on [pyyaml 6.0](https://pypi.org/project/PyYAML/#description)


## <a name="installation"></a> 3. Installation

Gardnersnake can be installed most conveniently via pip and the [Python Package Index](https://pypi.org/project/gardnersnake/) (PyPi). The most recent version is `gardnersnake==0.4.1`

```bash
pip install gardnersnake
```

This repo can also be cloned and built from source using the [build](https://pypi.org/project/build/) package.

## <a name="class_configuration"></a> 4. The Configuration Class
### Basic Usage of Configuration

The basis for much of gardnersnake is the `Configuration` class object implemented as part of `gardnersnake.core`. To initialize the object, we simply pass as its only argument, the name of a yaml configuration file for the snakemake workflow. This can be a string or a `pathlib.Path object`.
```python
from gardnersnake.core import Configuration  # import the Configuration class
from pathlib import Path  # provides Path objects from the python standard library

config_filepath = Path("~/path/to/my/config.yaml").resolve()  # build a pathlib.Path object and resolve the absolute path
cfg = Configuration(filepath=config_filepath)  # instantiate the Configuration object
cfg.load()  # load the configuration data 
```

### The YAML configuration file
To interface cleanly with `gardnersnake`, We have implemented a configuration parsing system in `Configuration.load()` which require YAML files of a certain format. As currently implemented, `gardnersnake` expects to recieve a YAML file comprising one or more documents separated by `---`. Documents may be in any order, but should be of one of two types: a __RULE_CONFIG__ or a __GLOBAL_CONFIG__, specified at the top level by `DOC_TYPE:` field (see below). Configuration expects at most one __GLOBAL_CONFIG__ document, and will only remember the last of document of this type defined in the yaml file. There may be as many __RULE_CONFIG__ documents as desired (typically one per rule in the snakemake file, although not enforced). Each document of type __RULE_CONFIG__ must have a unique field `rule_name:`. Repeats will cause the Configuration to overwrite previously read documents from earlier in the file.

Below is an example of a very basic configuration file with both a __GLOBAL_CONFIG__ document, and two __RULE_CONFIG__ documents.
```yaml
---
# File Name: basic-config.yaml
# Created On: 2022-07-21

DOC_TYPE: "GLOBAL_CONFIG"
analysis_name: "my-snakemake-workflow"
workding_dir: "/my/working/directory"
files: {
  some_reference_file: "ref.txt",
  some_metadata: "meta.txt"
}
workflow_log: "my-snakemake-workflow.log"
---
DOC_TYPE: "RULE_CONFIG"
rule_name: "RuleA"
parameters: {
  par1: 100,
  par2: "--verbose"
}
resources: {
  walltime: "2:00:00",
  nodes: 1,
  ...
}

---
DOC_TYPE: "RULE_CONFIG"
rule_name: "RuleB"
parameters: {}
resources: {
  walltime: "0:30:00",
  nodes: 1,
  ...
}

```

For each document type, there are a number of required fields. These are outlined in the table below.

Field | Required in GLOBAL_CONFIG | Required in RULE_CONFIG | Short Description
--- | --- | --- | ---
DOC_TYPE | Yes (DOC_TYPE: "GLOBAL_CONFIG" ) | Yes (DOC_TYPE: "RULE_CONFIG" ) | Specifies the type of document to be read into Configuration
analysis_name | Yes (String, empty = "" ) | No | High level workflow name for logs/ reports/ etc/ reproducibility and clarity/.
working_directory | Yes (String, empty = "" ) | No | Specifies the working directory for the snakemake workflow. to be used with `workdir:` in a Snakefile.
files | Yes (Dict, empty = {} ) | No | A dictionary of files and their metadata to be used in the analysis. 
rule_name | No | Yes (String, empty="", must be unique ) | A unique identifier for each rule configuration document. Should generally correspond to a rule in the Snakefile file.
parameters | No | Yes (Dict, empty = {} ) | A dictionary to contain the non-file arguments to a given Snakefile rule.
resources | No | Yes (Dict, empty = {} ) | A dictionary to contain the resource requirements for a given Snakefile rule.

### Interfacing Configuration with Snakefiles

If we take the above configuration yaml file as an example, we can illustrate its integration with a given snakemake Snakefile. One of the main features of the `Configuration` class beyond abstraction and portability is the implementation of dot-style attribute access so that we don't have to chain together long dictionary access calls to get deep into the structure of our workflow config data object.

A psuedo-Snakefile that interfaces with the above _basic-config.yaml_:

```python

from gardnersnake.core import Configuration
from pathlib import Path

config_filepath = Path("basic-config.yaml").resolve()
cfg = Configuration(filepath=config_filepath)
cfg.load

GLOBALS = cfg.global_params

# Rule A:
ruleA_params = cfg.get_rule_params("RuleA")
rule A:
  input: GLOBALS.files.some_reference, GLOBALS.files.some_metadata
  output: "some-output.txt"
  params: **(ruleA_params.parameters), log=GLOBALS.misc.workflow_log
  resources: **(ruleA_params.resources)
  shell:
    "mycommand {input} -o {output} --trys={params.par1} {params.par2} 2> {params.log}"

# Rule B:
ruleB_params = cfg.get_rule_params("RuleB")
ruleBfiles = [Path("plots/plot-out-B") / ext for ext in (".png", ".pdf", ".rData")]
rule B:
  input: "some-output.txt", GLOBALS.files.some_metadata
  output: "returncode.out"
  params: 
    **(ruleB_params.parameters),
    filestocheck=ruleBfiles,
    targetdir=str(Path("plots/")),
    log=GLOBALS.misc.workflow_log
  resources: **(ruleB_params.resources)
  shell:
    "Rscipt plotting.R -i {input} 2> {params.log} \
    && check_directory -o {output} {params.filestocheck} {params.targetdir} 2> {params.log}"
```

One important note about the above Snakefile. You can see that the field in the configuration file `workflow_log` is now accessed not at the top level but under the attribute `misc`. In the global configuration, every field which is not one of the three required fields is refiled under this miscillaneous attributes field with thier structure otherwise preserved. This is not the case in rule configurations because every non-file field specific to the rule is likely to fit well under parameters or resources. Because of this, all other fields in the __RULE_CONFIG__ documents other than the required ones are ignored by the `Configuration.load()` routine.


## <a name="commandline_tools"> </a> 5. Command Line Tools
### check_directory

Many bioinformatics tools produce directories of various structure with large numbers of output files. Rather than require Snakemake to keep track of these outputs as global outputs, the `check_directory` command-line utility validates output directories against a known set of files, and returns a small file containing a return code (0) if the directory of interest was successfully validated. `check_directory` throws an error and does not write the return code file if it is unable to validate the contents according to the given requirements.

The options and requirements are specified in the usage message and can be retrieved using the `-h` or `--help` flags.

```
usage: check_directory [-h] [-o OUT] FILES [FILES ...] DIR

Validates dynamic directory contents against expectations. If each of the required files is present in the directory, the
program writes '0' to the output file. otherwise, it returns an Error

positional arguments:
  FILES                 set of filepaths to check against dir contents
  DIR                   filepath of directory to verify

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --output OUT  name of return code output file
```

__Positional Options__ \

* `FILES` [_required_] a list of whitespace separated files to search for in the passed directory. these file names should be specified without their path extensions (i.e. a file whose full path is _/home/user/analysis/myoutputs/output1.txt_ should be passed as _output1.txt_ if the `DIR` is indicated to be _/home/user/analysis/myoutputs/_)
* `DIR` [_required_] is the full path of the directory to verify. `~/` conventions are acceptable but shell variable syntax such as `$WORKDIR` are not supported. Relative path functionality remains in active development but is not guaranteed to work as of the current version (0.4.1)

__Flagged Options__ \

* `--ouput -o` [_required_] specifies the name of the file generated (containing the return code) when the passed directory is successfully validated.


```bash
check_dir -o rc.out output1.txt output2.txt ~/myanalysis/outputs/
```

which should return a file called _rc.out_ if the folder _~/myanalysis/outputs/_ has at least two files --> _output1.txt_ and _output2.txt_



