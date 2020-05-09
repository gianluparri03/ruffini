class VariablesDict:
    """
    A VariablesDict is a sort of dictionary with special
    features, created to manage the variables of a monomial.

    In this case, we'll call keys variables and
    values exponents.

    Its main features are:

    - A VariablesDict is immutable
    - The default exponent is 0; therefore, variables with exponent 0 aren't stored
    - Variables aren't case sensitive
    - Variables must be letters from the latin alphabet and one-character long
    - Exponents must be positive integer
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

        NB: Variables are sorted

        >>> VariablesDict(k=2, b=3)
        {'b': 3, 'k': 2}

        As said above, variables aren't case sensitive, so
        they're always made lowercase

        >>> VariablesDict(X=2)
        {'x': 2}

        It also converts the exponent in integer if it's a whole number

        >>> VariablesDict(x=3.0)
        {'x': 3}

        It can raise an error if:

        - `variable` is not a string

        >>> VariablesDict({9: 9})
        Traceback (most recent call last):
        ...
        TypeError: variable's name must be a string

        - `variable` is too long

        >>> VariablesDict(xy=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's name length must be one

        - `variable` is not alphabetical

        >>> VariablesDict(x2=9)
        Traceback (most recent call last):
        ...
        ValueError: variable's name must be alphabetical

        - `exponent` is not an integer (or a whole number)

        >>> VariablesDict(k=[])
        Traceback (most recent call last):
        ...
        TypeError: variable's exponent must be int

        >>> VariablesDict(z=7.13)
        Traceback (most recent call last):
        ...
        TypeError: variable's exponent must be a whole number

        - `exponent` is negative

        >>> VariablesDict(f=-3)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive


        It also checks if the dict is empty:

        >>> VariablesDict(a=2, b=8, c=3).is_empty
        False
        >>> VariablesDict(x=0).is_empty
        True

        :raise: TypeError, ValueError
        """

        # look for variables
        if not variables:
            variables = kwargs

        items = {}

        for variable, exponent in variables.items():
            # Check variable's name
            if not isinstance(variable, str):
                raise TypeError("variable's name must be a string")
            elif not variable.isalpha():
                raise ValueError("variable's name must be alphabetical")
            elif len(variable) > 1:
                raise ValueError("variable's name length must be one")

            # Check variable's exponent
            if not isinstance(exponent, (int, float)):
                raise TypeError("variable's exponent must be int")
            elif isinstance(exponent, float) and not exponent.is_integer():
                raise TypeError("variable's exponent must be a whole number")
            elif exponent < 0:
                raise ValueError("variable's exponent must be positive")

            # Add it to the items
            if not exponent == 0:
                items[variable.lower()] = int(exponent)

        # Set items
        self.__items = tuple(sorted((v, e) for v, e in items.items()))

        # Check if it's empty
        self.is_empty = not bool(len(self))

    ###  Items
    def __getitem__(self, variable):
        """
        Returns the exponent for the given variable

        >>> VariablesDict(a=2)['a']
        2

        It returns 0 if that variable does not exists

        >>> VariablesDict(a=2)['b']
        0

        It can return an error if:

        - `variable` is not a string

        >>> VariablesDict({9: 9})
        Traceback (most recent call last):
        ...
        TypeError: variable's name must be a string

        - `variable` is too long

        >>> VariablesDict(xy=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's name length must be one

        - `variable` is not alphabetical

        >>> VariablesDict(x2=9)
        Traceback (most recent call last):
        ...
        ValueError: variable's name must be alphabetical

        :type variable: string
        :rtype: int
        """

        # Check if kye is valid
        if not isinstance(variable, str):
            raise TypeError("variable's name must be a string")
        elif not variable.isalpha():
            raise ValueError("variable's name must be alphabetical")
        elif len(variable) > 1:
            raise ValueError("variable's name length must be one")

        variable = variable.lower()

        # Look if there is that variable in the dict
        for item in self.__items:
            if item[0] == variable:
                return item[1]

        # Otherwise return 0
        return 0

    def exponents(self):
        """
        Returns the exponents of the VariablesDict
        as a tuple

        >>> VariablesDict(a=2, b=3).exponents()
        (2, 3)

        :rtype: tuple
        """

        return tuple(item[1] for item in self.__items)

    def items(self):
        """
        Returns the pairs variable-exponent of the
        VariablesDict as a tuple of tuples

        >>> VariablesDict(a=2, b=3).items()
        (('a', 2), ('b', 3))

        :rtype: tuple
        """

        return self.__items

    def __iter__(self):
        """
        Returns the iterator of the VariablesDict

        >>> iter(VariablesDict(a=2, b=3))
        {'a': 2, 'b': 3}

        For more informations see :func:`VariablesDict.__next__()`.

        :rtype: VariablesDict
        """

        self.itern = 0
        return self

    def __next__(self):
        """
        Gets the next variable in the VariablesDict

        >>> i = iter(VariablesDict(a=2, b=3))
        >>> next(i)
        'a'
        >>> next(i)
        'b'
        >>> next(i)
        Traceback (most recent call last):
        ...
        StopIteration

        :rtype: str
        :raise: StopIteration
        """

        try:
            variable = self.__items[self.itern][0]
            self.itern += 1
            return variable
        except IndexError:
            raise StopIteration

    def __len__(self):
        """
        Returns the dict's len

        >>> len(VariablesDict(a=2, b=3))
        2

        :rtype: int
        """

        return len(self.__items)

    # Representation
    def __str__(self):
        """
        Returns the VariablesDict as a string, like a normal dict

        >>> str(VariablesDict(x=2, y=3))
        "{'x': 2, 'y': 3}"

        :rtype: str
        """

        return str({item[0]: item[1] for item in self.__items})

    def __repr__(self):
        """
        Returns the VariablesDict as a string

        >>> repr(VariablesDict(y=5))
        "{'y': 5}"

        For more informations see :func:`VariablesDict.__str__()`.

        :rtype: str
        """

        return self.__str__()

    # Operations
    def __add__(self, other):
        """
        Sums two VariablesDict, returning a VariablesDict
        whose exponents are the sum of the starting VariablesDicts' ones

        >>> VariablesDict(x=5, y=3) + VariablesDict(y=5)
        {'x': 5, 'y': 8}

        It raises a TypeError if `other` is not a VariablesDict

        >>> VariablesDict(x=1) + 3
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for +: 'VariablesDict' and 'int'

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

        If any exponent becomes negative, a ValueError
        will be raised instead:

        >>> VariablesDict(c=2) - VariablesDict(c=3)
        Traceback (most recent call last):
        ...
        ValueError: variable's exponent must be positive

        It raises a TypeError if `other` is not a VariablesDict

        >>> VariablesDict(x=1) - 3
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for -: 'VariablesDict' and 'int'

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
        this one's, multiplied by a given (integer) number

        >>> VariablesDict(a=2, b= 5) * 3
        {'a': 6, 'b': 15}

        If the number is negative, a ValueError is
        raised

        >>> VariablesDict() * (-15)
        Traceback (most recent call last):
        ...
        ValueError: can't multiply a VariablesDict by a negative number

        It raises a TypeError if `other` is not an integer

        >>> VariablesDict(x=1) * '3'
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for *: 'VariablesDict' and 'str'

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
        this one's divided by a given (integer) number

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

        It raises a TypeError if `other` is not an integer

        >>> VariablesDict(x=1) / '3'
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for /: 'VariablesDict' and 'str'

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

        It raises ValueError if `other` isn't a positive integer

        >>> VariablesDict(k=2) % (-7)
        Traceback (most recent call last):
        ...
        ValueError: can't use modulus with VariablesDict and negative numbers

        It raises a TypeError if `other` is not an integer

        >>> VariablesDict(x=1) % '3'
        Traceback (most recent call last):
        ...
        TypeError: unsupported operand type(s) for %: 'VariablesDict' and 'str'

        :type other: int
        :rtype: bool
        :raise: TypeError, ValueError
        """

        if not isinstance(other, int):
            raise TypeError(f"unsupported operand type(s) for %: 'VariablesDict' and '{other.__class__.__name__}'")
        elif other < 0:
            raise ValueError("can't use modulus with VariablesDict and negative numbers")

        return all(l % other == 0 for l in self.exponents())

    def __eq__(self, other):
        """
        Checks if two variablesDict are equivalent

        >>> VariablesDict(a=2, b=4) == VariablesDict(b=4, a=2)
        True

        If `other` is not a VariablesDict it always returns False

        >>> VariablesDict(a=2, b=4) == 3
        False

        :type other: VariablesDict
        :rtype: bool
        """

        if not isinstance(other, VariablesDict):
            return False

        return set(self.items()) == set(other.items())

    def __hash__(self):
        """
        Returns the hash of the VariablesDict by hashing
        the result of :func:`VariablesDict.items()`.

        :rtype: int
        """

        return hash(self.__items)

    def __bool__(self):
        """
        Returns the opposite of `is_empty`.

        >>> VariablesDict().is_empty
        True
        >>> bool(VariablesDict())
        False

        :rtype: int
        """

        return not self.is_empty
