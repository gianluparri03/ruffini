from setuptools import setup

readme = """
# Ruffini

To see the documentation, please [click here](https://gianluparri03.github.io/ruffini).

Instead, if you want to see the source, [click here](https://github.com/gianluparri03/ruffini).
"""

setup(
    name="ruffini",
    version="0.1",
    description="Monomials, Polynomials and lot more!",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Gianluca Parri",
    author_email="gianlucaparri03@gmail.com",
    url="https://github.com/gianluparri03/ruffini",
    packages=["ruffini"],
    license="MIT",
)
