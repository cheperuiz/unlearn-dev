from dataclasses import dataclass, field
from typing import List

from ingredients import Ingredient, GrillableIngredient


@dataclass
class Burger:
    name: str = field()
    ingredients: List[Ingredient] = field(repr=False)

    def __post_init__(self):
        if not all(isinstance(e, Ingredient) for e in self.ingredients):
            raise ValueError(f"'{self.ingredients}' is not a list of ingredients.")

    def taste(self, recipe):
        self._all_ingredients_in_correct_order(recipe)
        self._all_ingredients_cooked_correctly()

    def _all_ingredients_in_correct_order(self, recipe):
        try:
            assert len(recipe) == len(self.ingredients)
            assert all(ingredient.name == item for ingredient, item in zip(self.ingredients, recipe))
        except AssertionError:
            raise ValueError("Ingredients are incomplete or in incorrect order.") from None

    def _all_ingredients_cooked_correctly(self):
        grillable_ingredients = [
            ingredient for ingredient in self.ingredients if isinstance(ingredient, GrillableIngredient)
        ]
        try:
            assert all(ingredient.acceptable_doneness() for ingredient in grillable_ingredients)
        except AssertionError:
            raise ValueError(f"Some ingredients were not cooked correctly: {grillable_ingredients}") from None
