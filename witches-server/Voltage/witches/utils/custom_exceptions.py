__author__ = 'yoshi.miyamoto'


class NoValueFoundError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(NoValueFoundError, self).__init__(message)


class TooManyValueFoundError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(TooManyValueFoundError, self).__init__(message)


class BuildVersionFormatError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(BuildVersionFormatError, self).__init__(message)


class WrongValueError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(WrongValueError, self).__init__(message)


class ReceiptVerificationError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(ReceiptVerificationError, self).__init__(message)


class NegativeUserCurrentItemIndexError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super(NegativeUserCurrentItemIndexError, self).__init__(message)