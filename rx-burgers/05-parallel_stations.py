import time
import sys
from multiprocessing import Pool, cpu_count

from ingredients import GrillableIngredient, SliceableIngredient
from kitchen import Kitchen, Pantry, CuttingBoard, Grill
from burgers import Burger
from utils import (
    ingredients_list_from_recipe,
    flat_generator,
    select_ingredients,
    gather_ingredients,
    slice_ingredient,
    grill_ingredient,
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


class MultiStationKitchen:
    def __init__(self, n_grills=4, n_cutting_boards=8):
        self.pantry = Pantry()
        self.grills = n_grills * [Grill()]
        self.cutting_boards = n_cutting_boards * [CuttingBoard()]


kitchen = MultiStationKitchen()


def match_lengths(long, short):
    n = len(long) // len(short)
    m = len(long) % len(short)
    repeated = n * short
    repeated += short[:m]
    return repeated


def pair_ingredients_stations(ingredients, stations):
    if len(ingredients) > len(stations):
        repeated_stations = match_lengths(ingredients, stations)
        return ingredients, repeated_stations
    else:
        return ingredients, stations[: len(ingredients)]


def prepare_parallel(ingredients, stations, op):
    n = len(stations)
    with Pool(n) as pool:
        args = zip(*pair_ingredients_stations(ingredients, stations))
        prepared_ingredients = pool.starmap(op, args)

    return prepared_ingredients


def make_burger(order):
    recipe = RECIPES[order]
    ingredients_list = ingredients_list_from_recipe(recipe)
    ingredients = gather_ingredients(ingredients_list, kitchen.pantry)

    grillable_ingredients = [
        ingredient for ingredient in ingredients if isinstance(ingredient, GrillableIngredient)
    ]
    sliceable_ingredients = [
        ingredient for ingredient in ingredients if isinstance(ingredient, SliceableIngredient)
    ]

    prepared_ingredients = prepare_parallel(sliceable_ingredients, kitchen.cutting_boards, slice_ingredient)
    prepared_ingredients += prepare_parallel(grillable_ingredients, kitchen.grills, grill_ingredient)
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
