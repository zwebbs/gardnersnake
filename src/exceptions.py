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


# ConfigParameterError: raising errors when configuration
# parameters cannot be located in the ConfigurationHelper
# class.
class ConfigParameterError(UserError):
    def __init__ (self, cfg, message, param, *args, **kw):
        super(ConfigParameterError, self).__init__(message, *args, **kw)
        self.cfg = cfg # stores internal representation of config
        self.param = param # parameter that raised the error

    def __str__ (self):
        self._eprint("\nError in the following portion of the configuration..")
        self._edictprint(self.cfg, indent=2)
        return f"Param --> {self.param}. {self.message}"


# RuleConfigurationError: raising errors having to do with
# accessing rule parameters
class ConfigRuleParameterError(ConfigParameterError):
    def __init__ (self, cfg, message, param, rule, *args, **kw):
        super(ConfigRuleParameterError, self).__init__(
            cfg, message, param, *args, **kw
        )
        self.rule = rule

    def __str__ (self):
        self._eprint("\nError in the following portion of the configuration..")
        self._edictprint(self.cfg, indent=2)
        return f"Rule --> {self.rule}, Param --> {self.param}. {self.message}"

#------------------------------------------------------------------------------
#EOF
