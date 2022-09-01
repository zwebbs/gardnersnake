# File Name: config.py
# Created By: ZW
# Created On: 2022-07-13
# Purpose: Defines a configuration object that simplifies the writing of
# snakemake workflows. the core object. <class Configuration> stores both
# the global and rule-level workflow parameters, including resource specs
# for each rule.


# Module Imports
# -----------------------------------------------------------------------------
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from sys import stderr
from typing import Dict, List, Optional, Union
from yaml import load_all, SafeLoader
from .exceptions import UserError


# Type Definitions
# -----------------------------------------------------------------------------
PATH_T = Union[str, Path]  # defines a type for filepaths

# Global Definitions
# -----------------------------------------------------------------------------
ALLOWED_DOC_TYPES = ("GLOBAL_CONFIG", "RULE_CONFIG")

# Error and Exception Definitions
# -----------------------------------------------------------------------------
## Define an Error for loading the configuration in the class
## <class Configuration> which is raised if none of the documents in
## the yaml file have the keyword `DOC_TYPE: "configuration"`
class YamlConfigLoadError(UserError):
    def __init__ (self, fname, message, *args, **kw):
        super(UserError, self).__init__(message, *args, **kw)
        self.fname = fname
        self.message = message

    def __str__(self) -> str:
        err_prelude = f"""

            Error! Cannot Properly load Yaml Config from file.
            Passed file: {self.fname}
        -------------------------------------------------------
        """
        self._eprint(err_prelude)
        return self.message

## Define an Error for retrieving rule data in the class <class Configuration>
## which is raised when the user asks for data from a rule whose name is not 
## catalogued in the attribute tuple Configuration.rule_names
class YamlConfigRuleError(UserError):
    def __init__(self,message, *args, **kw):
        super(UserError, self).__init__(message, *args, **kw)
        self.message= message

    def __str__(self) -> str:
        err_prelude = f"""
        Error! Inappropriate access attemt on rule parameters
        ------------------------------------------------------
        """
        self._eprint(err_prelude)
        return self.message

# Class Definitions
# -----------------------------------------------------------------------------

## Define a class <class Dotdict> which functions identically to
## a normal dictionary object but has attribute-style '.' access
## for instance `dd = Dotdict({"key1":val1})` allows `dd.key1`
class Dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


## Define a class <class GlobalParams> which adopts the dataclass schema
## and holds the top-level parameters for a given snakemake workflow
## Most importantly, the workflow files should be stored here
@dataclass(frozen=True)
class GlobalParams:
    analysis_name: str  # holds the name of the rule for internal reference
    working_directory: PATH_T  # holds the path for the specified workdir
    files: Dotdict  # holds all of the specified workflow files
    misc: Optional[Dotdict]  # holds any globals which are not the first three


## Define a class <class RuleParams> which adopts the dataclass schema
## and holds the rule-level parameters and resources for a given portion
## of the snakemake workflow, but importantly does not contain
## the input and output file inormation
@dataclass(frozen=True)
class RuleParams:
    rule_name: str # holds the name of the rule for internal reference
    parameters: Dotdict # holds the dictionary of items for params
    resources: Dotdict  # holds the dictionary of items for resources


## Define a class <class Configuration> that loads our yaml configuration
## file and structures the information to make access easy in a Snakefile
class Configuration:
    def __init__(self, filepath: PATH_T):
        self.filepath = filepath
        self.global_params = None
        self.rule_params = None
        self.rule_names = None

    # internal function that recursively turns nested dicts into Dotdicts
    # for '.' style attribute access
    def _recursive_convert_to_Dotdict(self, d: Dict) -> Dotdict:
        d = Dotdict(d)
        for key,value in d.items():
            if type(value) is dict:
                d[key] = self._recursive_convert_to_Dotdict(value)
            else:
                continue
        return d

    # internal method that loads global params from a config document with
    # the DOC_TYPE: GLOBAL_CONFIG tag. This method requires that global 
    # config documents have three mandatory sections: 
    # analysis_name -- A name given to the overall workflow instance
    # working_directory -- the name of the directory from which the workflow instance
    #   should be run.
    # files -- dictionary containing the files used in the workflow.
    # any other sections will be automatically packed into a field called misc
    def _load_global_params(self, globdict):
        globkeys = globdict.keys()
        reqd_keys = ("analysis_name", "working_directory", "files")

        # check that all of the keys required in a global config are present
        if any([reqd not in globkeys for reqd in reqd_keys]):
            msg = f"""
            At least one of {reqd_keys}, could not be
            located in the passed global configuration.
            please include all required fields.
            (even if they are empty)
            global config: {globdict}
            """
            raise YamlConfigLoadError(self.filepath,msg)

        # if all of the required keys are present, build the config
        misc = {k:v for k,v in globdict.items() if k not in reqd_keys}
        misc_dd = self._recursive_convert_to_Dotdict(misc)
        files_dd = self._recursive_convert_to_Dotdict(globdict["files"])
        self.global_params = GlobalParams(
            analysis_name=globdict["analysis_name"],
            working_directory=globdict["working_directory"],
            files=files_dd,
            misc=misc_dd
        )
        # return None after assignment to self.global_p
        return
    
    # internal method that loads rule params from a config document with
    # the DOC_TYPE: RULE_CONFIG tag. This method requires that rule
    # config documents have three mandatory sections: 
    # rule_name -- A name given to the rule (hopefully consistent with the Snakefile)
    # parameters -- dictionary containing non-file arguments to be used with the rule
    #   (typically those arguments which will be unpacked in the params: section of a 
    #    rule definition)
    # resources -- dictionary containing the resource specification for the rule in terms of
    # HPC compute resources. this is often helpful in external wrappers that make calls
    # to a job scheduler.
    # ** There are no additional fields considered or loaded in rule configs.
    def _load_rule_params(self, ruledict):
        if self.rule_params is None:
            self.rule_params = ()
            self.rule_names = ()
        rulekeys = ruledict.keys()
        reqd_keys = ("rule_name", "resources", "parameters")

        # check that all required keys are in the rule dict
        if any([reqd not in rulekeys for reqd in reqd_keys]):
            msg = f"""
            At least one of {reqd_keys}, could not be
            located in the passed rule configuration.
            please include all required fields.
            (even if they are empty)
            global config: {ruledict}
            """
            raise YamlConfigLoadError(self.filepath, self.msg)

        # build the rules config and append it to the list of rule configs
        rp = RuleParams(
                rule_name=ruledict["rule_name"],
                parameters=self._recursive_convert_to_Dotdict(ruledict["parameters"]),
                resources=self._recursive_convert_to_Dotdict(ruledict["resources"])
             )
        self.rule_params = (*self.rule_params, rp)
        self.rule_names = (*self.rule_names, rp.rule_name)

    # define a loading method to read the yaml from self.filepath and
    # integrate it into the Configuration class object.
    def load(self):
        with open(self.filepath, 'r') as yobj:
            docs = load_all(yobj, SafeLoader)
            for doc in docs:
                if doc["DOC_TYPE"] == "GLOBAL_CONFIG": self._load_global_params(doc)
                elif doc["DOC_TYPE"] == "RULE_CONFIG": self._load_rule_params(doc)
                else:
                    f"""
                    Passed document is not of type {ALLOWED_DOC_TYPES}
                    The offending document printed below. Please ensure that
                    the `DOC_TYPE:` field is at the top level and is one of 
                    the allowed types. 

                    malformed document: 
                    {doc}

                    """
                    raise YamlConfigLoadError(msg)

    # define a method to retrieve a set of rule parameters by first looking up
    # the position of the rule_name in the tuple of RuleParams objects.
    def get_rule_params(self, rulename):
        try:
            rule_idx = self.rule_names.index(rulename)
            return self.rule_params[rule_idx]
        except ValueError as ve:
            msg = f"""
            Could not find rule with name: {rulename}
            """
            raise YamlConfigRuleError(msg) from ve

