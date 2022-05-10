# File Name: confighelper.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: a class definition for a configurationHelper that makes
#  snakemake workflows easier to construct

# module imports
from operator import itemgetter
from .schemas import SchemaMap
from ..fileops.yamlparser import get_validated_from_schema

# function definitions
# -----------------------------------------------------------------------------

# class definitions
# -----------------------------------------------------------------------------


# class ConfigurationHelper: object which cleans up much of the code
# linking run configurations to snakefile. requires a specifically formatted
# yaml configuration which is described in a schema indicated by
# schema type. for more details please visit config/schemas.py
class ConfigurationHelper:
    def __init__(self, cfg_dict, schema_type, schema_map=SchemaMap()):
        # load the configuration and validate it
        self.cfg = get_validated_from_schema(
            target_dict=cfg_dict,
            schema=schema_map.get_schema(schema_type),
            name="Workflow Configuration"
        )

        # useful operators to use in methods. these attributes are themselves
        # methods but easier and more concise to define here
        self._name_getter = itemgetter("rule_name")
        self._resources_getter = itemgetter("resources")
        self._parameters_getter = itemgetter("parameters")

        # attributes of the rule set held in the configuration
        self.rule_params = self.cfg['rule_params']  # list of rule objects
        self.rule_names = [self._name_getter(r) for r in self.rule_params]

    # define _get_rule() internal method which retrieves a rule by name from
    # the list of rules using a simple .index search of the rule names list
    def _get_rule(self, rule_name):
        idx = self.rule_names.index(rule_name)
        return self.rule_params[idx]

    # define get_resources() external method for returning the resource
    # dictionary for a particular passed rule
    def get_resources(self, rule_name, return_job_id=True):
        if not return_job_id:
            out = (self._resources_getter(self._get_rule(rule_name))).copy()
            out.pop("job_id")
            return out
        else:
            return self._resources_getter(self._get_rule(rule_name))

    # define get_parameters() external method for returning the parameter
    # dictionary for a particular passed rule
    def get_parameters(self, rule_name):
        return self._parameters_getter(self._get_rule(rule_name))

    # define get_rule() external method which aliases the _get_rule()
    # internal methods for various edge case uses. most of the time
    # this should be unnecessary. return type is a dict
    def get_rule(self, rule_name):
        return self._get_rule(rule_name)

    # define get_glob() external method to produce globally defined
    # configuration elements like workdir and analysis_id
    def get_glob(self, glob):
        return self.cfg[glob]
