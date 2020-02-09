from collections import frozendict

class VariablesDict(frozendict):
    """
    A VariablesDict is a dictionary with special
    features, created to manage in a better way
    the variables of a monomial.

    In this case, we'll call keys variables and
    values exponents.

    Anyway, the changes are:

    - If a variable isn't in the dictionary, its exponent is 0
    - Therefore, variables with exponent 0 won't be inserted
    - Variables are made lowercase
    - Variables must be letters from the latin alphabet
      and one-character long
    - Exponents must be integer

    **NB** VariablesDict is a sublass of dict, so all
    the methods of dict are inherited rom VariablesDict;
    many of these methods are not in this docs.
    """

    def __init__(self, variables=None, **kwargs):
        """
        Initialize the VariablesDict by giving it
        the pairs variable: exponent storing them
        in a dict (variables) or as keyword arguments:

        >>> VariablesDict({'x': 5, 'y': 3})
        {'x': 5, 'y': 3}
        >>> VariablesDict(x=5, y=3)
        {'x': 5, 'y': 3}

        As said above, it asserts if  variables are
        lowercase; if not they'll be transformed
        automatically:

        It also converts the exponent in integer if
        it's a whole number

        >>> VariablesDict(c=9.0)
        {'c': 9}

        It can raise an error if:

        - variable's name is too long (ValueError)

        >>> VariablesDict(xy=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's name length must be one

        - variable's name is not alphabetical (ValueError)

        >>> VariablesDict(x2=9)
        Traceback (most recent call last):
        ...
        ValueError: variable's name must be alphabetical

        - exponent is not int (or a whole number) (TypeError)

        >>> VariablesDict(k=[])
        Traceback (most recent call last):
        ...
        TypeError: variable's exponent must be int

        - exponent is not a whole number (TypeError)

        >>> VariablesDict(z=7.13)
        Traceback (most recent call last):
        ...
        TypeError: variable's exponent must be a whole number

        - exponent is negative (ValueError)

        >>> VariablesDict(f=-3)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive


        After that, it checks if the dictionary is empty:

        >>> VariablesDict(a=2, b=8, c=3).is_empty
        False
        >>> VariablesDict(x=0).is_empty
        True

        :raise: TypeError, ValueError
        """

        # look for variables
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
                raise TypeError("variable's exponent must be int")
            elif isinstance(value, float) and not value.is_integer():
                raise TypeError("variable's exponent must be a whole number")
            elif value < 0:
                raise ValueError("variable's exponent must be positive")

            if not value == 0:
                new_variables[key.lower()] = int(value)

        super().__init__(new_variables)

        # Check if it's empty
        self.is_empty = not bool(len(self))

    ###  Item storing ###

    def __setitem__(self, key, value):
        """
        Raises AttributeError: VariablesDict is immutable

        :raise: AttributeError
        """

        raise AttributeError("VariablesDict is immutable")

    def __delitem__(self, key):
        """
        Raises AttributeError: VariablesDict is immutable

        :raise: AttributeError
        """

        raise AttributeError("VariablesDict is immutable")

    def pop(self, key):
        """
        Raises AttributeError: VariablesDict is immutable

        :raise: AttributeError
        """

        raise AttributeError("VariablesDict is immutable")

    def clear(self):
        """
        Raises AttributeError: VariablesDict is immutable

        :raise: AttributeError
        """

        raise AttributeError("VariablesDict is immutable")

    def __getitem__(self, key):
        """
        Gets the exponent of a variable from the variable's name

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

    ### Representation ###

    def __str__(self):
        """
        Returns the dict as a string (as a normal dict)

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
        Returns the dict as a string

        >>> repr(VariablesDict(Y=5))
        "{'y': 5}"

        For more informations see :func:`VariablesDict.__str__()`.

        :rtype: str
        """

        return self.__str__()

    ### Operations Methods ###

    def __add__(self, other):
        """
        Sums two VariablesDict, returning a VariablesDict
        whose exponents are the sum of the starting VariablesDicts' ones

        >>> VariablesDict(x=5, y=3) + VariablesDict(y=5)
        {'x': 5, 'y': 8}
        >>> VariablesDict(x=18) + VariablesDict(y=4)
        {'x': 18, 'y': 4}
        >>> VariablesDict(a=36) + VariablesDict()
        {'a': 36}

        If the second operator isn't a VariablesDict it will
        raise a TypeError

        >>> VariablesDict() + "-"
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for +: 'VariablesDict' and 'str'

        :type other: VariablesDict
        :rtype: VariablesDict
        :raise: TypeError
        """

        # check if other is a VariablesDict
        if not isinstance(other, VariablesDict):
            raise TypeError(f"unsupported operand type(s) for +: 'VariablesDict' and '{other.__class__.__name__}'")

        result = {}

        # sum the variables' exponents
        for variable in set(self) | set(other):
            result[variable] = self[variable] + other[variable]

        return VariablesDict(result)

    def __sub__(self, other):
        """
        Return a VariablesDict whose values are the difference
        between the starting VariablesDicts' ones

        >>> VariablesDict(x=5, y=3) - VariablesDict(x=1, y=2)
        {'x': 4, 'y': 1}
        >>> VariablesDict(x=18) - VariablesDict(x=18)
        {}

        If any exponent becomes negative, a ValueError
        will be raised instead:

        >>> VariablesDict(c=2) - VariablesDict(c=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive

        It can raise a TypeError if the second argument
        isn't a VariablesDict

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

        # compute difference
        for variable in set(self) | set(other):
            result[variable] = self[variable] - other[variable]

        return VariablesDict(result)

    def __mul__ (self, other):
        """
        Returns a VariablesDict whose exponents are
        this one's, but multiplied by a given (integer)
        number

        >>> VariablesDict(a=2, b= 5) * 3
        {'a': 6, 'b': 15}

        If the number is negative, a ValueError is
        raised

        >>> VariablesDict() * (-15)
        Traceback (most recent call last):
        ...
        ValueError: can't multiply a VariablesDict by a negative number

        If `other` is not an integer, a TypeError is raised

        >>> VariablesDict() * {}
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for *: 'VariablesDict' and 'dict'

        :type other: int
        :rtype: VariablesDict
        :raise: TypeError, ValueError
        """

        # check other's type
        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for *: 'VariablesDict' and '{other.__class__.__name__}'")
        elif other < 0:
            raise ValueError("can't multiply a VariablesDict by a negative number")

        variables = {}

        # multiply exponents
        for variable in self:
            variables[variable] = self[variable] * other

        return VariablesDict(variables)

    def __truediv__ (self, other):
        """
        Returns a VariablesDict whose values are
        this one's, but divided by a given (integer)
        number

        >>> VariablesDict(a=4, b=2) / 2
        {'a': 2, 'b': 1}

        If the VariableDict is not divisible
        by the given number, it will raise a ValueError

        >>> VariablesDict(x=7) / 3
        Traceback (most recent call last):
        ...
        ValueError: can't divide this VariablesDict by 3

        To see if a VariablesDict is divisible by a number,
        you can use modulus operator (see more at :func:`VariablesDict.__mod__()`):

        >>> VariablesDict(x=7) % 3
        False

        If `other` is not an integer, it will raise a TypeError

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
            raise ValueError(f"can't divide this VariablesDict by {other}")

        return VariablesDict(dict(map(lambda k: (k, self[k] / other), self)))

    def __mod__ (self, other):
        """
        Checks if the VariablesDict can be divided by a number
        (True => can be divided by `other`).

        >>> VariablesDict(a=2, b=4) % 2
        True
        >>> VariablesDict(a=2, b=4) % 3
        False

        It raises a TypeError when `other` is not
        an integer

        >>> VariablesDict(k=2) % []
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for %: 'VariablesDict' and 'list'

        Or ValueError when it isn't positive

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
        Returns the hash of the VariablesDict.
        It's equal to the tuple of its items.

        >>> hash(VariablesDict(x=2)) == hash((('x', 2),))
        True

        :rtype: int
        """

        return hash(tuple(list((k, self[k]) for k in sorted(self.keys()))))
