from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class Predicate(Generic[T]):

    def __init__(self, condition: Callable[[T], bool]):
        self.condition = condition

    def and_(self, condition: Callable[[T], bool]) -> "Predicate[T]":
        return Predicate(lambda t: condition(t) and self.condition(t))

    def or_(self, condition: Callable[[T], bool]) -> "Predicate[T]":
        return Predicate(lambda t: condition(t) or self.condition(t))

    def test(self, arg: T) -> bool:
        return self.condition(arg)