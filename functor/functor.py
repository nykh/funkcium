from typing import TypeVar, Generic, Callable, Sequence

T = TypeVar('T')
U = TypeVar('U')


class Functor(Generic[T]):
    def map(self, f: Callable[[T], U]) -> 'Functor[U]':
        raise NotImplementedError()

    def flatmap(self, f: Callable[[T], Sequence[U]]) -> 'Functor[U]':
        raise NotImplementedError()
