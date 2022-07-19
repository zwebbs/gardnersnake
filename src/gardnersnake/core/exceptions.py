# File Name exceptions.py
# Created By: ZW
# Created On: 2022-07-14
# Purpose: Defines shared exception and error classes between parts of
# the gardnersnake library


# Module Imports
# ----------------------------------------------------------------------------

# Type Definitions
# ----------------------------------------------------------------------------

# Function Definitions
# ----------------------------------------------------------------------------

## Define a function <def eprint> which aliases the print function to
## output to stderr rather than stdout for printing errors and warnings
def eprint(*args, **kw):
    print(*args, file=stderr, **kw)


# Error and Exception Defintions
# ----------------------------------------------------------------------------

## Define an Error <class UserError> which serves as the base class for 
## errors derived from IO operations. 
class UserError(Exception):
    def __init__ (self, message, *args, **kw):
        super(Exception,self).__init__(*args, **kw)
        self.message = message

    def __str__ (self) -> str:
        return f"{self.message}"

    def _eprint(self, *args, **kw):
        eprint(*args, **kw)

    def test_message(self):
        self._eprint(self.__str__())

