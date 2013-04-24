class Error(Exception):
    message = ''

    def __init__(self, message=None, *args):
        if not message:
            message = self.message
        self.args = (message,) + args

class AddRemoveError(Error):
    message = 'Only subclasses of JSONableDict can be added or removed to this object.'
