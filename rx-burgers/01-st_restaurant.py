import time
import sys

from kitchen import Kitchen
from burgers import Burger
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

kitchen = Kitchen()


def make_burger(order):
    recipe = RECIPES[order]
    ingredients_list = ingredients_list_from_recipe(recipe)
    ingredients = gather_ingredients(ingredients_list, kitchen.pantry)
    prepared_ingredients = [prepare_ingerdient(ingredient, kitchen) for ingredient in ingredients]
    prepared_ingredients = list(flat_generator(prepared_ingredients))
    return Burger(order, select_ingredients(recipe, prepared_ingredients))


if __name__ == "__main__":
    multiplier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    orders = multiplier * sys.argv[1].split(",")

    start_time = time.time()
    for order in orders:
        burger = make_burger(order)
        burger.taste(RECIPES[order])
        print(f"You can eat your delicious '{burger}'")

    print(f"Delivered {len(orders)} burgers in {time.time()-start_time}s")
