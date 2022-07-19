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
from typing import Union
from yaml import load_all, SafeLoader
from .exceptions import UserError

# Type Definitions
# -----------------------------------------------------------------------------
PATH_T = Union[str, Path]  # defines a type for filepaths


# Function Definitions
# -----------------------------------------------------------------------------

## Define a series of functions <get_rulename>, <get_parameters>,
## <get_resources> that access a dictionary with the keywords
## rule_name, resources, parameters, respectively and throw warnings
## if unable
getrulename = itemgetter("rule_name")
getresources = itemgetter("resources")
getparameters = itemgetter("parameters")

def get_rulename(object):
    try: return getrulename(object)
    except KeyError as ke:
        errmsg = f"""
        Warning. This rule configuration has no rule_name field
        Without a name, this configuration will not be applied to the workflow
        For debugging purposes, the module is printed below:
        {object}
        """
        eprint(errmsg)
        return None

def get_resources(object):
    try: return getresources(object)
    except KeyError as ke:
        errmsg = f"""
        Warning. This rule configuration has no resources field.
        Without specified resources, this rule will likely fail.
        For debugging purposes, the module is printed below:
        {object}
        """
        eprint(errmsg)
        return None

def get_parameters(object):
    try: return getparameters(object)
    except KeyError as ke:
        errmsg = f"""
        No parameters field found for rule configuration: {object}.
        (This may or may not be intentional)
        """
        eprint(errmsg)
        return None


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



# Class Definitions
# -----------------------------------------------------------------------------

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
    def __init__(self, filepath: PATH_T):
        self.filepath = filepath
        self.cfg = None
        self.global_params = None
        self.rule_params = None

    # define a loading method to read the yaml from self.filepath and
    # integrate it into a general configuration (self.cfg)
    def load(self):
        with open(self.filepath, 'r') as yobj:
            docs = load_all(yobj, SafeLoader)
            for doc in docs:
                if doc["DOC_TYPE"] == "configuration":
                    self.cfg = doc
                    try:
                        self.gobal_params = self.cfg["GLOBAL_CONFIG"]
                    except KeyError as ke:
                        errmsg = """
                        Warning. Configuration document has no apparent Global
                        config parameters. If you need global parameters
                        please specify them under the header GLOBAL_CONFIG:
                        """
                        eprint(errmsg)
                    try:
                        rule_configs = self.cfg["RULE_CONFIG"]
                        ruleparams = Dotdict({})
                        for rule in rule_configs:
                            name = get_rulename(rule)
                            resources = get_resources(rule)
                            parameters = get_parameters(rule)

                            if type(resources) is dict:
                                resources = Dotdict(resources)
                            if type(parameters) is dict:
                                parameters = Dotdict(parameters)

                            ruleparams[name] = RuleParams(
                                rule_name=name,
                                resources=resources,
                                parameters=parameters
                            )
                        self.rule_params = ruleparams

                    except KeyError as ke:
                        errmsg = """
                        Warning. Configuration document has no apparent Rule
                        config parameters. If you need rule parameters please
                        specify them under the header RULE_CONFIG: [...] as
                        a list of dictionary type objects. see template for
                        details.
                        """
                        eprint(errmsg)

                    # break when we find a configuration (i.e. look no further)
                    break

            if not self.cfg:  # if there is no configuration in the yaml docs
                errmsg = """
                Please ensure that a configuration document is present in the
                yaml file and that is appropriately headed by
                DOC_TYPE: "configuration"
                """
                raise YamlConfigLoadError(self.filepath, errmsg)

