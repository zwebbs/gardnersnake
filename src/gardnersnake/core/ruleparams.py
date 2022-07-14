# File Name: rparams.py
# Created By: ZW
# Created On: 2022-07-12
# Purpose: defines the dataclass holding rule parameters and resources

# module imports 
from dataclasses import dataclass
from typing import Dict, Union
from .dotdict import dotdict
from .yamlconfig import YamlConfig

# dataclass definition for an object to contain rule parameters
# and resources for a snakemake workflow
@dataclass(frozen=True)
class RuleParams:
    rule_name: str
    parameters: dotdict
    resources: dotdict

# function to build an Rparam class object from a YamlConfig object
def get_ruleparams(yamlconfig, rule_name):
    ruledict = yamlconfig["rules_config"][rule_name]

# TODO: Write tests
# tests for the class definition
if __name__ == "__main__":
    pass