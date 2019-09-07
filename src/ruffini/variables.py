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

        >>> print(VariablesDict(x=5, y=3))
        {'x': 5, 'y': 3}
        >>> print(VariablesDict(Y=5))
        {'y': 5}
        >>> print(VariablesDict(a=2, b=8, c=3))
        {'a': 2, 'b': 8, 'c': 3}

        It also check if the dictionary is empty.

        >>> VariablesDict(a=2, b=8, c=3).empty
        False
        >>> VariablesDict(x=0).empty
        True
        """
        super(VariablesDict, self).__init__(None)

        # Add the values
        for k in kwargs:
            self.__setitem__(k, kwargs[k])

        # Check if it's empty
        self.empty = not bool(len(self))

    def __setitem__(self, key, value):
        """
        Insert a pair of key:value into the dictionary
        if the values if is not zero and the key
        respect the features descripted before.
        It automatically make the key lowercase.

        >>> vd = VariablesDict(y=3)
        >>> vd['x'] = 18
        >>> vd
        VariablesDict(x=18, y=3)

        The keys are automatically made lowercase

        >>> vd['S'] = 2
        >>> vd
        VariablesDict(s=2, x=18, y=3)

        If the value is 0, it wont be inserted
        into the dictionary

        >>> vd['a'] = 0
        >>> vd
        VariablesDict(s=2, x=18, y=3)
        >>> vd['x'] -= 18 # 18 - 18 = 0
        >>> vd
        VariablesDict(s=2, y=3)

        You can also assign a float to a variable,
        if it represents whole number
        >>> vd['b'] = 9.0
        >>> vd
        VariablesDict(b=9, s=2, y=3)

        :type key: str
        :type value: int, float
        :raise: TypeError, ValueError
        """

        # Check variable name
        if not isinstance(key, str):
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

        if value == 0:
            del self[key]

        else:
            super(VariablesDict, self).__setitem__(key.lower(), int(value))

    def __str__(self):
        """
        Return the dict as a string (as a normal dict)

        >>> str(VariablesDict(x=5, y=3))
        "{'x': 5, 'y': 3}"
        >>> str(VariablesDict(Y=5))
        "{'y': 5}"
        """

        pairs = [f"'{k}': {self[k]}" for k in sorted(self.keys())]

        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        """
        Return the dict as a string (as a normal dict)

        >>> repr(VariablesDict(Y=5))
        'VariablesDict(y=5)'
        >>> repr(VariablesDict(a=2, b=8, c=3))
        'VariablesDict(a=2, b=8, c=3)'
        """

        pairs = [f"{k}={self[k]}" for k in sorted(self.keys())]
        return f"VariablesDict({', '.join(pairs)})"

    def __add__(self, other):
        """
        Sum two VariablesDict, returning a VariablesDict
        whose values are the sum of the values of this
        and the second VariablesDict

        >>> VariablesDict(x=5, y=3) + VariablesDict(y=5)
        VariablesDict(x=5, y=8)
        >>> VariablesDict(x=18) + VariablesDict(y=4)
        VariablesDict(x=18, y=4)
        >>> VariablesDict(a=36) + VariablesDict()
        VariablesDict(a=36)

        :type other: VariablesDict
        :rtype: VariablesDict
        """
        if not isinstance(other, VariablesDict):
            return NotImplemented

        result = VariablesDict()
        for letter in set(self) | set(other):
            result[letter] = self[letter] + other[letter]
        return result

    def __sub__(self, other):
        """
        Subtract two VariablesDict, returning a
        VariablesDict whose values are the
        subtraction between the values of this
        dict and the values of the second one

        >>> VariablesDict(x=5, y=3) - VariablesDict(x=1, y=2)
        VariablesDict(x=4, y=1)
        >>> VariablesDict(x=18) - VariablesDict(x=18)
        VariablesDict()
        >>> VariablesDict(c=2) - VariablesDict(c=3)
        Traceback (most recent call last):
        ...
        ValueError: Exponent must be positive

        :type other: VariablesDict
        :rtype: VariablesDict
        :raise: ValueError
        """
        if not isinstance(other, VariablesDict):
            return NotImplemented

        result = VariablesDict()
        for letter in set(self) | set(other):
            result[letter] = self[letter] - other[letter]
        return result

    def __hash__(self):
        """
        Return the hash for the VariablesDict.
        It's equal to the tuple of the items.
        """
        return hash(tuple(list((k, self[k]) for k in self)))
