import sys
import time
from random import shuffle

import pykka

from burgers import Burger
from kitchen import Pantry, Grill, CuttingBoard
from ingredients import GrillableIngredient, SliceableIngredient
from utils import infer_name, select

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


def round_robin_generator(collection):
    while True:
        yield from collection


def is_slice(name):
    return any(substring in name for substring in ["slice", "ring", "piece", "bottom", "top"])


class BurgerBuilderActor(pykka.ThreadingActor):
    def __init__(self, recipes, slicers, grillers):
        super().__init__()
        self.recipes = recipes
        self.slicers = round_robin_generator(slicers)
        self.grillers = round_robin_generator(grillers)

    def make_burger(self, order):
        recipe = self.recipes[order]
        future_ingredients = []
        for ingredient in recipe:
            if is_slice(ingredient):
                slicer = next(self.slicers)
                future_ingredient = slicer.ask_for_sliced(ingredient)
            else:
                griller = next(self.grillers)
                future_ingredient = griller.ask_for_grilled(ingredient)
            future_ingredients.append(future_ingredient)
        prepared_ingredients = pykka.get_all(future_ingredients)
        return Burger(order, prepared_ingredients)


class SlicerActor(pykka.ThreadingActor):
    def __init__(self, pantry):
        super().__init__()
        self.pantry = pantry
        self.slices = []
        self.cutting_board = CuttingBoard()

    def ask_for_sliced(self, sliced):
        selected = select(sliced, self.slices)
        if not selected:
            name = infer_name(sliced)
            ingredient = self.pantry.gather(name)
            self.slices += self.cutting_board.use(ingredient)
            selected = select(sliced, self.slices)
        return selected


class GrillerActor(pykka.ThreadingActor):
    GRILL_TIMES = {
        "beefpatty": 20,
        "chickenpatty": 20,
        "veggiepatty": 20,
        "bacon": 20,
    }

    def __init__(self, pantry):
        super().__init__()
        self.pantry = pantry
        self.grill = Grill()

    def ask_for_grilled(self, grilled):
        name = infer_name(grilled)
        ingredient = self.pantry.gather(name)
        return self.grill.use(ingredient, self.GRILL_TIMES[name])


class KitchenActors:
    def __init__(self, pantry, n_slicers=8, n_grillers=4, n_builders=16):
        self.slicers = [SlicerActor.start(pantry).proxy() for _ in range(n_slicers)]
        self.grillers = [GrillerActor.start(pantry).proxy() for _ in range(n_grillers)]
        self.builders = [
            BurgerBuilderActor.start(RECIPES, self.slicers, self.grillers).proxy() for _ in range(n_builders)
        ]


if __name__ == "__main__":
    multiplier = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    orders = multiplier * sys.argv[1].split(",")

    kitchen = KitchenActors(Pantry())
    builder_generator = round_robin_generator(kitchen.builders)

    start_time = time.time()
    future_burgers = []
    for order in orders:
        builder = next(builder_generator)
        future_burger = builder.make_burger(order)
        future_burgers.append(future_burger)

    burgers = pykka.get_all(future_burgers)

    for order, burger in zip(orders, burgers):
        burger.taste(RECIPES[order])
        print(f"You can eat your delicious '{burger}'")

    pykka.ActorRegistry.stop_all()
    print(f"Delivered {len(orders)} burgers in {time.time()-start_time}s")
