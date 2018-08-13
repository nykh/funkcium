import inspect

__all__ = ['Func', 'Monad', 'fn', 'monad']


class _Func(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        return self.f(*args)

    def __lshift__(self, other):
        return Func(lambda *args: self.__call__(other.__call__(*args)))

    def __rshift__(self, other):
        return Func(lambda *args: other.__call__(self.__call__(*args)))


def fn(f):
    return Func(f)


class Func(_Func):
    def __init__(self, f, params=[], *, nargs=None):
        super(Func, self).__init__(f)
        self.params = params
        if nargs is None:
            self.expect_arity = self.to_arity(f) - len(params)
            self.max_arity = self.to_max_arity(f) - len(params)
        else:
            self.expect_arity = self.max_arity = nargs

    @staticmethod
    def to_arity(f):
        try:
            return sum(1 for p in inspect.signature(f, follow_wrapped=False).parameters.values() if p.default is inspect.Parameter.empty)
        except ValueError:
            ## numpy ufunc support
            return getattr(f, 'nin', 1)

    @staticmethod
    def to_max_arity(f):
        try:
            return len(inspect.signature(f, follow_wrapped=False).parameters)
        except ValueError:
            ## numpy ufunc support
            return getattr(f, 'nin', 1)

    def __call__(self, *args):
        if self.expect_arity <= len(args) <= self.max_arity:
            return self.f(*self.params, *args)
        elif len(args) < self.expect_arity:
            return Func(self.f, self.params + list(args))
        else:
            raise TypeError("Too many paremters for curried functions! Expect up to {} got {}".format(
                self.max_arity, len(args)))

    def __repr__(self):
        return "Func[{}]".format(self.f)


class Monad(_Func):
    def __init__(self, f):
        super(Monad, self).__init__(f)

    def __call__(self, *args):
        self.f(*args)
        if len(args) == 1:
            return args[0]
        else:
            return args


def monad(f):
    return Monad(f)


print_monad = Monad(print)


def print_fmt(fmt): return Monad(lambda *args: print(fmt.format(*args)))


def print_keyval(k): return Monad(lambda v: print("{0}={1}".format(k, v)))

##################################### test #################################


def test_composable_functions():
    p = Func(lambda x: x + 1) << Func(lambda x: x * 3)
    assert p(3) == (3 * 3) + 1
    q = Func(lambda x: x + 1) >> Func(lambda x: x * 3)
    assert q(3) == (3 + 1) * 3


def test_monad():
    m = print_monad >> Func(lambda x: x + 1) >> print_monad
    assert m(3) == 4


def test_currying():
    @fn
    def f(x, y, z):
        return x + y + z
    assert f(1)(2)(3) == 6
    assert f(1)(2, 3) == 6
    assert f(1, 2)(3) == 6

    ff = f(1, 2) >> f(3, 4)
    assert ff(5) == (1 + 2 + 3 + 4 + 5)

def test_currying_with_default_arg():
    def f(x, y=1, z=2):
        return x + y + z

    F = Func(f, nargs=1)
    assert F.expect_arity == 1
    assert F.max_arity == 1
    assert F(3) == 6

    F2 = Func(f)
    assert F2.expect_arity == 1
    assert F2.max_arity == 3
    assert F2(3) == 6
    assert F2(3, 5, 7) == 15
