import asyncio
import time
import sys

from async_kitchen import AsyncKitchen
from burgers import Burger
from ingredients import SliceableIngredient, GrillableIngredient
from utils import (
    ingredients_list_from_recipe,
    prepare_ingerdient,
    flat_generator,
    select_ingredients,
    gather_ingredients,
)

RECIPES = {
    "cheeseburger": [
        "bun-bottom",
        "lettuce-slice",
        "onion-ring",
        "tomato-slice",
        "grilled-beefpatty",
        "cheese-slice",
        "bun-top",
    ]
}

GRILL_TIMES = {
    "beefpatty": 20,
    "chickenpatty": 20,
    "veggiepatty": 20,
    "bacon": 20,
}


async def async_prepare_ingerdient(ingredient, kitchen):
    if isinstance(ingredient, SliceableIngredient):
        async with kitchen.cutting_board_lock:
            return await async_slice_ingredient(ingredient, kitchen.cutting_board)
    if isinstance(ingredient, GrillableIngredient):
        async with kitchen.grill_lock:
            return await async_grill_ingredient(ingredient, kitchen.grill)
    return ingredient


async def async_slice_ingredient(ingredient, cutting_board):
    return await cutting_board.use(ingredient)


async def async_grill_ingredient(ingredient, grill):
    return await grill.use(ingredient, GRILL_TIMES[ingredient.name])


class SafeAsyncKitchen(AsyncKitchen):
    def __init__(self):
        super().__init__()
        self.cutting_board_lock = asyncio.Lock()
        self.grill_lock = asyncio.Lock()


async def make_burger(order, kitchen):
    recipe = RECIPES[order]
    ingredients_list = ingredients_list_from_recipe(recipe)
    ingredients = gather_ingredients(ingredients_list, kitchen.pantry)
    prepared_ingredients = [await async_prepare_ingerdient(ingredient, kitchen) for ingredient in ingredients]
    prepared_ingredients = list(flat_generator(prepared_ingredients))
    return Burger(order, select_ingredients(recipe, prepared_ingredients))


async def main():
    multiplier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    orders = multiplier * sys.argv[1].split(",")

    start_time = time.time()
    kitchen = SafeAsyncKitchen()
    coroutines = [make_burger(order, kitchen) for order in orders]
    burgers = await asyncio.gather(*coroutines)
    for burger, order in zip(burgers, orders):
        burger.taste(RECIPES[order])
        print(f"You can eat your delicious '{burger}'")

    print(f"Delivered {len(orders)} burgers in {time.time()-start_time}s")


if __name__ == "__main__":
    asyncio.run(main())
