# File Name: config.py 
# Created By: ZW
# Created On: 2022-07-13
# Purpose: Defines a configuration object that simplifies the writing of 
# snakemake workflows. the core object. <class Configuration> stores both 
# the global and rule-level workflow parameters, including resource specs
# for each rule. 


# Module Imports
# ----------------------------------------------------------------------------
from dataclasses import dataclass
from pathlib import Path
from typing import Union
# Function Definitions
# ----------------------------------------------------------------------------

# Class Definitions
# ----------------------------------------------------------------------------

## Define a class <class Dotdict> which functions identically to
## a normal dictionary object but has attribute-style '.' access
## for instance `dd = Dotdict({"key1":val1})` allows `dd.key1`
class Dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


## Define a class <class RuleParams> which adopts the dataclass schema
## and holds the rule-level parameters and resources for a given portion
## of the snakemake workflow, but importantly does not contain
## the input and output file inormation
@dataclass(frozen=True)
class RuleParams:
    rule_name: str # holds the name of the rule for internal reference
    parameters: Dotdict # holds the dictionary of items for params 
    resources: Dotdict  # holds the dictionary of items for resources:


## Define a class <class Configuration> that loads our yaml configuration
## file and structures the information to make access easy in a Snakefile
class Configuration:
    def __init__(self, filepath: Union[str,Path]):
        self.cfg: DICT_T = self.read_yaml(filepath)
    
    # re-define getitem to access cfg
    def __getitem__(self, key: str) -> Any: return self.cfg[key]
    
    # read in a yaml file from a filepath
    def read_yaml(self, path: Union[str, Path]) -> DICT_T:
        with open(path) as fobj:
            cfg: DICT_T = safe_load(fobj)
            return cfg        




