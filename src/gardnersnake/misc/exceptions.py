# File Name: exceptions.py
# Created By: ZW
# Created On: 2022-04-11
# Purpose: provides exception classes and methods for gardnersnake package

# module imports
import sys # for sys.stderr
import json # for printing dicts

# function definitions
#------------------------------------------------------------------------------

# eprint(): printing function to alias print statements to sys.stderr
def eprint(*args, **kw):
    print(*args, file=sys.stderr, **kw)

# edictprint(): printing function to alias print
# statements to sys.stderr, specifically for printing dictionaries
# in parsable formats.
def edictprint(mydict, indent, **kw):
    print(json.dumps(mydict,indent=indent, default=str),
          file=sys.stderr, **kw
          )

# class definitions
#------------------------------------------------------------------------------

# UserError: base class for a custom user error
class UserError(Exception):
    def __init__ (self, message, *args, **kw):
        super(Exception,self).__init__(*args, **kw)
        self.message = message

    def __str__ (self):
        return f"{self.message}"

    def _eprint(self, *args, **kw):
        eprint(*args, **kw)

    def _edictprint(self, mydict, indent, **kw):
        edictprint(mydict, indent, **kw)

    def test_message(self):
        self._eprint(self.__str__())


# YAMLValidationError: exception class raised when we cannot validate
# configuration or metadata inputs from provided schemas
class YAMLValidationError(UserError):
    def __init__ (self, name, message, *args, **kw):
        super(YAMLValidationError, self).__init__(message, *args, **kw)
        self.name = name

    def __str__(self):
        self._eprint(f"Error in validation of YAML data for: {self.name}")
        return self.message

# EOF
