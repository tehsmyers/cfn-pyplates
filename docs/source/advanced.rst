==============
Advanced Usage
==============

Refactoring your pyplates
=========================

At some point, probably when you start managing multiple projects with pyplates or possibly
earlier if you have a penchant for clean code, you will want to be able to reuse your pyplates
definitions.  Fortunately, a pyplate is a standard python class, so refactoring is a relatively
straightforward matter of creating useful superclasses (with a few minor gotchas that are easy to
work around.

Defining the problem
--------------------

Let's say you have a pyplate that creates a stack with an EC2 instance and an S3 bucket.  It
might look like this:

.. rubric:: project.py
.. literalinclude:: examples/advanced/project_template.py

To begin our refactoring, we can begin by extracting resource creation into a subclass of
`CloudFormationTemplate`.

.. rubric:: refactored.py
.. literalinclude:: examples/advanced/refactored_template.py

We now instantiate ProjectTemplate instead of CloudFormationTemplate, and rather than
messing with a bunch of attributes on our pyplate instance, we just call cft.add_resources()
and we're done.

Solving the problem with reusable pyplates
------------------------------------------

This already looks nicer, but if we create a new project, we still have to copy and paste all
this code into a new pyplate.  We haven't saved any typing, and we haven't made refactoring any
easier.  For that, we need to pull common code into a module on our python path that all of our
projects can access.

As we do this, though, we lose access to all the all of the pre-existing variables that
pyplates give us.  We can import most of them from ``pyplates.core`` (``CloudFormationTemplate``,
``Resource``, ``Parameter``, ``Output``, and ``MetaData``) or ``pyplates.functions`` (``ref``,
``join``, ``get_att``, and ``base64``).  ``options`` is handled differently.  We need to pass
that in to our template explicitly as the second argument, after the description.  It will
then be available within the class as ``self.options``.

.. rubric:: basetemplate.py
.. literalinclude:: examples/advanced/base_template.py

We can now use this base template as a catalog of components that we might want to include in
our projects.  Projects can define their own subclasses and only use those components that are
relevant to them.

Our usual project's pyplate now looks like this:

.. rubric:: inheriting.py
.. literalinclude:: examples/advanced/inheriting_template.py

And if we want to create another project that requires an S3 bucket only, we can do so.  We
can even add a CORS configuration to this bucket while still leveraging the base template.
Our pyplate is really just a collection of dictionaries (JSONableDicts, technically), so all we
need to do is alter the right part of the dictionary using standard python.

.. rubric:: altered.py
.. literalinclude:: examples/advanced/altered_template.py

Going further
-------------

You may wish to go even further with your pyplate refactoring.  This is python, so anything is
possible.  You can build a collection of reusable tools to create various resource types, and
then build a an abstraction layer on top of that for creating related groups of resources that
work together, such as an SQS Queue and an IAM User and a set of permissions to allow the user
to access the queue.  You could build mixins to organize those functional abstractions.  You
could build a framework for dynamically managing resource dependencies.  The sky is the limit.
pyplates is deliberately kept simple, so that building on top of it is easy.

If you do find new ways to get more mileage out of your pyplates usage, please let us know.
We'd love to hear about it.

Generating Templates in Python
==============================

If you'd rather not use the CLI, then you can instead use some generation capabilities directly:

.. rubric:: callable_generate.py
.. literalinclude:: examples/advanced/callable_generate.py
