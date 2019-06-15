from .monomials import Monomial

from collections import Counter


class Polynomial:
    def __init__(self, *terms):
        """
        Initialize the polynomial

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> print(p)
        5xy -3yz +a^4b

        This method calculate also the degree of the
        polynomial, the degree for each letter

        >>> p.degree
        5
        >>> p.degrees["z"]
        1

        :param *terms: The terms of the polynomial
        :type *terms: Monomials
        :raise: TypeError
        """

        self.terms = [*terms]
        self.reduce()

        # Add polynomial degrees
        self.degree = max(m.degree for m in self.terms)

        # Calculate the degree for each letter
        self.degrees = {}
        letters = set()
        for m in self.terms:  # Find all the letters
            letters |= set(m.degrees.keys())
        for l in letters:  # Calculate its degree
            self.degrees[l] = max(m.degrees[l] for m in self.terms)

    ### Utility Methods ###

    def reduce(self):
        """
        Sum all the simil monomials, so reduce the polynomial.
        This method is automatically called by the __init__
        method.

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'x'])
        >>> m3 = Monomial(variables=['x', 'y'])
        >>> p = Polynomial(m1, m2, m3) 
        >>> # p should be 5xy -3xy +xy, but
        >>> # reduce method reduced it as...
        >>> print(p)
        3xy
        """

        variables = [tuple(m.variables) for m in self.terms]

        # Check if there are simil monomial
        if not (len(set(variables)) == len(variables)):

            # If there are some, sum them
            terms_counter = Counter()
            for t in self.terms:
                terms_counter[' '.join(t.variables)] += t.coefficient

            # And rewrite the terms
            self.terms.clear()
            for v in terms_counter:
                self.terms.append(Monomial(
                    terms_counter[v], v.split(" ")))

    ### Operations Methods ###

    def __add__(self, other):
        """
        Add two polynomials or a polynomial and
        a monomial

        >>> m1 = Monomial(17, ['x', 'y'])
        >>> m2 = Monomial(-3, ['x', 'y'])
        >>> m3 = Monomial(-2, ['x'])
        >>> m4 = Monomial(5, ['x', 'y^3'])
        >>> m5 = Monomial(0, ['x'])

        >>> p1 = Polynomial(m1, m3)
        >>> p2 = Polynomial(m2, m4)

        >>> print(p1 + p2) # polynomial + polynomial
        14xy -2x +5xy^3

        >>> print(p1 + m5) # polynomial + monomial
        17xy -2x

        :type other: Monomial or Polynomial
        :rtype: Polynomial
        :raise: TypeError
        """

        # polynomial
        if isinstance(other, type(self)):
            return Polynomial(*self.terms, *other.terms)

        # monomial
        elif isinstance(other, Monomial):
            return Polynomial(*self.terms, other)

        else:
            raise TypeError("unsupported operand type(s) for +:"
                            f"'Polynomial' and '{type(other).__name__}'")

    def __sub__(self, other):
        """
        Subtract two polynomials or a monomial from
        a polynomial

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['x', 'y'])
        >>> m3 = Monomial(-2, ['x'])
        >>> m4 = Monomial(14, ['x', 'y^3'])
        >>> m5 = Monomial(0, ['x'])

        >>> p1 = Polynomial(m1, m3)
        >>> p2 = Polynomial(m2, m4)

        >>> print(p1 - p2) # polynomial - polynomial
        8xy -2x -14xy^3

        >>> print(p1 - m5) # polynomial - monomial
        5xy -2x

        :type other: Monomial or Polynomial
        :rtype: Polynomial
        :raise: TypeError
        """

        # polynomial
        if isinstance(other, type(self)):
            other = list(map(lambda m: -m, other))
            return Polynomial(*self.terms, *other)

        # monomial
        elif isinstance(other, Monomial):
            return Polynomial(*self.terms, -other)

        else:
            raise TypeError("unsupported operand type(s) for -:"
                            f"'Polynomial' and '{type(other).__name__}'")

    def __mul__(self, other):
        """
        Multiply two polynomials, a polynomial and a
        monomial or a polynomial and a number (int/float)

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['x', 'y'])
        >>> m3 = Monomial(-2, ['x'])
        >>> m4 = Monomial(14, ['x', 'y^3'])

        >>> p1 = Polynomial(m1, m3)
        >>> p2 = Polynomial(m2, m4)

        >>> print(p1 * p2) # polynomial * polynomial
        -15x^2y^2 +70x^2y^4 +6x^2y -28x^2y^3

        >>> print(p1 * m4) # polynomial * monomial
        70x^2y^4 -28x^2y^3

        >>> print(p1 * 4) # polynomial * number
        20xy -8x

        :type other: Monomial, Polynomial, int or float
        :rtype: Polynomial
        :raise: TypeError
        """

        # monomial
        if isinstance(other, Monomial):
            return Polynomial(*(t*other for t in self.terms))

        # polynomial
        elif isinstance(other, type(self)):
            return Polynomial(*(a*b for a in self.terms for b in other.terms))

        # int or float
        elif isinstance(other, int) or isinstance(other, float):
            return Polynomial(*(t*other for t in self.terms))

        else:
            raise TypeError("unsupported operand type(s) for *:"
                            f"'Polynomial' and '{type(other).__name__}'")

    ### Magic Methods ###

    def __str__(self):
        """
        Return the polynomial as a string, adding
        a space between each term

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> str(p)
        '5xy -3yz +a^4b'
        """
        result = str(self.terms[0])
        for t in self.terms[1:]:
            if t.coefficient > 0:
                result += f" +{t}"
            elif t.coefficient < 0:
                result += f" {t}"
        return result

    def __iter__(self):
        """
        Return the iterator for the polynomial.
        The iteration will iter over the polynomial's
        terms. As a magic method, you can access it
        calling the iter() function with the polynomial
        as argument

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> i = iter(p)
        >>> # see __next__ for the next part
        """
        self._iter_n = -1
        return self

    def __next__(self):
        """
        The next magic method (to use with iter)
        returns the next terms of the polynomials
        itered. When it's finished, it raise StopIteration

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> i = iter(p)
        >>> print(next(i))
        5xy
        >>> print(next(i))
        -3yz
        >>> print(next(i))
        a^4b
        >>> next(i) # no more terms
        Traceback (most recent call last):
        ...
        StopIteration
        """

        self._iter_n += 1
        if self._iter_n <= len(self.terms) - 1:
            return self.terms[self._iter_n]
        else:
            raise StopIteration

    def __getitem__(self, key):
        """
        Enable the indexing of polynomial's terms.

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(variables=['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> print(p[0])
        5xy
        >>> print(p[1])
        -3yz

        Also negative indexing is enabled:

        >>> print(p[-1])
        a^4b

        :raise: IndexError, TypeError
        """
        return self.terms[key]

    def __eq__(self, other):
        """
        Check if two polynomials are equivalent,
        comparating each term

        >>> m1 = Monomial(14, ["a"])
        >>> m2 = Monomial(14, ["a^2"])
        >>> Polynomial(m1, m2) == Polynomial(m1, m2)
        True
        >>> Polynomial(m1, m2) == Polynomial(m1)
        False

        If a polynomial has a single term, it can
        also be compared to a monomial
        >>> Polynomial(m1) == m1
        True

        Otherwise, the result will be False
        >>> Polynomial(m1, m2) == m1
        False

        :type other: Polynomial, Monomial
        :rtype: bool
        """

        # polynomial == polynomial
        if type(other) == type(self):
            if not len(self) == len(other):
                return False
            else:
                def _sort(p): return sorted(p, key=lambda m: m.coefficient)
                p1 = _sort(self)
                p2 = _sort(other)
                return all(p1[i] == p2[i] for i in range(len(p1)))

        # polynomial (1 term) == monomial
        elif isinstance(other, Monomial) and len(self) == 1:
            return self[0] == other

        else:
            return False

    def __neg__(self):
        """
        Return the opposite of the polynomial,
        changing the sign at all it's terms:

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(15, ['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> print(-p)
        -5xy +3yz -15a^4b

        :rtype: Polynomial
        """
        return Polynomial(*(-m for m in self))

    def __len__(self):
        """
        Return the number of terms of the
        polynomial

        >>> m1 = Monomial(5, ['x', 'y'])
        >>> m2 = Monomial(-3, ['y', 'z'])
        >>> m3 = Monomial(15, ['a^4', 'b'])
        >>> p = Polynomial(m1, m2, m3)
        >>> print(len(p))
        3

        :rtype: int
        """
        return len(self.terms)
