# File Name: confighelper.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: a class definition for a configurationHelper that makes
#  snakemake worflows easier to construct

# module imports
from operator import itemgetter
from .schemas import SchemaMap
from ..fileops.yamlparser import get_validated_from_schema

# function defintions
#------------------------------------------------------------------------------

# class definitions
#------------------------------------------------------------------------------

# class ConfigurationHelper: object which cleans up much of the code
# linking run conifgurations to snakefile. requires a specificly formatted
# yaml configuration which is described in a schema indicated by
# schema type. for more details please visit config/schemas.py
class ConfigurationHelper:
    def __init__ (self, cfg_dict, schema_type, schema_map=SchemaMap()):
        # load the configuration and validate it
        self.cfg = get_validated_from_schema(
            target_dict=cfg_dict,
            schema=schema_map.get_schema(schema_type),
            name="Workflow Configuration"
        )

        # useful operators to use in methods. these attributes are themselves
        # methods but easier and more consise to define here
        self._name_getter = itemgetter("rule_name")
        self._resources_getter = itemgetter("resources")
        self._parameters_getter = itemgetter("parameters")

        # attributes of the rule set held in the configuration
        self.rule_params = self.cfg['rule_params'] # list of rule objects
        self.rule_names = [self._name_getter(r) for r in self.rule_params]

    # define _get_rule() internal method which retrieves a rule by name from
    # the list of rules using a simple .index search of the rule names list
    def _get_rule(self, rule_name):
        idx = self.rule_names.index(rule_name)
        return self.rule_params[idx]

    # define get_resources() external method for returning the resource
    # dictionary for a particular passed rule
    def get_resources(self, rule_name):
        return self._resources_getter(self._get_rule(rule_name))

    # define get_parameters() external method for returning the parameter
    # dictionary for a partiuclar passed rule
    def get_parameters(self, rule_name):
        return self._parameters_getter(self._get_rule(rule_name))

    # define get_rule() external method which aliases the _get_rule()
    # internal methods for various edge case uses. most of the time
    # this should be unnecessary. return type is a dict
    def get_rule(self, rule_name):
        return self._get_rule(rule_name)

















    def get_static_params():
        return self._get("parameters")
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
        gp = self._get_global_param(param, ispath, pathtype, exists)
        if ((ispath) and (not returnPath)):
            return str(gp)
        else:
            return gp

    # define get_rule_param(): exposed wrapper for internal
    # method _get_rule_param()
    def get_rule_param(self, rule, param, ispath=False, pathtype=None,
                       exists=False, returnPath=False):

        rp = self._get_rule_param(rule, param, ispath, pathtype, exists)
        if ((ispath) and (not returnPath)):
            return str(rp)
        else:
            return rp

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
