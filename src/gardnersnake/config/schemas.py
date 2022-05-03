# File name: schemas.py
# Created By: ZW
# Created On: 2022-05-03
# Purpose: contains schema definitions for use with config validation
#    as well as a map of those definitions to a keyword dictionary for
#    ease of use.

# module imports
#------------------------------------------------------------------------------
from collections import defaultdict


# Schema Definitions
#------------------------------------------------------------------------------

# define a universally permissive configuration schema
CFG_SCHEMA_DEFAULT = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "permissive schema for any configuration, mostly for dev",
    "type": "object",
    "properties": {},
    "additionalProperties": True
}

# define a basic gardner configuration schema
CFG_SCHEMA_GARDNER_BASIC = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "minimum requirements for workflow cfgs run on gardner",
    "type": "object",
    "properties": {
        "analysis_id": {"type": "string"},
        "workdir": {"type": "string"},
        "rule_params": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "rule_name": {"type": "string"},
                    "walltime": {"type": "string"},
                    "nodes": {"type": "number"},
                    "processors_per_node": {"type": "number"},
                    "total_memory": {"type": "number"}
                },
                "additionalProperties": True,
                "required": [
                    "rule_name", "walltime", "nodes",
                    "processors_per_node", "total_memory"
                ]
            }
        }
    },
    "required": ["analysis_id", "workdir", "rule_params"],
    "additionalProperties": True
}


# Mapping Class Definition
#------------------------------------------------------------------------------

# define a helper function to return the universally permissive schema
# in a default dict
def get_universal_schema():
    return CFG_SCHEMA_DEFAULT

# define SchemaMap, a class containing the above defined schemas
# for ease of access in snakemake workflows with gardnersnake.
class SchemaMap:
    def __init__ (self):
        self.schema_map = defaultdict(get_universal_schema)
        self.schema_map.update({
            "CFG_DEFAULT": CFG_SCHEMA_DEFAULT,
            "CFG_GARDNER_BASIC": CFG_SCHEMA_GARDNER_BASIC
        })

    def get_schema(self, schema_type=None):
        return self.schema_map[schema_type]





