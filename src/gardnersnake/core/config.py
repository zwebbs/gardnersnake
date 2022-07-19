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


## Define a class <class GlobalParams> which adopts the dataclass schema
## and holds the top-level parameters for a given snakemake workflow
## Most importantly, the workflow files should be stored here
@dataclass(frozen=True)
class GlobalParams:
    analysis_name: str  # holds the name of the rule for internal reference
    working_directory: PATH_T  # holds the path for the specified workdir
    files: Union[List[Dotdict], List]  # holds all of the specified workflow files
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

    # internal function that recursively turns nested dicts into dotdicts
    def _recursive_convert_to_Dotdict(self, d: Dict):
        d = Dotdict(d)
        for key in d.keys():
            if type(key) is dict:
                d[key] = _recursive_convert_to_Dotdict(d[key])
            else:
                continue
        return d

    def load_global_params(self, globdict):
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
            raise YamlConfigLoadError(self.filepath, self.msg)

        # if all of the required keys are present, build the config
        misc = {k:v for k,v in globdict.items if k not in reqd_keys}
        misc_dd = _recursive_convert_to_Dotdict(misc, Dotdict)
        files_dd = _recursive_convert_to_Dotdict(files, Dotdict)
        self.global_params = GlobalParams(
            analysis_name=globdict["analysis_name"],
            working_directory=globdict["working_directory"],
            files=files_dd,
            misc=misc_dd
        )
        # return None after assignment to self.global_p
        return

    def load_rule_params(self, ruledict):
        if self.rule_params is None: self.rule_params = []
        rulekeys = ruledict.keys()
        reqd_keys = ["rule_name", "resources", "parameters"]

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

        # TODO: build the rules config and append it to the list of rule configs,
        # additionally, add the rule's name to the list of rulenames for easy lookup.



    def load2(self):
        with open(self.filepath, 'r') as yobj:
            docs = load_all(yobj, SafeLoader)
        for doc in docs:
            if doc["DOC_TYPE"] == "GLOBAL_CONFIG": self.load_global_params(doc)
            elif doc["DOC_TYPE"] == "RULE_CONFIG": self.load_rule_params(doc)
            else:
                # TODO: implement error for wrong DOC_TYPE
                pass


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

