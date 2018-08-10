from funkcium.function import Func
from funkcium.underscore import underscore as _
from funkcium.functor import *

## This works well with the new data class
from dataclasses import dataclass

@dataclass
class point:
    x: int
    y: int

ps = List(point(1, 2),
         point(3, 4),
         point(5, 6))

## First rule: map f . map g === map (f. g)
assert ps.map(_.x).map(_ + 1) == ps.map(_.x + 1) == List(2, 4, 6)

## Second rule: map f F[x] === F[f(x)]
functor = Some(1)
assert functor.map(_ + 1).get() == functor.get() + 1
functor = Non  # Non doesn't change when map'd on
assert functor.map(_ + 1) is functor
