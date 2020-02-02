class VariablesDict(dict):
    """
    A VariablesDict is a dictionary with special
    features, created to manage in a better way
    the variables of a monomial. These features are:

    - If a key isn't in the dictionary, its value is 0
    - All the keys (representing letters) will be made lowercase
    - Letters must be alphabetical (only letter) and with a length
      of one
    - The values (representing exponents) have to be
      integer (things like 5.0 are allowed) and positive

    **NB** VariablesDict is a sublass of dict, so all
    the methods of dict are inherited rom VariablesDict;
    many of these methods are not in this docs.
    """

    def __init__(self, variables=None, **kwargs):
        """
        Initialize the VariablesDict by giving it
        the pairs key: value as keyword-arguments.

        >>> VariablesDict(x=5, y=3)
        {'x': 5, 'y': 3}

        While inserting the pairs key: value, it
        also:

        - automatically makes the key lowercase.

        >>> VariablesDict(Y=3)
        {'y': 3}

        - doesn't insert the pair if the value is 0

        >>> VariablesDict(a=0, b=2)
        {'b': 2}

        - convert the value in int if it's a whole number

        >>> VariablesDict(c=9.0)
        {'c': 9}

        It can raise an error if:

        - the variable's name length is grater than 1

        >>> VariablesDict(xy=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's name length must be one

        - the variable's name is not alphabetical

        >>> VariablesDict(x2=9)
        Traceback (most recent call last):
        ...
        ValueError: variable's name must be alphabetical

        - the exponent is not int or float

        >>> VariablesDict(k=[])
        Traceback (most recent call last):
        ...
        TypeError: variable's exponent must be int or float

        - the exponent is not a whole number

        >>> VariablesDict(z=7.13)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be a whole number

        - the exponent is negative

        >>> VariablesDict(f=-3)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive

        It also check if the dictionary is empty.

        >>> VariablesDict(a=2, b=8, c=3).is_empty
        False
        >>> VariablesDict(x=0).is_empty
        True

        :raise: TypeError, ValueError
        """

        if not variables:
            variables = kwargs

        new_variables = {}

        for key in variables:
            # Check variable name
            if not key.isalpha():
                raise ValueError("variable's name must be alphabetical")
            elif len(key) > 1:
                raise ValueError("variable's name length must be one")

            value = variables[key]

            # Check variable exponent
            if not isinstance(value, (int, float)):
                raise TypeError("variable's exponent must be int or float")
            elif isinstance(value, float) and not value.is_integer():
                raise ValueError("variable's exponent must be a whole number")
            elif value < 0:
                raise ValueError("variable's exponent must be positive")

            if not value == 0:
                new_variables[key.lower()] = int(value)

        super().__init__(new_variables)

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

    def pop(self, key):
        """
        Raise TypeError: VariablesDict is immutable

        :raise: TypeError
        """

        raise TypeError("VariablesDict is immutable")

    def clear(self):
        """
        Raise TypeError: VariablesDict is immutable

        :raise: TypeError
        """

        raise TypeError("VariablesDict is immutable")

    def __getitem__(self, key):
        """
        Get the exponent of a variable by giving
        it the variable's name

        >>> v = VariablesDict(a=2, b=3)
        >>> v['a']
        2

        If a variable isn't in the dictionary, its value is 0

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

        NB: Letters are sorted alphabetically:
        
        >>> str(VariablesDict(k=2, b=3))
        "{'b': 3, 'k': 2}"

        :rtype: str
        """

        pairs = [f"'{k}': {self[k]}" for k in sorted(self.keys())]

        return "{" + ", ".join(pairs) + "}"

    def __repr__(self):
        """
        Return the dict as a string

        >>> repr(VariablesDict(Y=5))
        "{'y': 5}"

        For more informations see :func:`VariablesDict.__str__()`.

        :rtype: str
        """

        return self.__str__()

    ### Operations Methods ###

    def __add__(self, other):
        """
        Sum two VariablesDict, returning a VariablesDict
        whose values are the sum of the values of the two
        VariablesDicts

        >>> VariablesDict(x=5, y=3) + VariablesDict(y=5)
        {'x': 5, 'y': 8}
        >>> VariablesDict(x=18) + VariablesDict(y=4)
        {'x': 18, 'y': 4}
        >>> VariablesDict(a=36) + VariablesDict()
        {'a': 36}

        If the second operator isn't a VariablesDict
        raise a TypeError

        >>> VariablesDict() + "-"
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for +: 'VariablesDict' and 'str'

        :type other: VariablesDict
        :rtype: VariablesDict
        :raise: TypeError
        """

        if not isinstance(other, VariablesDict):
            raise TypeError(f"unsupported operand type(s) for +: 'VariablesDict' and '{other.__class__.__name__}'")

        result = {}
        for letter in set(self) | set(other):
            result[letter] = self[letter] + other[letter]
        return VariablesDict(result)

    def __sub__(self, other):
        """
        Return a VariablesDict whose values are the subtraction
        of this ones and the second's ones:

        >>> VariablesDict(x=5, y=3) - VariablesDict(x=1, y=2)
        {'x': 4, 'y': 1}
        >>> VariablesDict(x=18) - VariablesDict(x=18)
        {}

        If any exponent will be negative, a ValueError
        will be raised instead:

        >>> VariablesDict(c=2) - VariablesDict(c=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive

        If the second operator isn't a VariablesDict
        raise a TypeError

        >>> VariablesDict() - "-"
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for -: 'VariablesDict' and 'str'

        :type other: VariablesDict
        :rtype: VariablesDict
        :raise: ValueError, TypeError
        """

        if not isinstance(other, VariablesDict):
            raise TypeError(f"unsupported operand type(s) for -: 'VariablesDict' and '{other.__class__.__name__}'")

        result = {}
        for letter in set(self) | set(other):
            result[letter] = self[letter] - other[letter]
        return VariablesDict(result)

    def __mul__ (self, other):
        """
        Returns a VariablesDict whose exponent are
        equivalent to this ones multiplied by a given
        number

        >>> VariablesDict(a=2, b= 5) * 3
        {'a': 6, 'b': 15}

        If the number is negative, a ValueError is
        raised

        >>> VariablesDict() * (-15)
        Traceback (most recent call last):
        ...
        ValueError: can't multiply a VariablesDict and a negative number

        Otherwise, a TypeError will be raised

        >>> VariablesDict() * {}
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for *: 'VariablesDict' and 'dict'

        :type other: int
        :rtype: VariablesDict
        :raise: TypeError, ValueError
        """

        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for *: 'VariablesDict' and '{other.__class__.__name__}'")
        elif other < 0:
            raise ValueError("can't multiply a VariablesDict and a negative number")

        variables = {}
        for l in self:
            variables[l] = self[l] * other
        return VariablesDict(variables)

    def __truediv__ (self, other):
        """
        Divide the variables' exponents by the given number

        >>> VariablesDict(a=4, b=2) / 2
        {'a': 2, 'b': 1}

        If the variablesdict is not divisible
        by the number, it will raise a ValueError

        >>> VariablesDict(x=7) / 3
        Traceback (most recent call last):
        ...
        ValueError: can't divide a VariablesDict by 3

        To see if a variables dict is divisible by a number,
        you can use modulus:

        >>> VariablesDict(x=7) % 3
        False

        Instead, if the second operator is not an integer
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
            raise ValueError(f"can't divide a VariablesDict by {other}")

        return VariablesDict(dict(map(lambda k: (k, self[k] / other), self)))

    def __mod__ (self, other):
        """
        Check if the VariablesDict can be
        divided for a number

        >>> VariablesDict(a=2, b=4) % 2
        True
        >>> VariablesDict(a=2, b=4) % 3
        False

        Can raise a TypeError when `other` is not
        an integer

        >>> VariablesDict(k=2) % []
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for %: 'VariablesDict' and 'list'

        Or ValueError when `other` isn't positive

        >>> VariablesDict(k=2) % (-7)
        Traceback (most recent call last):
        ...
        ValueError: can't use modulus with VariablesDict and negative numbers

        :type other: int
        :rtype: bool
        :raise: TypeError
        """

        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for %: 'VariablesDict' and '{other.__class__.__name__}'")
        elif other < 0:
            raise ValueError("can't use modulus with VariablesDict and negative numbers")

        return all(l % other == 0 for l in self.values())

    ### Hashing Methods ###

    def __hash__(self):
        """
        Return the hash of a VariablesDict.
        It's equal to the tuple of its items.

        >>> hash(VariablesDict(x=2)) == hash((('x', 2),))
        True

        :rtype: int
        """

        return hash(tuple(list((k, self[k]) for k in sorted(self.keys()))))
