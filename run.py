from monomials import Monomial

print("Some examples:")

a = Monomial(5, ["x", "y"])
b = Monomial(18, ["x", "y"])
c = Monomial(6, ["x^2", "y"])
d = Monomial(-1, ["y"])
e = Monomial(variables=["x", "y"])

print("Additions:")
print(f"{a} + {e} = ", a + e)
print(f"{b} + {a} = ", b + a)

print("\nSubtractions:")
print(f"{a} - {b} = ", a - b)
print(f"{b} - {e} = ", b - e)
print()

print("\nMultiplications:")
print(f"{e} * {c} = ", e * c)
print(f"{a} * {d} = ", a * d)
print()

print("\nDivisions:")
print(f"{b} / {a} = ", b / a)
print(f"{c} / {a} = ", c / a)
print()

print("\nPowers:")
print(f"{a} ** 2 = ", a ** 2)
print(f"{d} ** 3 = ", d ** 3)
