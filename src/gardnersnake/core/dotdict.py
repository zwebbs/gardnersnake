# File Name: dotdict.py
# Created By: ZW
# Created On: 2022-07-12
# Purpose: defines a dictionary class that has dot access for convenience and brevity

import pprint

# class that creates support for .access of dictionary elements
class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# tests 
if __name__ == "__main__":
    test_dict = dotdict({"A": 100, "B": dotdict({"C":1000})})
    print("Testing dotdict implementation")
    print("------------------------------")
    fmtd = pprint.pformat(test_dict)
    print(f"test_dict = {fmtd}")
    print(f"testing dotdict access.. first level (test_dict.A): {test_dict.A}")
    print(f"testing dotdict access.. second level (test_dict.B.C): {test_dict.B.C}")
    