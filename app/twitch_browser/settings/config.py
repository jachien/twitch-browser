# copied from http://www.tornadoweb.org/en/stable/_modules/tornado/util.html#ObjectDict

class Config(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value