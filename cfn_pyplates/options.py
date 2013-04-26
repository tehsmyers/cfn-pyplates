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
