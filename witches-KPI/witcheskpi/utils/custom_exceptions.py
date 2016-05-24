__author__ = 'yoshi.miyamoto'


class NoPurchaseFoundException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(NoPurchaseFoundException, self).__init__(message)