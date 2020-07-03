import time
import sys
from threading import Thread, Lock

from kitchen import Kitchen, Grill, CuttingBoard, Pantry
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


class LockingCuttingBoard(CuttingBoard):
    def __init__(self, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = lock

    def use(self, *args, **kwargs):
        with self.lock:
            return super().use(*args, **kwargs)


class LockingGrill(Grill):
    def __init__(self, lock, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = lock

    def use(self, *args, **kwargs):
        with self.lock:
            return super().use(*args, **kwargs)


class LockingKitchen(Kitchen):
    def __init__(self):
        self.pantry = Pantry()
        self.cutting_board = LockingCuttingBoard(Lock())
        self.grill = LockingGrill(Lock())


kitchen = LockingKitchen()
results = []


def make_burger(order):
    recipe = RECIPES[order]
    ingredients_list = ingredients_list_from_recipe(recipe)
    ingredients = gather_ingredients(ingredients_list, kitchen.pantry)
    prepared_ingredients = [prepare_ingerdient(ingredient, kitchen) for ingredient in ingredients]
    prepared_ingredients = list(flat_generator(prepared_ingredients))
    results.append(Burger(order, select_ingredients(recipe, prepared_ingredients)))


if __name__ == "__main__":
    multiplier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    orders = multiplier * sys.argv[1].split(",")

    threads = []
    start_time = time.time()

    for order in orders:
        t = Thread(target=make_burger, args=(order,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for burger in results:
        burger.taste(RECIPES[order])
        print(f"You can eat your delicious '{burger}'")

    print(f"Delivered {len(orders)} burgers in {time.time()-start_time}s")
