__author__ = 'yoshi.miyamoto'


class _const(object):
    class ConstError(TypeError):pass

    def __setattr__(self, name, value):
        if self.__dict__. has_key(name):
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value


import sys

sys.modules[__name__] = _const()