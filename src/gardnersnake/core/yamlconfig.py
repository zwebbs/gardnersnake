# File Name: yamlconfig.py
# Created By: ZW
# Created On: 2022-07-12
# Purpose: defines a class containing the yaml config
# read in from a file passed to the filepath argument

# module imports
from pathlib import Path
from typing import Any, Dict, Union
from yaml import safe_load 

# global type declarations
DICT_T = Dict[str, Any]

# small class definition of Yaml Config object has one argument at instantiation
# which is the filepath (either string or pathlib.Path object) corresponding 
# to the yaml configuration file.
class YamlConfig:
    def __init__(self, filepath: Union[str, Path]):
        self.cfg: DICT_T = self.read_yaml(filepath)
    
    # re-define getitem to access cfg
    def __getitem__(self, key: str) -> Any: return self.cfg[key]
    
    # read in a yaml file from a filepath
    def read_yaml(self, path: Union[str, Path]) -> DICT_T:
        with open(path) as fobj:
            cfg: DICT_T = safe_load(fobj)
            return cfg
    