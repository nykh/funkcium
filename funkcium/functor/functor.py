from typing import TypeVar, Generic, Callable, Sequence

__all__ = ['Box']

T = TypeVar('T')
U = TypeVar('U')


class Functor(Generic[T]):
    def map(self, f: Callable[[T], U]) -> 'Functor[U]':
        raise NotImplementedError()

    def flatmap(self, f: Callable[[T], Sequence[U]]) -> 'Functor[U]':
        raise NotImplementedError()


class Box(Functor):
    def __init__(self, v):
        self.v = v

    def map(self, f):
        return Box(f(self.v))

    def __rshift__(self, f: Callable[[T], U]) -> 'Functor[U]':
        return self.map(f)

    def flatmap(self, f):
        u = f(v)
        if isinstance(u, Box):
            return u
        else:
            return Box(u)

    @property
    def get(self):
        return self.v

############################## test ################################


def test_unit_functor_works_as_expected():
    x = Box(1)
    y = x.map(lambda x: x + 1).map(lambda x: x * 3).map(lambda x: x - 3)
    assert y.get == (1 + 1) * 3 - 3
    z = x >> (lambda x: x + 1) >> (lambda x: x * 3) >> (lambda x: x - 3)
    assert z.get == (1 + 1) * 3 - 3
