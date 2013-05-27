..
    This is copied into the README for displaying on github.
    Try to keep the two files in sync :\

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

