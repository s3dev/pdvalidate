Release checklist
=================

Things to remember when making a new release of pandas-validation.

#.  Changes should be made to some branch other than master (a pull request should then be created before making the release).

#.  Update the release (version) numbers in *setup.py* and *pandasvalidation.py*.

#.  Make desirable changes to the code.

#.  Run tests with PEP8 check and report coverage:

    .. code-block:: bash

    $ py.test -v --pep8 pandasvalidation.py
    $ coverage run -m py.test
    $ coverage report --include pandasvalidation.py -m

#.  Update *README.rst* and the documentation (in `docs/`).

    .. code-block:: bash

    $ sphinx-build -b html ./docs/source ./docs/_build/html

#.  Update *CHANGELOG.rst*.

#.  Create pull request(s) with changes for the new release.

#.  Create the new release in GitHub.

#.  Create distributions and upload the files to `PyPI <https://pypi.python.org/pypi>`_.

    .. code-block:: bash

    $ python setup.py bdist_wheel --universal
    $ python setup.py sdist
