# coding=utf-8

from ..base import PineError

def _expand_args (args, kwargs, specs):
    args_dict = {}
    if args:
        la = len(args)
        ls = len(specs)
        if la > ls:
            raise PineError("Too many arguments: {0} for {1}".format(la , ls))
        for a, spec in zip(args, specs):
            n, _, _ = spec
            args_dict[n] = a
    if kwargs:
        args_dict.update(kwargs)

    args_expanded = []
    # TODO: wrong key check
    for name, typ, mand in specs:
        a = args_dict.get(name, None)
        if a is None:
            if mand:
                raise PineErrpr("Missing mandatory arguemnt: {}".fomrat(name))
        else:
            if not isinstance(a, typ):
                raise PineErrpr("Invalid argument type mandatory arguemnt: {}".fomrat(name))
        args_expanded.append(a)

    return args_expanded
    

# *title(const string)
#  shorttitle(const string)
#  overlay(const bool)
#  precision(const integer)
#  scale(const integer)
#  max_bars_back(const integer)
#  linktoseries(const bool)
def study (vm, args, kwargs):
    title, stitle, _, _, _, _, _ = _expand_args(args, kwargs,
        (
            ('title', str, True),
            ('shorttitle', str, False),
            ('overlay', bool, False),
            ('precision', int, False),
            ('scale', int, False),
            ('max_bars_back', int, False),
            ('linktoseries', bool, False),
        )
    )
    return None
