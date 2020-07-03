import time
import sys
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool

from ingredients import GrillableIngredient, SliceableIngredient
from kitchen import Pantry, CuttingBoard, Grill
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


def match_lengths(long, short):
    n = len(long) // len(short)
    m = len(long) % len(short)
    repeated = n * short
    repeated += short[:m]
    return repeated


def pair_mismatched_lists(lst1, lst2):
    if len(lst1) > len(lst2):
        repeated = match_lengths(lst1, lst2)
        return lst1, repeated
    else:
        return lst1, lst2[: len(lst1)]


def prepare_parallel(ingredients, stations, op):
    n = len(stations)
    with ThreadPool(n) as pool:
        args = zip(*pair_mismatched_lists(ingredients, stations))
        prepared_ingredients = pool.starmap(op, args)

    return prepared_ingredients


def make_burger(order, kitchen):
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


class MultiStationKitchen:
    def __init__(self, n_grills=4, n_cutting_boards=8):
        self.pantry = Pantry()
        self.grills = n_grills * [Grill()]
        self.cutting_boards = n_cutting_boards * [CuttingBoard()]


if __name__ == "__main__":
    multiplier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    orders = multiplier * sys.argv[1].split(",")

    kitchens = cpu_count() * [MultiStationKitchen()]
    start_time = time.time()
    with Pool(len(kitchens)) as pool:
        args = zip(*pair_mismatched_lists(orders, kitchens))
        burgers = pool.starmap(make_burger, args)

    for order, burger in zip(orders, burgers):
        burger.taste(RECIPES[order])
        print(f"You can eat your delicious '{burger}'")

    print(f"Delivered {len(orders)} burgers in {time.time()-start_time}s")
