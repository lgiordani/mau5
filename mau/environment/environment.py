from .helpers import flatten_nested_dict, nest_flattened_dict


class Environment:
    """
    This is a class that hosts a nested configuration.

    An Environment contains a dictionary of
    configuration variables that can be queried using flat
    variable names like `a.b.c`.
    """

    def __init__(self):
        # This is the internal dictionary, which
        # is always kept in its flattened version.
        self._variables: dict = {}

    @classmethod
    def from_dict(cls, other: dict, namespace: str | None = None):
        env = cls()
        env.update(other, namespace)
        return env

    def update(self, other: dict, namespace: str | None = None):
        if namespace:
            other = {namespace: other}

        self._variables.update(flatten_nested_dict(other))

    def asdict(self):
        return nest_flattened_dict(self._variables)

    # def __eq__(self, other):
    #     return self._variables == other._variables

    # def clone(self):
    #     return self.from_dict(self._variables)

    def setvar(self, key, value):
        self.update({key: value})

    def getvar_nodefault(self, key):
        return self._variables[key]

    def getvar(self, key, default=None):
        try:
            return self._variables[key]
        except KeyError:
            prefix = f"{key}."

            keys = [k for k in self._variables if k.startswith(prefix)]

            if len(keys) != 0:
                return self.__class__.from_dict(
                    {
                        k.removeprefix(prefix): v
                        for k, v in self._variables.items()
                        if k.startswith(prefix)
                    }
                )

            return default
