from types import GeneratorType as geneator
from collections import Iterable as iterable
import itertools
from copy import copy

from .functor import Functor

__all__ = ['List']


class List(Functor, iterable):
    __overriden__ = ['map', 'flatmap', '__len__', '__iter__', '__add__', '__getitem__']

    def __init__(self, *args):
        if len(args) == 1:
            head = args[0]
            if isinstance(head, iterable) or isinstance(head, geneator):
                self._list = list(head)
            else:
                self._list = [head]
        else:
            self._list = list(args)

    def map(self, f):
        return List(map(f, self._list))

    def flatmap(self, f):
        return List(itertools.chain(*map(f, self._list)))

    def __eq__(self, other):
        return self._list == list(other)

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def __add__(self, other):
        li2 = copy(self._list)
        li2.extend(iter(other))
        return List(li2)

    def __mul__(self, times):
        return List(self._list * times)

    def __getitem__(self, i):
        return self._list[i]

    def __getattr__(self, name):
        if name not in self.__overriden__:
            return self._list.__getattribute__(name)

    def __repr__(self):
        return "List{}".format(self._list)


############################### test ## #####################################
def test_list_work_like_a_normal_list():
    import pytest

    nil = List()
    assert len(nil) == 0

    x = List(0, 1, 2)
    assert x[0] == 0
    assert x[1] == 1
    assert x[2] == 2
    with pytest.raises(IndexError):
        x[3]

    x.append(3)
    assert x[3] == 3

    y = List(4, 5, 6)
    assert len(x + y) == 7

    z = List(1)
    zzz = z * 3
    assert len(zzz) == 3
    assert all(z == 1 for z in zzz)


def test_list_is_a_functor():
    x = List(0, 1, 2)
    y = x.map(lambda x: x + 1)
    assert len(y) == len(x)
    assert y[0] == 1
    assert y[1] == 2
    assert y[2] == 3

    xxx = x.flatmap(lambda x: [x] * 3)
    assert len(xxx) == 3 * len(x)
    assert xxx[0] == xxx[1] == xxx[2] == 0
    assert xxx[3] == xxx[4] == xxx[5] == 1
    assert xxx[6] == xxx[7] == xxx[8] == 2
