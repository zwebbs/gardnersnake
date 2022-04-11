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
class UserError:
    def __init__ (self, message):
        self.message = message
        super().__init__(self.message)

    def __str__ (self):
        pass
