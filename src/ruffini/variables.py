from collections import defaultdict


class VariablesDict (defaultdict):
    def __init__(self, **kwargs):
        """
        Initialize the VariablesDict.
        VariablesDict is a normal dictionary,
        with only few changes:
        -> If a key isn't in the vd, is value
           will be 0
        -> All the keys are in lowercase, with
           a lenght of one and only alphabetical
           characters
        -> All the values are integer

        >>> VariablesDict(a=5, b=2, c=0) # c is ignored
        {'a': 5, 'b': 2}
        """
        super().__init__(None)
        for k in kwargs:
            self.__setitem__(k, kwargs[k])

    def __missing__(self, *args):
        """
        If a key isn't present in the dictionary
        its value will always be zero.
        """
        return 0

    def __setitem__(self, key, value):
        """
        Insert a pair of key: value into the dictionary
        if the values if different from zero and the key
        is alphabetical and with a lenght of one. It
        trasforms the key in lowercase and the value in a
        integer
        """
        if value == 0:
            pass
        elif len(key) > 1 or not key.isalpha():
            raise ValueError(f"Variable not valid ({key})")
        elif isinstance(value, float) and not value.is_integer():
            raise ValueError(f"Variable not valid ({key} = {value})")
        else:
            super().__setitem__(key.lower(), int(value))

    def __str__(self):
        """
        Return the dict as a string (as a normal dict)
        """
        return str(dict(self))

    def __repr__(self):
        """
        Return the dict as a string (as a normal dict)
        """
        return repr(dict(self))
