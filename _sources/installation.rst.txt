Installation
============

To install the example, ensure that you have Python version 3.11 or higher.

From PyPI
---------

.. code-block:: bash

    $ pip install pyml-regression-example2


From GitHub
-----------

* Download the git source:

.. code-block:: bash

    $ git clone --depth=1 https://github.com/hakonhagland/pyml-regression-example2.git
    $ cd pyml-regression-example2
    $ python -m venv .venv  # optionally create venv
    $ source .venv/bin/activate
    $ pip install .
    $ source shell_completion/bash.sh   # On Linux/macOS: optionally enable shell completion

.. note::
    On Windows (powershell) type ``.\.venv\Scripts\Activate.ps1`` to activate the venv

.. note::
    For development installation from GitHub see: :doc:`Development <development>`

* Verify that the installation was successful:

.. code-block:: bash

    $ housing-prices --help
