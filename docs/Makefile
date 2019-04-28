# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = ruffini
SOURCEDIR     = rst
BUILDDIR      = build


clean:
	rm -rf _* *.js *.html

html:
	sphinx-build -b html source .
	rm -rf .doctrees
	rm .buildinfo objects.inv

apidoc:
	rm source/*.rst
	sphinx-apidoc -o source ../src/ruffini
	cp source/modules.rst source/index.rst

