Suggesting changes to the code
==============================

Suggestions for improvements are very welcome. Use the
`GitHub issue tracker <https://github.com/hakonhagland/pyml-regression-example2/issues>`_
or submit a pull request.

Pull request
------------

To set up an environment for developing and submitting a pull request:

* Install `uv <https://docs.astral.sh/uv/>`_ using e.g. ``pipx install uv``

* Then, from the root directory of this repository:

.. code-block:: bash

    $ uv venv
    $ uv pip install -e .
    $ source .venv/bin/activate

* Now you can:

   * run ``make test`` to run the test suite
   * run ``pre-commit install`` to install the pre-commit hooks
   * run ``make coverage`` to run unit tests and generate coverage report
   * run ``make ruff-check`` to check the code with ruff
   * run ``make mypy`` to check the code with mypy
