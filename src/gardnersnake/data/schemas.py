# File name: schemas.py
# Created By: ZW
# Created On: 2022-05-03
# Purpose: contains schema definitions for use with metadata validation
#    as well as a map of those definitions to a keyword dictionary for
#    ease of use.

# module imports
# -----------------------------------------------------------------------------
from collections import defaultdict


# schema definitions
# -----------------------------------------------------------------------------

# define a universally permissive metadata schema
META_SCHEMA_DEFAULT = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "permissive schema for any metadata structure, for dev",
    "type": "object",
    "properties": {},
    "additionalProperties": True
}

# define a basic metadata schema for basic sequencing-based workflows
META_SCHEMA_GARDNER_SEQ_BASIC = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "basic schema for basic sequencing workflow metadata",
    "type": "object",
    "properties": {
        "shared_data": {
            "type": "array",
        },
        "rule_data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "rule_name": {"type": "string"}
                },
                "additionalProperties": True,
                "required": ["rule_name"]
            },
        }
    },
    "additionalProperties": False,
    "required": ["shared_data", "rule_data"]
}

# class definitions
# -----------------------------------------------------------------------------


# define SchemaMap, a class containing the above defined schemas
# for ease of access in snakemake workflows with gardnersnake.
class SchemaMap:
    def __init__(self):
        self.schema_map = dict()
        self.schema_map.update({
            "META_DEFAULT": META_SCHEMA_DEFAULT,
            "META_GARDNER_SEQ_BASIC": META_SCHEMA_GARDNER_SEQ_BASIC
        })

    def get_schema(self, schema_type=None):
        return self.schema_map[schema_type]
