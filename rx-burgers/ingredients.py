from dataclasses import dataclass, field
from typing import List


@dataclass
class Ingredient:
    name: str = field()


@dataclass
class SliceableIngredient(Ingredient):
    slice_into: List[str] = field(default_factory=list, repr=False)

    def __init__(self, name, slice_into, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.slice_into = slice_into
        if not len(self.slice_into):
            raise TypeError("__init__() missing 1 required positional argument: 'slice_into'")

    def to_slices(self):
        slices = self.slice_into[:]
        self.slice_into = []
        print(f"Slicing {self} into {len(slices)} parts.")
        return [Ingredient(s) for s in slices]


@dataclass
class GrillableIngredient(Ingredient):
    temp: int = field(default=4)
    BAD_DONENESS = ["raw", "burned"]

    def apply_heat(self, delta_temp=10):
        self.temp += delta_temp
        print(f"Heating {self}.")

    def acceptable_doneness(self):
        return self.doneness not in self.BAD_DONENESS

    def __repr__(self):
        return f"{self.__class__.__name__}(temp='{self.temp}', doneness='{self.doneness}')"

    @property
    def doneness(self):
        if self.temp < 40:
            return "raw"
        if self.temp < 50:
            return "rare"
        if self.temp < 60:
            return "medium"
        if self.temp < 70:
            return "well-done"
        return "burned"


@dataclass(repr=False)
class Bun(SliceableIngredient):
    name: str = "bun"
    slice_into: List[str] = field(default_factory=lambda: ["bun-bottom", "bun-top"])


@dataclass(repr=False)
class Lettuce(SliceableIngredient):
    name: str = "lettuce"
    slice_into: List[str] = field(default_factory=lambda: 10 * ["lettuce-slice"])


@dataclass(repr=False)
class Tomato(SliceableIngredient):
    name: str = "tomato"
    slice_into: List[str] = field(default_factory=lambda: 5 * ["tomato-slice"])


@dataclass(repr=False)
class Onion(SliceableIngredient):
    name: str = "onion"
    slice_into: List[str] = field(default_factory=lambda: 5 * ["onion-ring"])


@dataclass(repr=False)
class Pickle(SliceableIngredient):
    name: str = "pickle"
    slice_into: List[str] = field(default_factory=lambda: 5 * ["pickle-slice"])


@dataclass(repr=False)
class Cheese(SliceableIngredient):
    name: str = "cheese"
    slice_into: List[str] = field(default_factory=lambda: 5 * ["cheese-slice"])


@dataclass(repr=False)
class BeefPatty(GrillableIngredient):
    name: str = "beefpatty"


@dataclass(repr=False)
class ChickenPatty(GrillableIngredient):
    name: str = "chickenpatty"


@dataclass(repr=False)
class VeggiePatty(GrillableIngredient):
    name: str = "veggiepatty"


@dataclass(repr=False)
class Bacon(GrillableIngredient):
    name: str = "bacon"
