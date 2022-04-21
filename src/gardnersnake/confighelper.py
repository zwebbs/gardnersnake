# File Name: confighelper.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: a class definition for a configurationHelper that makes
#  snakemake worflows easier to construct

# module imports
from collections import OrderedDict
from .pathutils import get_verified_path
from .exceptions import eprint
from .exceptions import UserError
from .exceptions import ConfigParameterError
from .exceptions import ConfigRuleParameterError

# class definitions
#------------------------------------------------------------------------------

# class ConfigurationHelper: object which
# cleans up much of the code linking run
# conifgurations to snakefile rules.
class ConfigurationHelper:
    def __init__ (self, cfg_dict):
        self.cfg = cfg_dict
        self._validate_config_dict(self.cfg)
        self.globs = self.cfg.copy()
        self.rule_params = self.globs.pop("rule_params")
        self.resource_list = [
            "walltime","nodes",
            "processors_per_node"
        ]

    # define _validate_config_dict() function to ensure minimum requirements
    # for the passed configuration dict --including type checking the dict
    def _validate_config_dict(self,cfg):
        validation_codes = []
        keys_to_check = ["analysis_id", "workdir", "rule_params"]
        outcome = lambda x: validation_codes.append(x)

        # test the type of the passed dict
        outcome(type(cfg) in [dict, OrderedDict])

        # test default required keys
        for k in keys_to_check:
            outcome(k in cfg.keys())

        # verify validation codes
        if not validation_codes[0]: # type check
            eprint(f"passed config: {cfg}")
            raise UserError("Could not validate configuration dictionary")
        elif not all(validation_codes[1:]): # key checks
            msg1 = "Could not Validate Configuration in ConfiguationHelper."
            msg2 = "Please check the listed keys."
            msg = "\n".join([msg1,msg2])
            raise ConfigParameterError(cfg, msg, keys_to_check)
        else:
            return 0

    # define _get_global_param() internal method to return a top level
    # parameter from the passed configuration with optional path handling
    def _get_global_param(self, param, ispath=False,
                         pathtype=None, exists=False):
        # access the parameter, check if we need to do path handling
        # and return accordingly
        try: gparam = self.globs[param]
        except KeyError as ke:
            msg = "Key Error"
            perr = ConfigParameterError(self.globs,msg,param)
            raise perr from ke
        if not ispath: return gparam
        else:
            return get_verified_path(gparam, pathtype, exists)

    # define _get_rule_param() internal method to return a rule-level
    # parameter from the passed configuration with optional path handling
    def _get_rule_param(self, rule, param, ispath=False,
                        pathtype=None, exists=False):
        # access the parameter, check if we need to do path handling
        # and return accordingly.
        try: rparam = self.rule_params[rule][param]
        except KeyError as ke:
            msg = "Key Error"
            rperr = ConfigRuleParameterError(self.rule_params, msg, param, rule)
            raise rperr from ke
        if not ispath: return rparam
        else:
            return get_verified_path(rparam, pathtype, exists)

    # define get_global_param(): exposed wrapper for internal
    # method _get_global_param()
    def get_global_param(self, param, ispath=False, pathtype=None,
                         exists=False, returnPath=False):
        if returnPath:
            return self._get_global_param(param, ispath, pathtype, exists)
        else:
            return str(self._get_global_param(param,
                            ispath, pathtype, exists))

    # define get_rule_param(): exposed wrapper for internal
    # method _get_rule_param()
    def get_rule_param(self, rule, param, ispath=False, pathtype=None,
                       exists=False, returnPath=False):
        if returnPath:
            return self._get_rule_param(rule, param, ispath, pathtype, exists)
        else:
             return str(self._get_rule_param(rule, param,
                                ispath, pathtype, exists))

    # define get_rule_resources(): returns the standard resource set
    # as a dictionary according to the internal resource list-
    # self.resource_list
    def get_rule_resources(self, rule, logdir="logs/", jobid=""):
        # build resource dictionary and return
        rule_spec = self.rule_params[rule]
        addendum = {"log_dir":logdir, "job_id":jobid}
        resources = {}
        resources.update(addendum)

        # build out the rest of the resources through a dictionary comp.
        try:
            rtrigger = None
            for r in self.resource_list:
                rtrigger = r
                resources.update({r:rule_spec[r]})
            return resources
        except KeyError as ke:
            msg = "Could not find resource of the indicated type"
            crpe = ConfigRuleParameterError(rule_spec, msg, rtrigger, rule)
            raise crpe from ke


# EOF
