======================================
Creating a CFN Template using Pyplates
======================================

As simple as it gets
====================

Here's an example of the simplest pyplate you can make, which is one that defines a CloudFormationTemplate, and then adds one Resource to it. Let's say that this is "template.py" (a.k.a python template; a.k.a pyplate!)

CloudFormation won't let you make a stack with no Resources, so this template needs one. Notice how cft.resources is already there for you. In addition to
CloudFormationTemplate, common things that you'll need are available right
now without having to import them, including classes like Resource and
Properties, as well as all of the intrinsic functions such as ref and
base64.

You can see what the required properties of an AWS::EC2::Instance are here:

http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html

.. rubric:: template.py
.. literalinclude:: examples/simple/template.py

Now, on the command-line, we run ``cfn_py_generate template.py out.json``. Here's what out.json looks like:

.. rubric:: out.json
.. literalinclude:: examples/simple/out.json
    :language: json

Upload that to CloudFormation to have it make you a stack of one unnamed instance.

But now let's do something useful
=================================

Okay, we've made an instance! It would be nice to actually hand it a user-data script, though. There are a few ways to go about that. Fortunately, the pyplate is written in python, and we can anything that python can do.

.. note::

    Properties args can be either a 'Properties' object, or just a plain
    old python dict. For this example, we'll use a dict, but either way works.

.. rubric:: template.py
.. literalinclude:: examples/useful/template.py

Alternatively, because this is python, you could put the userdata
script in its own file, and read it in using normal file operations::

    user_data_script = open('userdata.sh').read()

The output certainly makes a mess of the script file, but that's really a discussion between the JSON serializer and CloudFormation that we don't need to worry ourselves with. After, we're here because making proper JSON is not a task for a human. Writing python is much more appropriate.

``cfn_py_generate template.py out.json``

.. rubric:: out.json
.. literalinclude:: examples/useful/out.json
    :language: json

Adding Metadata and Other Attributes to Resources
=================================================
Cloudformation provides extensive support for Metadata that may be used to associate structured data with a resource.

.. note::

    AWS CloudFormation does not validate the JSON in the Metadata attribute.


Adding Metadata to an S3 bucket
-------------------------------

.. rubric:: s3.py
.. literalinclude:: examples/resource_attributes/s3.py

.. rubric:: out.json
.. literalinclude:: examples/resource_attributes/s3.json
    :language: json

Adding Metadata to an EC2 instance
----------------------------------

.. rubric:: ec2_instance.py
.. literalinclude:: examples/resource_attributes/ec2_instance.py

.. rubric:: out.json
.. literalinclude:: examples/resource_attributes/ec2_instance.json
    :language: json

Practical Metadata example for bootstrapping an instance
--------------------------------------------------------

.. rubric:: ec2_instance_attribs.py
.. literalinclude:: examples/resource_attributes/ec2_instance_attribs.py

.. rubric:: out.json
.. literalinclude:: examples/resource_attributes/ec2_instance_attribs.json
    :language: json


Referencing Other Template Objects
==================================

This is where things start to really come together.
The instrinsic functions :func:`ref <cfn_pyplates.functions.ref>` and :func:`get_att <cfn_pyplates.functions.get_att>` are critical tools for getting the
most out of CloudFormation templates.

What if you're using CloudFormation to describe a stack of Resources, but the
goal is to try a bunch of different AMIs? Entering the AMIs at stack creation
is a good way to tackle that situation, and parameters are how you do it. Use ``ref``
to refer to the parameter from the Instance properties.

While we're here, we'd also like to prompt the user for what instance type
they'd like to spawn, as well as a friendly name to put on the instance for
EC2 API tools, like the AWS Console. These are also good uses for ``ref``

We also want to put the instance's DNS name in the stack outputs so we see it when using CFN API tools, and maybe act on it with some automation later. In this case, ``get_att`` is right for the job.

Here are some examples:

.. rubric:: template.py
.. literalinclude:: examples/ref/template.py
    :emphasize-lines: 28,29,31,37

``cfn_py_generate template.py out.json``

.. rubric:: out.json
.. literalinclude:: examples/ref/out.json
    :language: json
    :emphasize-lines: 28,34,37,46

Using the Options Mapping
=========================

In the introduction, there was some talk of using one pyplate to easily
describe similar stacks. For example, let's say you have a static website
being hosted on any number instances running in an auto scaling group
behind a load balancer. This website has a few known roles, including
development, testing, and production.

Using the options mapping, you can specify different options for each of
those roles, and then plug them into the pyplate when the stack template is
generated, giving you a custom template for each stack role.

Options mappins are defined in :doc:`YAML <why_yaml>`. Here are some examples
of the options for each stack role:

.. rubric:: mappings/development.yaml
.. literalinclude:: examples/options/mappings/development.yaml

.. rubric:: mappings/testing.yaml
.. literalinclude:: examples/options/mappings/testing.yaml

.. rubric:: mappings/production.yaml
.. literalinclude:: examples/options/mappings/production.yaml

And here's the pyplate:

.. toctree::

    examples/options/template

Notice that 'ImageId' is absent from the development options mapping. This
will trigger a prompt for the user to fill in the blanks. This does two things:

- It gives you the ability to easily add options at runtime where appropriate
- It helps you spot typos in options names

In our case, the former reason is what we're after. Our developers love to boot
all sorts of different AMIs and mess around, so it's easiest just to put in a
new ID every time we generate a template. Here's what that prompt looks like::

    Key "ImageId" not found in the supplied options mapping.
    You can enter it now (or leave blank for None/null):
    >

Generate the development template:

- ``cfn_py_generate template.py development.json -o mappings/development.yaml``

The ami flavor du jour is ``ami-deadbeef``, which I entered in the prompt. You
can see how it was inserted into the development.json below.

Now, generate a new stack template based on each remaining role:

- ``cfn_py_generate template.py testing.json -o mappings/testing.yaml``
- ``cfn_py_generate template.py production.json -o mappings/production.yaml``


And here are the generated templates for CloudFormation:

.. toctree::

    examples/options/development
    examples/options/testing
    examples/options/production

Go forth, and pyplate
=====================

As you can see, things with pyplates can escalate quickly. Fortunately, with
the help of the python interpreter, a little bit of YAML, and CloudFormation
itself, crazy templates like the above don't have to be written purely in
JSON, with no comments.

See any room for improvement? Fork this on GitHub!

https://github.com/seandst/cfn-pyplates
