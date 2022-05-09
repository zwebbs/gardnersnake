# File Name: datamanager.py
# Created By: ZW
# Created On: 2022-05-05
# Purpose: defines the DataManager class object which handles workflow
#   metadata. Along with ConfigurationHelper this is a foundational
#   object in the gardnersnake package.

# module imports
# -----------------------------------------------------------------------------
from ..fileops.yamlparser import get_validated_from_schema
from .schemas import SchemaMap
from operator import getitem, itemgetter
from functools import reduce


# class definitions
# -----------------------------------------------------------------------------


# class DataManager: object which cleans up much of the code relating to
# analysis data files in the snakefile. this class is intended to manage input
# and output files requires a specifically formatted yaml configuration which
# is described in a schema indicated by schema type. for more details please
# visit data/schemas.py
class DataManager:
    def __init__(self, metadata, schema_type, schema_map=SchemaMap()):
        self.metadata = get_validated_from_schema(
            target_dict=metadata,
            schema=schema_map.get_schema(schema_type),
            name="Workflow Metadata", quietly=False
        )
        self.get_rule_names = itemgetter("rule_name")
        self.rule_names = [self.get_rule_names(r) for r
                           in self._get_from_key_list(["rule_data"])
                           ]

        # define _get_from_key_list() internal method used to extract attributes

    # from deeply nested metadata dictionaries. the single argument, key_list
    # represents the successive keys required to descend the dictionary with
    # the last key in the list representing the attribute target.
    def _get_from_key_list(self, key_list, d=None):
        if not d:
            d = self.metadata
        return reduce(getitem, key_list, d)

    # define get_rule_data() external method which extracts attributes from the
    # rule_data subsection of the metadata file, given a generic key list
    # of descending keys
    def get_rule_data(self, rule_name, key_list):
        rule_idx = self.rule_names.index(rule_name)
        d = self.metadata["rule_data"][rule_idx]
        return self._get_from_key_list(key_list=key_list, d=d)
