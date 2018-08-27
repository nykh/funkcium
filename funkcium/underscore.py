import inspect
from inspect import Signature, Parameter

__all__ = ['underscore']


class _AST(object):
    def __call__(self, *args):
        raise NotImplementedError()

    def __getattr__(self, name): return _GetAttr(name, self)

    def __add__(self, a): return _Add(a, self)

    def __radd__(self, a): return self.__add__(a)


class _UnaryExpr(_AST):
    def __init__(self, name, f):
        self.info = {'name': name, 'f': f}

    def __repr__(self):
        return "{name}({f!r})".format(**self.info)

    def __call__(self):
        raise NotImplementedError()


class _Id(_UnaryExpr):
    __signature__ = Signature([Parameter('x', Parameter.POSITIONAL_ONLY)])

    def __init__(self):
        pass

    def __call__(self, x):
        return x

    def __repr__(self):
        return "_"

class _BinaryExpr(_AST):
    __signature__ = Signature([Parameter('y', Parameter.POSITIONAL_ONLY)])

    def __init__(self, name, f, a):
        self.info = {'name': name, 'a': a, 'f': f}
        self.f = f

    def __repr__(self):
        return "{name}({a}, {f!r})".format(**self.info)

    def __call__(self, other):
        raise NotImplementedError()


class _Add(_BinaryExpr):
    def __init__(self, a, f):
        super().__init__('Add', f, a)
        self.a = a

    def __call__(self, x):
        return self.a + self.f(x)


class _GetAttr(_BinaryExpr):
    def __init__(self, name, f):
        self.f = f
        self.name = name

    def __repr__(self):
        return "{f!r}.{name}".format(f=self.f, name=self.name)

    def __call__(self, x):
        return getattr(self.f(x), self.name)


underscore = _Id()

############################### test #################################


def test_ast():
    from collections import namedtuple

    x = _Id()
    assert x(1) == 1

    point = namedtuple('point', ['x', 'y'])

    y = _GetAttr('x', _Id())
    assert y(point(1, 2)) == 1
    assert str(y) == "x.x"

    z = _Add(3, _GetAttr('x', _Id()))
    assert z(point(1, 2)) == 4
    assert str(z) == "Add(3, x.x)"


def test_underscore_basic():
    from function import Func
    from functor.list import List
    from collections import namedtuple

    _ = _Id()
    point = namedtuple('point', ['x', 'y'])

    ps = List(point(1, 2), point(3, 4), point(5, 6))
    xs = ps.map(_.x)
    assert len(xs) == len(ps)
    assert xs[0] == 1
    assert xs[1] == 3
    assert xs[2] == 5
