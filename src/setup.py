from setuptools import setup
from json import load

readme = """
# Ruffini

To see the documentation, please [click here](https://gianluparri03.github.io/ruffini).
You can find the documentation for this project in
[Read The Docs website](https://ruffini.readthedocs.io/en/stable/).

Instead, if you want to see the source, [click here](https://github.com/gianluparri03/ruffini).
If you want to see the source, [click here](https://github.com/gianluparri03/ruffini).
"""

with open("config.json") as f:
    version = load(f)["version"]

setup(
    name="ruffini",
    version=version,
    description="Monomials, Polynomials and lot more!",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Gianluca Parri",
    author_email="gianlucaparri03@gmail.com",
    url="https://github.com/gianluparri03/ruffini",
    packages=["ruffini"],
    license="MIT",
)
