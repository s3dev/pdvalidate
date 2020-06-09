Release checklist
=================

Things to remember when making a new release of pdvalidate.

#.  Changes should be made to some branch other than master (a pull request
    should then be created before making the release).

#.  Make desirable changes to the code.

#.  Check coding style against some of the conventions in PEP8:

    .. code-block:: none

        $ pylint *.py

#.  Run tests and report coverage:

    .. code-block:: none

        $ pytest -v test_validation.py
        $ coverage run -m pytest test_validation.py
        $ coverage report -m ./pdvalidate/validation.py

#.  Update ``README.rst`` and the documentation (in ``docs/``).

    .. code-block:: none

        $ sphinx-build -b html ./docs/source ./docs/_build/html

#.  Update ``CHANGELOG.rst`` and add a release date.

#.  Update the release (version) number in ``_version.py`` and
    ``validation.py``. Use the standard ``major.minor.revision`` 
    convention. Note: A development version such as x.y.z.dev1 is 
    acceptable.

#.  Create pull request(s) with changes for the new release.

#.  Create distributions and upload the files to
    `PyPI <https://pypi.org>`_ with
    `twine <https://github.com/pypa/twine>`_.

    .. code-block:: none

        $ python setup.py sdist bdist_wheel --universal
        $ twine upload dist/*

#.  Create the new release in GitHub.

#.  Trigger a new build (latest version) of the documentation on
    `<http://readthedocs.io>`_.
