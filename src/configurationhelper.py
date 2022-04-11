# File Name: configurationhelper.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: a class definition for a configurationHelper that makes
#  snakemake worflows easier to construct


class ConfigurationHelper:
    def __init__ (self, cfg_dict):
        self.d = cfg_dict
        self.resource_list = [
            "walltime","nodes",
            "processors_per_node"
        ]

    def get_gobal_param(self, param):
        pass

    def get_rule_param(self, rule, param, ispath=False, exists=False):
        pass

    def get_rule_resources(self, rule, logdir="logs/", job_id):
        pass
