# File Name:
# Created By: ZW
# Created On: 2022-04-11
# Purpose: provides exception classes and methods for gardnersnake package

# module imports
import sys # for sys.stderr

# function definitions
#----------------------------

# eprint(): printing function to alias print statements to sys.stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# class definitions
#----------------------------

# UserError: base class for a custom user error
class UserError(Exception):
    def __init__ (self, message):
        self.message
        super().__init__(self.message)

    def __str__ (self):
        return f"{self.message}"


# ConfigParameterError: raising errors when configuration
# parameters cannot be located in the ConfigurationHelper
# class.
class ConfigParameterError(UserError):
    def __init__ (self, message, param):
        self.param = param
        super().__init__(message=message)

    def __str__ (self):
        return f"{self.param} -> {self.message}"



# RuleConfigurationError: raising errors having to do with
# accessing rule parameters
class RuleConfigurationError(UserError):
    def __init__ (self, message, rule, param):
        self.rule = rule
        self.param = param
        self.message = message
        super().__init__(self.message)

    def __str__ (self):
        return f"{self.rule}:{self.param} -> {self.message}"


# GlobConfigurationError: raising errors having to do with
# accessing global configuration parameters
class GlobConfigurationError(UserError):
    def __init__ (self, message, param):
        self.param = param
        self.message = message
        super().__init__(self.message)

    def __str__ (self):
        return f"{self.param} -> {self.message}"

