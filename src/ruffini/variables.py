class VariablesDict(dict):
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
      a length of one
    - The values (wich are the exponent) have to be
      integer (5.0 is allowed) and positive

    **NB** VariablesDict is a sublass of Counter, so all
    the methods of Counter are inherited
    from VariablesDict; many of these methods
    are not in this docs.
    """

    def __init__(self, **kwargs):
        """
        Initialize the VariablesDict by giving
        the pairs key:value as keyword-arguments.

        >>> print(VariablesDict(x=5, y=3))
        {'x': 5, 'y': 3}

        While inserting the pairs key: value, it
        also:

        - automatically makes the key lowercase.

        >>> VariablesDict(Y=3)
        VariablesDict(y=3)

        - doesn't insert the pair if the value is 0

        >>> VariablesDict(a=0, b=2)
        VariablesDict(b=2)

        - convert the value in int if it's a whole number

        >>> VariablesDict(c=9.0)
        VariablesDict(c=9)

        It can raise an error if:

        - the variable's name length is grater than 1

        >>> VariablesDict(xy=3)
        Traceback (most recent call last):
        ...
        ValueError: Variable name length must be one

        - the variable's name is not alphabetical

        >>> VariablesDict(x2=9)
        Traceback (most recent call last):
        ...
        ValueError: Variable name must be alphabetical

        - the exponent is not int or float

        >>> VariablesDict(k=[])
        Traceback (most recent call last):
        ...
        TypeError: Exponent must be int or float

        - the exponent is not a whole number

        >>> VariablesDict(z=7.13)
        Traceback (most recent call last):
        ...
        ValueError: Exponent must be a whole number

        - the exponent is negative

        >>> VariablesDict(f=-3)
        Traceback (most recent call last):
        ...
        ValueError: Exponent must be positive

        It also check if the dictionary is empty.

        >>> VariablesDict(a=2, b=8, c=3).is_empty
        False
        >>> VariablesDict(x=0).is_empty
        True

        :raise: TypeError, ValueError
        """

        variables = {}

        for key in kwargs:
            # Check variable name
            if not key.isalpha():
                raise ValueError("Variable name must be alphabetical")
            elif len(key) > 1:
                raise ValueError("Variable name length must be one")

            value = kwargs[key]

            # Check variable exponent
            if not isinstance(value, (int, float)):
                raise TypeError("Exponent must be int or float")
            elif isinstance(value, float) and not value.is_integer():
                raise ValueError("Exponent must be a whole number")
            elif value < 0:
                raise ValueError("Exponent must be positive")

            if not value == 0:
                variables[key.lower()] = int(value)

        super().__init__(variables)

        # Check if it's empty
        self.is_empty = not bool(len(self))

    ### Methods about Item storing ###

    def __setitem__(self, key, value):
        """
        Raise TypeError: VariablesDict is immutable

        :raise: TypeError
        """

        raise TypeError("VariablesDict is immutable")

    def __delitem__(self, key):
        """
        Raise TypeError: VariablesDict is immutable

        :raise: TypeError
        """

        raise TypeError("VariablesDict is immutable")

    def pop (self, key):
        """
        Raise TypeError: VariablesDict is immutable

        :raise: TypeError
        """

        raise TypeError("VariablesDict is immutable")

    def clear (self):
        """
        Raise TypeError: VariablesDict is immutable

        :raise: TypeError
        """

        raise TypeError("VariablesDict is immutable")

    def __getitem__(self, key):
        """
        Get the exponent of a variable by the
        variable's name

        >>> v = VariablesDict(a=2, b=3)
        >>> v['a']
        2

        If a variable isn't in the dictionary,
        its value is 0

        >>> v['k']
        0

        :type key: str
        :rtype: int
        """

        try:
            return super().__getitem__(key)
        except KeyError:
            return 0

    ### Methods about Representation ###

    def __str__(self):
        """
        Return the dict as a string (as a normal dict)

        >>> str(VariablesDict(x=5, y=3))
        "{'x': 5, 'y': 3}"
        >>> str(VariablesDict(Y=5))
        "{'y': 5}"

        :rtype: str
        """

        pairs = [f"'{k}': {self[k]}" for k in sorted(self.keys())]

        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        """
        Return the dict as a string

        >>> repr(VariablesDict(Y=5))
        'VariablesDict(y=5)'
        >>> repr(VariablesDict(a=2, b=8, c=3))
        'VariablesDict(a=2, b=8, c=3)'

        :rtype: str
        """

        pairs = [f"{k}={self[k]}" for k in sorted(self.keys())]
        return f"{self.__class__.__name__}({', '.join(pairs)})"

    ### Operations Methods ###

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
        :raise: TypeError
        """

        if not isinstance(other, VariablesDict):
            raise TypeError(f"unsupported operand type(s) for +: 'VariablesDict' and '{other.__class__.__name__}'")

        result = {}
        for letter in set(self) | set(other):
            result[letter] = self[letter] + other[letter]
        return VariablesDict(**result)

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
        :raise: ValueError, TypeError
        """

        if not isinstance(other, VariablesDict):
            raise TypeError(f"unsupported operand type(s) for -: 'VariablesDict' and '{other.__class__.__name__}'")

        result = {}
        for letter in set(self) | set(other):
            result[letter] = self[letter] - other[letter]
        return VariablesDict(**result)

    def __mul__ (self, other):
        """
        This method returns a VariablesDict
        whose exponent are equivalent to
        this ones, multiplied by the given
        integer positive number

        >>> VariablesDict(a=2, b= 5) * 3
        VariablesDict(a=6, b=15)

        :type other: int
        :rtype: VariablesDict
        :raise: TypeError, ValueError
        """

        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for *: 'VariablesDict' and '{other.__class__.__name__}'")
        elif other < 0:
            raise ValueError("Second operator must be positive")

        variables = {}
        for l in self:
            variables[l] = self[l] * other
        return VariablesDict(**variables)

    def __truediv__ (self, other):
        """
        Divide all the variables' exponents
        by the given number (other)

        >>> VariablesDict(a=4, b=2) / 2
        VariablesDict(a=2, b=1)

        If the variablesdict is not divisible
        by the number, it will raise a ValueError

        >>> VariablesDict(x=7) % 3
        False
        >>> VariablesDict(x=7) / 3
        Traceback (most recent call last):
        ...
        ValueError: cannot divide by 3

        Intead, if the second operator is not a
        number, it will raise a TypeError

        >>> VariablesDict(k=2) / 1.5
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for /: 'VariablesDict' and 'float'

        :type other: int
        :rtype: VariablesDict
        :raises: ValueError, TypeError
        """

        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for /: 'VariablesDict' and '{other.__class__.__name__}'")

        if not self % other:
            raise ValueError(f"cannot divide by {other}")

        return VariablesDict(**dict(map(lambda k: (k, self[k] / other), self)))

    def __mod__ (self, other):
        """
        This method returns True if all the
        variables' exponents can be divided
        by a given integer positive number

        >>> VariablesDict(a=2, b=4) % 2
        True
        >>> VariablesDict(a=2, b=4) % 3
        False

        :type other: int
        :rtype: bool
        :raise: TypeError
        """

        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for %: 'VariablesDict' and '{other.__class__.__name__}'")
        elif other < 0:
            raise ValueError("Second operator must be positive")

        return all(l % other == 0 for l in self.values())

    ### Hashing Methods ###

    def __hash__(self):
        """
        Return the hash for the VariablesDict.
        It's equal to the tuple of the items.

        >>> hash(VariablesDict(x=2)) == hash((('x', 2),))
        True

        :rtype: int
        """

        return hash(tuple(list((k, self[k]) for k in sorted(self.keys())))) 
