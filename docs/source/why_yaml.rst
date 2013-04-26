Why use YAML for Options Mappings?
==================================

YAML's killer feature is that it allows comments alongside your config
entries. When the options mapping is deciding critical things in your
pyplate, it's nice to be able to explain why something is one way and not
another. For example:

.. code-block:: yaml

    # The task scheduler breaks if more than one instance spawns right now
    # We're working on it in ticket #1234, but for now just cap the group at 1
    TaskSchedulerAutoScalingMaxSize: 1

In addition to comments, breaking options out into the mapping mean that
you can potentially spend less time in the pyplate itself by implementing
branching logic based on keys in the options mapping.

Earlier drafts of cfn-pyplates used JSON for the options mapping, but
despite JSON's already lightweight markup compared to something like XML,
nothing beats YAML for its simplicity and content/markup ratio.

.. rubric:: See Also

- http://yaml.org
- http://en.wikipedia.org/wiki/YAML

