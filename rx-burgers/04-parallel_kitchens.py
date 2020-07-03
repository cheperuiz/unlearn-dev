import time
import sys
from multiprocessing import Pool, cpu_count

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


def match_lengths(long, short):
    n = len(long) // len(short)
    m = len(long) % len(short)
    repeated = n * short
    repeated += short[:m]
    return repeated


def pair_orders_kitchens(orders, kitchens):
    if len(orders) > len(kitchens):
        repeated_kitchens = match_lengths(orders, kitchens)
        return orders, repeated_kitchens
    else:
        return orders, kitchens[: len(orders)]


def make_burger(order, kitchen):
    recipe = RECIPES[order]
    ingredients_list = ingredients_list_from_recipe(recipe)
    ingredients = gather_ingredients(ingredients_list, kitchen.pantry)
    prepared_ingredients = [prepare_ingerdient(ingredient, kitchen) for ingredient in ingredients]
    prepared_ingredients = list(flat_generator(prepared_ingredients))
    return Burger(order, select_ingredients(recipe, prepared_ingredients))


if __name__ == "__main__":
    multiplier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    orders = multiplier * sys.argv[1].split(",")

    kitchens = cpu_count() * [Kitchen()]

    start_time = time.time()
    with Pool(len(kitchens)) as pool:
        args = zip(*pair_orders_kitchens(orders, kitchens))
        burgers = pool.starmap(make_burger, args)

    for order, burger in zip(orders, burgers):
        burger.taste(RECIPES[order])
        print(f"You can eat your delicious '{burger}'")

    print(f"Delivered {len(orders)} burgers in {time.time()-start_time}s")
