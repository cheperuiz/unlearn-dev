from typing import List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

Ingredient = str


@dataclass
class AbstractBurger:
    name: str = field(default="Abstract Burger")
    ingredients: List[Ingredient] = field(
        default_factory=lambda: ["bun-bottom", "lettuce", "beefpatty", "tomato", "onion", "bun-top"],
        repr=False,
    )


class BurgerMeta(ABC):
    @abstractmethod
    def make_recipe(self):
        print("Recipe for: ", end="")
        self.announce()
        for ingredient in self.ingredients:
            print(ingredient)

    def announce(self):
        print(self.name)


@dataclass
class ClassicBurger(AbstractBurger, BurgerMeta):
    name: str = field(default="Classic Burger")

    def make_recipe(self):
        super().make_recipe()


@dataclass
class CheeseBurger(AbstractBurger, BurgerMeta):
    def __init__(self):
        super().__init__()
        self.name = "Cheese Burger"
        patty_index = self.ingredients.index("beefpatty")
        self.ingredients.insert(patty_index + 1, "cheese")

    def make_recipe(self):
        super().make_recipe()


@dataclass
class ImpossibleBurger(AbstractBurger, BurgerMeta):
    def __init__(self):
        super().__init__()
        self.name = "Impossible Burger"
        patty_index = self.ingredients.index("beefpatty")
        self.ingredients.pop(patty_index)
        self.ingredients.insert(patty_index, "impossiblepatty")

    def make_recipe(self):
        print(f"Recipe for: {self.name}")
        for ingredient in self.ingredients:
            if "patty" in ingredient:
                print(f"{ingredient} <---- VEGAN POWER!!!")
            else:
                print(ingredient)
