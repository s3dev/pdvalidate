Release checklist
=================

Things to remember when making a new release of pandas-validation.

#.  Changes should be made to some branch other than master (a pull request
    should then be created before making the release).

#.  Make desirable changes to the code.

#.  Check coding style against some of the conventions in PEP8:

    .. code-block:: none

        $ cd pylintr
        $ ./pylintr.sh

#.  Run tests and report coverage:

    .. code-block:: none

        $ cd tests
        $ ./run.sh
        $ ./coverage.sh

#.  Update ``README.rst`` and the documentation (in ``docs/``).

    .. code-block:: none

        $ cd docs
        $ ./update.sh

#.  Update ``CHANGELOG.rst`` and add a release date.

#.  Update the release (version) number in ``_version.py``.

#.  Create pull request(s) with changes for the new release.

#.  Create distributions and upload the files to
    `PyPI <https://pypi.org>`_ with
    `twine <https://github.com/pypa/twine>`_.

    .. code-block:: none

        $ python setup.py sdist bdist_wheel --universal
        $ twine upload dist/*

    or create a local build by running the ``setup.sh`` script::

        $ ./setup.sh

#.  Create the new release in GitHub.

#.  Trigger a new build (latest version) of the documentation on
    `<http://readthedocs.io>`_.
