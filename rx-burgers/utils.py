from ingredients import SliceableIngredient, GrillableIngredient

GRILL_TIMES = {
    "beefpatty": 20,
    "chickenpatty": 20,
    "veggiepatty": 20,
    "bacon": 20,
}


def infer_name(name, artifacts=["grilled", "slice", "ring", "piece", "bottom", "top"]):
    words = [word for word in name.split("-") if word not in artifacts]
    if len(words) != 1:
        raise ValueError(f"Couldn't infer name for '{name}'")
    return words[0]


def ingredients_list_from_recipe(recipe):
    return list(set(infer_name(ingredient) for ingredient in recipe))


def prepare_ingerdient(ingredient, kitchen):
    if isinstance(ingredient, SliceableIngredient):
        return slice_ingredient(ingredient, kitchen.cutting_board)
    if isinstance(ingredient, GrillableIngredient):
        return grill_ingredient(ingredient, kitchen.grill)
    return ingredient


def slice_ingredient(ingredient, cutting_board):
    return cutting_board.use(ingredient)


def grill_ingredient(ingredient, grill):
    return grill.use(ingredient, GRILL_TIMES[ingredient.name])


def gather_ingredients(ingredients_list, pantry):
    return [pantry.gather(ingredient) for ingredient in ingredients_list]


def flat_generator(nested_list):
    for item in nested_list:
        if isinstance(item, list):
            yield from flat_generator(item)
        else:
            yield item


def select(name, ingredients):
    for i, ingredient in enumerate(ingredients):
        if ingredient.name == name:
            return ingredients.pop(i)


def select_ingredients(recipe, ingredients):
    items = [select(item, ingredients) for item in recipe]
    return [item for item in items if item is not None]
