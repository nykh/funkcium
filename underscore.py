class Shortcut(object):
    def __getattr__(self, name):
        return lambda x: getattr(x, name)


_ = Shortcut()

############################### test #################################


def test_underscore_basic():
    from function import Func
    from functor.list import List
    from dataclasses import dataclass

    @dataclass
    class point:
        x: int
        y: int

    ps = List(point(1, 2), point(3, 4), point(5, 6))
    xs = ps.map(_.x)
    assert len(xs) == len(ps)
    assert xs[0] == 1
    assert xs[1] == 3
    assert xs[2] == 5
