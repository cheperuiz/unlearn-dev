import time
import asyncio

from typing import List
from ingredients import (
    Ingredient,
    SliceableIngredient,
    GrillableIngredient,
    Bun,
    Lettuce,
    Tomato,
    Onion,
    Pickle,
    Cheese,
    BeefPatty,
    ChickenPatty,
    VeggiePatty,
    Bacon,
)


class AsyncGrill:
    def __init__(self):
        self._hot_surface: List[Ingredient] = []

    def _place_ingredient(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise TypeError(f"'{ingredient!r}' is not a valid Ingredient.")
        if not isinstance(ingredient, GrillableIngredient):
            raise TypeError(f"Can't use grill with non-grillable '{ingredient.name}'")
        self._hot_surface.append(ingredient)

    def _remove_ingredient(self):
        ingredient = self._hot_surface.pop()
        ingredient.name = "-".join(["grilled", ingredient.name])
        return ingredient

    def _heat_intredients(self, temp_delta):
        for ingredient in self._hot_surface:
            ingredient.apply_heat(temp_delta)

    async def use(self, ingredient, period, interval=3, temp_delta=10):
        self._place_ingredient(ingredient)
        while (period := period - interval) > 0:
            await self._wait(interval / 10)
            self._heat_intredients(temp_delta)
        return self._remove_ingredient()

    @staticmethod
    async def _wait(period):
        await asyncio.sleep(period)


class AsyncCuttingBoard:
    def __init__(self):
        self._board: List[Ingredient] = []

    def _place_ingredient(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise TypeError(f"'{ingredient}' is not a valid Ingredient.")
        if not isinstance(ingredient, SliceableIngredient):
            raise TypeError(f"Can't use slicing station with non-sliceable '{ingredient.name}'")
        self._board.append(ingredient)

    def _slice_ingredient_in_board(self):
        ingredient = self._board.pop()
        slices = ingredient.to_slices()
        del ingredient
        return slices

    async def use(self, ingredient):
        self._place_ingredient(ingredient)
        await self._wait(len(ingredient.slice_into) / 10)
        return self._slice_ingredient_in_board()

    @staticmethod
    async def _wait(period):
        await asyncio.sleep(period)


class Pantry:
    SLICEABLE_INGREDIENTS = {
        "bun": Bun,
        "lettuce": Lettuce,
        "tomato": Tomato,
        "onion": Onion,
        "pickle": Pickle,
        "cheese": Cheese,
    }
    GRILLABLE_INGREDIENTS = {
        "beefpatty": BeefPatty,
        "chickenpatty": ChickenPatty,
        "veggiepatty": VeggiePatty,
        "bacon": Bacon,
    }
    ALL_INGREDIENTS = list(SLICEABLE_INGREDIENTS) + list(GRILLABLE_INGREDIENTS)

    def gather(self, ingredient):
        if ingredient not in self.ALL_INGREDIENTS:
            raise ValueError(f"Can't make unknown ingredient '{ingredient}'")
        if ingredient in self.SLICEABLE_INGREDIENTS:
            item = self.SLICEABLE_INGREDIENTS[ingredient]()
        if ingredient in self.GRILLABLE_INGREDIENTS:
            item = self.GRILLABLE_INGREDIENTS[ingredient]()
        print(f"Gathered {item} from pantry.")
        return item


class AsyncKitchen:
    grill = None
    cutting_board = None
    pantry = None

    def __init__(self):
        self.grill = AsyncGrill()
        self.cutting_board = AsyncCuttingBoard()
        self.pantry = Pantry()
