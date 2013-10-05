====================
Developer Guidelines
====================

Pull Requests
=============

Pull requests should:

* Conform to existing style in the project
* Add documentation for new functionality, where applicable
* Add unit test coverage for new functionality, where applicable
* :ref:`Lint the code <linting>`

.. _linting:

Linting
=======

This project adheres to just about everything in PEP8, with the exception of
line length restrictions and some specifics around indentation.

Line Length
-----------

Since the primary mechanism for code submission and review is GitHub, we're
allowed a little more freedom with regard to line length. The GitHub review
panel is 100 characters wide, so the max line length for this project is
similarly 100 characters.

Block Indentation
-----------------

PEP8 does account for indentation of multi-line block statements, but only
"officially" supports the following:

.. code-block:: python

   def a_very_long_function_name_that_takes_a_lot_of_arguments(will, need,
                                                               to, be,
                                                               indented,
                                                               like, this)

or...

.. code-block:: python

   def a_very_long_function_name_that_takes_a_lot_of_arguments(
           will, need, to, be, indented, like, this)

This would normally be disallowed, but can lead to better looking and more
compact (but still quite readable) code:

.. code-block:: python

   def a_very_long_function_name_that_takes_a_lot_of_arguments(will, need
           to, be, indented, like, this)
       # Note the two indents on the second line of the block statement,
       # which clearly separates the block statement from the trailing
       # code.

Flake8
------

Flake8 is an excellent tool for basic code linting to check for adherence
to style. It can be installed with ``pip`` or ``easy_install``.

An example flake8.conf, reflecting this project's specific exceptions to
PEP8:

.. code-block:: none

   [flake8]
   ignore = E128
   max-line-length = 100

Releases
========

Before posting a release
------------------------

* Ensure that tests pass on your local machine, and after pushing ensure
  that the tests pass in the continuous integration system.
* Ensure that the sphinx docs can be generated without error (preferably
  without any warnings, too)
* Create a source distribution with `python setup.py sdist`. Install that
  source distribution into a newly created virtualenv (or other "clean"
  environment), verify that it installs properly
* Create and tag a release commit, with changes listed. The tagging format
  is 'v$VERSION', where $VERSION is the version string from
  ``cfn_pyplates/__init__.py``.

Versions
--------

This project adheres to Semantic Versioning. During the beta period, the
*x* (major) version number is 0, and the *y* and *z* versions are intended
to represent what the *x* and *y* numbers would mean, respectively.

Thus, with the *x* version set to 0, incrementing the *y* version signals
possible backward-incompatible API changes that will require dependent code
changes, while incrementing the *z* version signals backward-compatible
changes, either new functionality in the API, bug fixes, or general
improvements.

.. seealso::


   PEP 8
       http://www.python.org/dev/peps/pep-0008/
   Semantic Versioning
       http://semver.org/
