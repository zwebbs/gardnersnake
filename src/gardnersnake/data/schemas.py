# File name: schemas.py
# Created By: ZW
# Created On: 2022-05-03
# Purpose: contains schema definitions for use with metadata validation
#    as well as a map of those definitions to a keyword dictionary for
#    ease of use.

# module imports
#------------------------------------------------------------------------------
from collections import defaultdict


# schema definitions
#------------------------------------------------------------------------------

# define a universally permissive configuration schema
META_SCHEMA_DEFAULT = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "permissive schema for any metadata structure, for dev",
    "type": "object",
    "properties": {},
    "additionalProperties": True
}
# mapping class definition
#------------------------------------------------------------------------------

# define a helper function to return the universally permissive schema
# in a default dict
def get_universal_schema():
    return META_SCHEMA_DEFAULT

# define SchemaMap, a class containing the above defined schemas
# for ease of access in snakemake workflows with gardnersnake.
class SchemaMap:
    def __init__ (self):
        self.schema_map = defaultdict(get_universal_schema)
        self.schema_map.update({
            "META_DEFAULT": META_SCHEMA_DEFAULT
        })

    def get_schema(self, schema_type=None):
        return self.schema_map[schema_type]

# EOF
