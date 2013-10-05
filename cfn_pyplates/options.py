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

from collections import defaultdict

prompt_str = '''Key "{0}" not found in the supplied options mapping.
You can enter it now (or leave blank for None/null):
> '''


class OptionsMapping(defaultdict):
    def __init__(self, *args, **kwargs):
        super(OptionsMapping, self).__init__(None, *args, **kwargs)

    def __missing__(self, key):
        try:
            value = raw_input(prompt_str.format(key))
        except KeyboardInterrupt:
            # Catch the sigint here, since the user's pretty likely to
            # Ctrl-C and go fix the options mapping input file
            raise SystemExit

        if not value:
            value = None

        self[key] = value
        return value
