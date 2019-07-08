from collections import Counter


class VariablesDict(Counter):
    def __init__(self, **kwargs):
        """
        Initialize the VariablesDict.
        VariablesDict is a normal dictionary,
        with only few changes:
        -> If a key isn't in the vd, is value
           will be 0
        -> If a value is 0, it won't be inserted
           into the dictionary
        -> All the keys are in lowercase, with
           a lenght of one and made of only
           alphabetical characters
        -> All the values are integer
        """
        super().__init__(None)

        for k in kwargs:
            self.__setitem__(k, kwargs[k])

    def __setitem__(self, key, value):
        """
        Insert a pair of key: value into the dictionary
        if the values if different from zero and the key
        is alphabetical and with a lenght of one. It
        trasforms the key in lowercase and the value in a
        integer
        """
        if value == 0:
            self.__delitem__(key)
        elif not isinstance(key, str):
            raise TypeError(f"Variable name not valid ({key})")
        elif len(key) > 1 or not key.isalpha():
            raise ValueError(f"Variable name not valid ({key})")
        elif isinstance(value, float) and not value.is_integer():
            raise TypeError(f"Variable value not valid ({key} = {value})")
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
