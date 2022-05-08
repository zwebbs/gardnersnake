# File Name: datamanager.py
# Created By: ZW
# Created On: 2022-05-05
# Purpose: defines the DataManager class object which handles workflow
#   metadata. Along with COnfigurationHelepr this is a foundational
#   object in the gardnersnake package.

# module imports
#------------------------------------------------------------------------------
from .schemas import SchemaMap
from ..fileops.

# class definitions
#------------------------------------------------------------------------------






class DataManager:
    def __init__ (self, metadata, schema_type, schema_map=sm.SchemaMap()):
        self.metadata = get_validated_from_schema(
            target_dict=metadata,
            schema=schema_map.get_schema(schema_type),
            name="Workflow Metadata", quietly=False)

