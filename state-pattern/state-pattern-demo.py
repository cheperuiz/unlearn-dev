from __future__ import annotations
from enum import Enum, auto
from typing import Callable, Tuple, Dict, Optional
from dataclasses import dataclass, field
import time


####################################################
#########         LIBRARY CODE          ############
####################################################
class EventType(Enum):
    THING_CREATED = auto()
    THING_UPDATED = auto()
    THING_ENDED = auto()


@dataclass
class Event:
    event_type: EventType
    thing_id: int


####################################################
#########         DOMAIN MODEL          ############
####################################################
@dataclass
class Thing:
    thing_id: int = field()
    counter: int = field(default=0)
    active: bool = field(default=True)


@dataclass
class ThingInfo:
    owner: str

    def __init__(self, owner: str) -> None:
        self.owner = owner


things_db: Dict[int, Tuple[Thing, ThingInfo]] = {}


def create_thing(thing_id: int) -> Tuple[Thing, ThingInfo]:
    thing_tuple = Thing(thing_id), ThingInfo("a user")
    things_db[thing_id] = thing_tuple
    return thing_tuple


def find_thing(thing_id: int) -> Tuple[Optional[Thing], Optional[ThingInfo]]:
    if thing_id in things_db:
        return things_db[thing_id]
    return None, None


def save_thing(thing: Thing, thing_info: ThingInfo) -> None:
    things_db[thing.thing_id] = (thing, thing_info)


####################################################
############### STATE PATTERN ######################
####################################################


def to_snake_case(name: str) -> str:
    return name.lower()


############# Context (State Machine) #######################
class ThingContext:
    state: State

    def __init__(self, state: State) -> None:
        self.state = state

    def handle(self, event: Event) -> None:
        handler = self.state.handler_for(event.event_type)
        next_state = handler(event)
        if self.state != next_state:
            self.set_state(next_state)

    def set_state(self, state: State) -> None:
        self.state.on_exit()
        self.state = state
        self.state.on_enter()


############# Base class for STATE ##########################
class State:
    def on_enter(self) -> None:
        print(f"ENTERING: {self.__class__.__name__}")

    def handler_for(self, event_type: EventType) -> Callable[[Event], State]:
        handler_name = "on_" + to_snake_case(event_type.name)
        return getattr(self, handler_name, self.null_handler)

    def on_exit(self) -> None:
        print(f"EXITING: {self.__class__.__name__}")

    def null_handler(self, event: Event) -> State:
        print(f"No handler for {event.event_type} in {self.__class__.__name__}")
        return self


############ Concrete States###########################
class NewThing(State):
    def on_thing_created(self, event: Event) -> State:
        thing, thing_info = create_thing(event.thing_id)
        return BuildingThing(thing, thing_info)


class BuildingThing(State):
    thing: Thing
    thing_info: ThingInfo

    def __init__(self, thing: Thing, thing_info: ThingInfo) -> None:
        self.thing = thing
        self.thing_info = thing_info

    def on_thing_updated(self, event: Event) -> State:
        self.thing.counter += 1
        save_thing(self.thing, self.thing_info)
        print(f"Updated thing: {self.thing}")
        return self

    def on_thing_ended(self, event: Event) -> State:
        self.thing.active = False
        save_thing(self.thing, self.thing_info)
        return ThingDone(self.thing, self.thing_info)

    def on_exit(self) -> None:
        print(f"EXITING: {self.__class__.__name__} with state: {self.thing}")


class ThingDone(State):
    thing: Thing
    thing_info: ThingInfo

    def __init__(self, thing: Thing, thing_info: ThingInfo) -> None:
        self.thing = thing
        self.thing_info = thing_info

    def on_enter(self) -> None:
        super().on_enter()
        print(f"{self.thing} has ended and will not handle any more events.")
        print(f"Final state was: {self.thing}")


##################### What we need to handle any events ############


def context_for(thing_id: int) -> ThingContext:
    thing, thing_info = find_thing(thing_id)
    state = state_factory(thing, thing_info)
    return ThingContext(state)


def infer_state(thing: Thing) -> str:
    if thing is None:
        return "NEW_THING"
    if thing is not None and thing.active:
        return "BUILDING_THING"
    return "FINISH_THING"


def state_factory(thing: Optional[Thing], thing_info: Optional[ThingInfo]) -> State:
    if thing is None:
        return NewThing()

    assert thing
    assert thing_info  # These lines remove mypy warnings (thing_info can't be None)
    state_name = infer_state(thing)

    if state_name == "BUILDING_THING":
        return BuildingThing(thing, thing_info)

    if state_name == "FINISH_THING":
        return ThingDone(thing, thing_info)

    raise ValueError(f"No state class for {state_name}")


def handle_any_event(redis_name: str, event: Event, event_id: str) -> None:
    print(event)
    context = context_for(event.thing_id)
    context.handle(event)
    print()


######################## DEMO TIME!!!!! ################################

if __name__ == "__main__":
    handle_any_event("", Event(EventType.THING_CREATED, 0), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_UPDATED, 0), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_UPDATED, 0), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_UPDATED, 0), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_UPDATED, 0), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_ENDED, 0), "")

    # This event will not be handled
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_UPDATED, 0), "")

    handle_any_event("", Event(EventType.THING_CREATED, 1), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_UPDATED, 1), "")
    time.sleep(0.5)
    handle_any_event("", Event(EventType.THING_ENDED, 1), "")
