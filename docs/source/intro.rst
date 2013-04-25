Intended Audience
=================

pyplates are intended to be used with the `Amazon Web Services CloudFormation
<https://aws.amazon.com/cloudformation/>`_ service. If you're already a
CloudFormation (CFN) user, chances are good that you've already come up with
fun and interesting ways of generating valid CFN templates. pyplates are a
way to make those templates while leveraging all of the power that the python
environment has to offer.

Features
========

- Allows for easy customization of templates at runtime, allowing one
  pyplate to describe all of your CFN Stack roles (production, testing,
  dev, staging, etc).
- Supports all required elements of a CFN template, such as Parameters,
  Resources, Outputs, etc.)
- Supports all intrinsic CFN functions, such as base64, get_att, ref,
  etc.
- Converts intuitiviely-written python dictionaries into JSON templates,
  without having to worry about nesting or order-of-operations issues.

So, what is a pyplate?
======================

A pyplate is a class-based python representation of a JSON CloudFormation
template and resources, with
the goal of generating cloudformation templates based on input python
templates (pyplates!) the reflect the cloudformation template resource
hierarchy.

Currently, there is no support for specific resource types in the pyplate, so
they've all got to be written out. This will hopefully change as time goes on
and the entire template reference can be implemented in python, but for now
it's quite simple to create resources in the "long" form.

You **can** do this::

    cft = CloudFormationTemplate()
    cft.resources.app_server = Resource('AppServer', 'AWS::EC2::Instance', properties)

You can also do this, if you're feeling dictionaryriffic::

    cft.resources['AppServer'] = {
        'Type': 'AWS::EC2::Instance',
        'Properties': properties
    }

But you can't do this (yet)::

    cft.resources.app_server = resources.aws.ec2.instance('AppServer', properties)

