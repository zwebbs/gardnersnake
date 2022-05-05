# File name: yamlparser.py
# Created By: ZW
# Created On: 2022-05-03
# Purpose: parsing tools for yaml files containing workflow configurations
#  and sample metadata.

# module imports
#------------------------------------------------------------------------------
from pprint import PrettyPrinter
from .pathutils import get_verified_path
from ..misc.exceptions import YAMLValidationError

from jsonschema import validate, ValidationError
import yaml

# function definitions
#------------------------------------------------------------------------------
# define read_yaml_config(): a function which takes a file path string as input
# and returns a list of dictionaries the first of which is the workflow
# configuration and the second of which is the metadata for the data inputs
def read_yaml_extended_config(filename):
    yamlpath = get_verified_path(filename, pathtype='file', strict=True)
    with open(yamlpath, 'r') as fh:
        rawdat = fh.read()
        yml_data = yaml.safe_load_all(rawdat)
    return [next(yml_data), next(yml_data)]

# define get_validated_from_schema(): a function which takes a dictionary and
# a schema pattern and returns the original dictionary if and only if it can
# be validated according to the json schema pattern provided (the schema)
# pattern is also a dictionary. please see schemas.py for specs
def get_validated_from_schema(target_dict, schema, name, quietly=False):
    try:
        validate(instance=target_dict, schema=schema)
        if not quietly:
            print(f"Successfully Validated {name}")
        return target_dict
    except ValidationError as verr:
        epprinter = PrettyPrinter(indent=4, width=60)
        target_fmtd = epprinter.pformat(target_dict)
        schema_fmtd = epprinter.pformat(schema)
        msg = f"""
        -----------------------------------------------------
        Passed Attributes: {target_fmtd}
       ------------------------------------------------------
        Schema Format {schema_fmtd}
        """
        raise YAMLValidationError(name,msg) from verr

# EOF
