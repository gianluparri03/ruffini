from setuptools import setup

with open("../README.md") as f:
    readme = f.read()

version = "v1.4_wip"

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
