import six
import inspect
import collections


def represent(item):
    if isinstance(item, six.text_type):
        return "'%s'" % item
    elif isinstance(item, (bytes, bytearray)):
        return repr(type(item))
    else:
        return repr(item)


def func_parameters(func, *args, **kwargs):
    """
    >>> def helper(func):
    ...     def wrapper(*args, **kwargs):
    ...         params = func_parameters(func, *args, **kwargs)
    ...         print(list(params.items()))
    ...         return func(*args, **kwargs)
    ...     return wrapper

    >>> @helper
    ... def args(a, b):
    ...     pass

    >>> args(1, 2)
    [('a', '1'), ('b', '2')]

    >>> args(*(1,2))
    [('a', '1'), ('b', '2')]

    >>> args(1, b=2)
    [('a', '1'), ('b', '2')]

    >>> @helper
    ... def kwargs(a=1, b=2):
    ...     pass

    >>> kwargs()
    [('a', '1'), ('b', '2')]

    >>> kwargs(a=3, b=4)
    [('a', '3'), ('b', '4')]

    >>> kwargs(b=4, a=3)
    [('a', '3'), ('b', '4')]

    >>> kwargs(a=3)
    [('a', '3'), ('b', '2')]

    >>> kwargs(b=4)
    [('a', '1'), ('b', '4')]

    >>> @helper
    ... def args_kwargs(a, b, c=3, d=4):
    ...     pass

    >>> args_kwargs(1, 2)
    [('a', '1'), ('b', '2'), ('c', '3'), ('d', '4')]

    >>> args_kwargs(1, 2, d=5)
    [('a', '1'), ('b', '2'), ('c', '3'), ('d', '5')]

    >>> args_kwargs(1, 2, 5, 6)
    [('a', '1'), ('b', '2'), ('c', '5'), ('d', '6')]

    >>> args_kwargs(1, b=2)
    [('a', '1'), ('b', '2'), ('c', '3'), ('d', '4')]

    >>> @helper
    ... def varargs(*a):
    ...     pass

    >>> varargs()
    []

    >>> varargs(1, 2)
    [('a', '(1, 2)')]

    >>> @helper
    ... def keywords(**a):
    ...     pass

    >>> keywords()
    []

    >>> keywords(a=1, b=2)
    [('a', '1'), ('b', '2')]

    >>> @helper
    ... def args_varargs(a, b, *c):
    ...     pass

    >>> args_varargs(1, 2)
    [('a', '1'), ('b', '2')]

    >>> args_varargs(1, 2, 2)
    [('a', '1'), ('b', '2'), ('c', '(2,)')]

    >>> @helper
    ... def args_kwargs_varargs(a, b, c=3, **d):
    ...     pass

    >>> args_kwargs_varargs(1, 2)
    [('a', '1'), ('b', '2'), ('c', '3')]

    >>> args_kwargs_varargs(1, 2, 4, d=5, e=6)
    [('a', '1'), ('b', '2'), ('c', '4'), ('d', '5'), ('e', '6')]

    >>> @helper
    ... def args_kwargs_varargs_keywords(a, b=2, *c, **d):
    ...     pass

    >>> args_kwargs_varargs_keywords(1)
    [('a', '1'), ('b', '2')]

    >>> args_kwargs_varargs_keywords(1, 2, 4, d=5, e=6)
    [('a', '1'), ('b', '2'), ('c', '(4,)'), ('d', '5'), ('e', '6')]

    >>> class Class(object):
    ...     @staticmethod
    ...     @helper
    ...     def static_args(a, b):
    ...         pass
    ...
    ...     @classmethod
    ...     @helper
    ...     def method_args(cls, a, b):
    ...         pass
    ...
    ...     @helper
    ...     def args(self, a, b):
    ...         pass

    >>> cls = Class()

    >>> cls.args(1, 2)
    [('a', '1'), ('b', '2')]

    >>> cls.method_args(1, 2)
    [('a', '1'), ('b', '2')]

    >>> cls.static_args(1, 2)
    [('a', '1'), ('b', '2')]

    """
    parameters = {}
    arg_spec = inspect.getfullargspec(func)

    arg_order = list(arg_spec.args)
    arg_order.extend(list(arg_spec.kwonlyargs))

    args_dict = dict(zip(arg_spec.args, args))
    args_dict.update(dict(zip(arg_spec.kwonlyargs, args)))

    if arg_spec.defaults:
        kwargs_defaults_dict = dict(zip(arg_spec.args[-len(arg_spec.defaults) :], arg_spec.defaults))
        parameters.update(kwargs_defaults_dict)

    if arg_spec.varargs:
        arg_order.append(arg_spec.varargs)
        varargs = args[len(arg_spec.args) :]
        parameters.update({arg_spec.varargs: varargs} if varargs else {})

    if arg_spec.args and arg_spec.args[0] in ["cls", "self"]:
        args_dict.pop(arg_spec.args[0], None)

    if kwargs:
        arg_order.extend(list(kwargs.keys()))
        parameters.update(kwargs)

    parameters.update(args_dict)

    if arg_spec.kwonlydefaults:
        for arg, default in arg_spec.kwonlydefaults.items():
            if arg not in parameters:
                parameters[arg] = default

    items = parameters.iteritems() if six.PY2 else parameters.items()
    # sorted_items = sorted(map(lambda kv: (kv[0], represent(kv[1])), items), key=lambda x: arg_order.index(x[0]))
    # sorted_items = sorted(map(lambda kv: (kv[0], kv[1]), items), key=lambda x: arg_order.index(x[0]))
    sorted_items = sorted(((key, value) for key, value in items), key=lambda x: arg_order.index(x[0]))

    return collections.OrderedDict(sorted_items)
