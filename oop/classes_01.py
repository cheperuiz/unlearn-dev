# ABC is "Abstract Base Class"
from abc import ABC, abstractmethod


class MyClass:
    def give_answer(self):
        return 42


class OtherClass(MyClass):
    pass


class SomeAbstractClass(ABC):
    @abstractmethod
    def some_interface(self, this, doesnt, matter):
        pass


class BadConcreteClass(SomeAbstractClass):
    def other_method(self):
        print("Haha! Im' bad!")


class GoodConcreteClass(SomeAbstractClass):
    def some_interface(self):
        return "Life is good..."
