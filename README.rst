============
cfn-pyplates
============

Amazon Web Services CloudFormation templates, generated with Python!

.. image:: https://travis-ci.org/seandst/cfn-pyplates.png
    :target: https://travis-ci.org/seandst/cfn-pyplates/

Where to get it
===============

- https://pypi.python.org/pypi/cfn-pyplates/
- easy_install cfn-pyplates
- pip install cfn-pyplates

Doumentation
============

- https://cfn-pyplates.readthedocs.org/

Intended Audience
=================

pyplates are intended to be used with the `Amazon Web Services CloudFormation
<https://aws.amazon.com/cloudformation/>`_ service. If you're already a
CloudFormation (CFN) user, chances are good that you've already come up with
fun and interesting ways of generating valid CFN templates. pyplates are a
way to make those templates while leveraging all of the power that the python
environment has to offer.

What is a pyplate?
==================

A pyplate is a class-based python representation of a JSON CloudFormation
template and resources, with the goal of generating cloudformation
templates based on input python templates (pyplates!) that reflect the
cloudformation template hierarchy.

Why this fork?
==============

We had some changes we wanted to make and have made these in this fork with
the intention of passing them up stream through PRs when such changes are
aligned with the interests of the upstream authors.

We will seek to bring upstream changes into this branch regularly.

Features
========

- Allows for easy customization of templates at runtime, allowing one
  pyplate to describe all of your CFN Stack roles (production, testing,
  dev, staging, etc).
- Lets you put comments right in the template!
- Supports all required elements of a CFN template, such as Parameters,
  Resources, Outputs, etc.)
- Supports all intrinsic CFN functions, such as base64, get_att, ref,
  etc.
- Converts intuitiviely-written python dictionaries into JSON templates,
  without having to worry about nesting or order-of-operations issues.

RTL Features
============

- Allows templating of scripts to be included in UserData arguments etc
  using Jinja2. Features allow natural creation of templates that translate
  to the appropriate format for inclusion in a Cloudformation template.
