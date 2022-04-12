# File Name: confighelper.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: a class definition for a configurationHelper that makes
#  snakemake worflows easier to construct

# module imports
from .pathutils import get_verified_path
from .exceptions import RuleConfigurationError
from .exceptions import GlobConfigurationError

# class definitions
#-----------------------

# class ConfigurationHelper: object which
# cleans up much of the code linking run
# conifgurations to snakefile rules.
class ConfigurationHelper:
    def __init__ (self, cfg_dict):
        self.cfg = self.globs = cfg_dict.copy()
        self.rule_params = self.cfg.pop("rule_params")
        self.resource_list = [
            "walltime","nodes",
            "processors_per_node"
        ]

    # internal methods
    #-------------------

    # _get_global_param()
    # returns global parameters with optional path handling
    def _get_global_param(self, param, ispath=False,
                         pathtype=None, exists=False):
        # access the parameter, check if we need to do path handling
        # and return accordingly
        try: gparam = self.globs[param]
        except KeyError as kexc:
            msg = "could not find entry in configuration"
            raise GlobConfigurationError(msg,param) from kexc
        if not ispath: return gparam
        else:
            return get_verified_path(gparam,pathtype, exists)

    # _get_rule_param()
    # returns rule parameters with optional path handling
    def _get_rule_param(self, rule, param, ispath=False,
                        pathtype=None, exists=False):
        # access the parameter, check if we need to do path handling
        # and return accordingly. if its not in the config, raise
        # a custom exception (RuleConfigurationError)
        try:rparam = self.rule_params[rule][param]
        except KeyError as kexc:
            msg = "could not find entry in configuration"
            raise RuleConfigurationError(msg,rule,param) from kexc
        if not ispath: return rparam
        else:
            return get_verified_path(rparam, pathype, exists)


    # exposed methods
    #-------------------

    # get_global_param()
    # wrapper for internal method _get_global_param
    def get_global_param(self, param, ispath=False,
                         pathtype=None, exists=False):
        return self._get_global_param(param, ispath, pathtype, exists)

    # get_rule_param()
    # wrapper for internal method _get_rule_param
    def get_rule_param(self, rule, param, ispath=False,
                       pathtype=None, exists=False):
        return self._get_rule_param(rule, param, ispath, pathtype, exists)

    # get_rule_resources()
    # returns the standard resource set as a dictionary according
    # to the internal resource list: self.resource_list
    def get_rule_resources(self, rule, logdir="logs/", jobid=""):
        # build resource dictionary and return
        resources = {r:self._get_rule_param(rule,r) for r in self.resource_list}
        addendum = {"log_dir":logdir, "job_id":jobid}
        resources.update(addendum)
        return resources








