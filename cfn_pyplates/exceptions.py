# Copyright (c) 2013 MetaMetrics, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.


class Error(Exception):
    """Base exception class for cfn_pyplates

    A namespaced Exception subclass with explicit 'message' support.
    Will be handled at template generation, with the message being delivered
    to the user.

    Args:
        message: An optional message to package with the Error
        args: Any number of optional arguments, to be used as subclasses
            see fit.

    """

    message = 'An unknown error has occurred.'

    def __init__(self, message=None, *args):
        if not message:
            # This is a subclass, message is a static attr
            message = self.message
        else:
            # Error is being directly instantiated, set the message
            self.message = message
        self.args = (message,) + args


class AddRemoveError(Error):
    """Raised when attempting to attach weird things to a JSONableDict

    Weird things, in this case, mean anything that isn't a JSONableDict

    Args:
        message: An optional message to package with the Error

    """

    message = 'Only subclasses of JSONableDict can be added or removed'


class IntrinsicFuncInputError(Error):
    """Raised when passing bad input values to an intrinsic function

    Args:
        message: An optional message to package with the Error

    """

    message = 'Invalid arguments passed to intrinsic function'
