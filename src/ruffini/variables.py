from collections import Counter


class VariablesDict(Counter):
    """
    A VariablesDict is a dictionary with
    some other features, created to manage
    in a better way the variables of a monomial.
    The changes are:
    - If a key isn't in the dictionary,
      its value is 0
    - All the keys (wich are the letters) will
      be made lowercase
    - The letters must be alphabetical and with
      a lenght of one
    - The values (wich are the exponent) have to be
      integer (5.0 is allowed) and positive
    """

    def __init__(self, **kwargs):
        """
        Initialize the VariablesDict by giving
        the pairs key:value as keyword-arguments.

        >>> VariablesDict(x=5, y=3)
        {'x': 5, 'y': 3}
        >>> VariablesDict(Y=5)
        {'y': 5}
        >>> VariablesDict(a=2, b=8, c=3)
        {'a': 2, 'b': 8, 'c': 3}
        """
        super(VariablesDict, self).__init__(None)

        # Add the values
        for k in kwargs:
            self.__setitem__(k, kwargs[k])

    def __setitem__(self, key, value):
        """
        Insert a pair of key:value into the dictionary
        if the values if is not zero and the key
        respect the features descripted before.
        It automatically make the key lowercase.

        >>> vd = VariablesDict(y=3)
        >>> vd['x'] = 18
        >>> vd
        {'x': 18, 'y': 3}

        The keys are automatically made lowercase

        >>> vd['S'] = 2
        >>> vd
        {'x': 18, 'y': 3, 's': 2}

        If the value is 0, it wont be inserted
        into the dictionary

        >>> vd['a'] = 0
        >>> vd
        {'x': 18, 'y': 3, 'S': 2}
        >>> vd['x'] -= 18 # 18 - 18 = 0
        >>> vd
        {'x': 18, 'y': 3, 'S': 2}

        You can also assign a float to a variable,
        if it represents whole number
        >>> vd['b'] = 9.0
        >>> vd
        {'x': 18, 'y': 3, 'S': 2, 'b': 9}

        :type key: str
        :type value: int, float
        :raise: TypeError, ValueError
        """

        if value == 0:
            self.__delitem__(key)

        # Check variable name
        elif not isinstance(key, str):
            raise TypeError("Variable name must be str")
        elif len(key) > 1:
            raise ValueError("Variable name lenght must be one")
        elif not key.isalpha():
            raise ValueError("Variable name must be alphabetical")

        # Check variable exponent
        elif not isinstance(value, (int, float)):
            raise TypeError("Exponent must be int or float")
        elif isinstance(value, float) and not value.is_integer():
            raise ValueError("Exponent must be a whole number")
        elif value < 0:
            raise ValueError("Exponent must be positive")

        else:
            super(VariablesDict, self).__setitem__(key.lower(), int(value))

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
