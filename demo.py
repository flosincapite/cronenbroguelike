import random

import adventurelib

from cronenbroguelike import commands
from cronenbroguelike import npcs
from cronenbroguelike import rooms
from engine import actor
from engine import ai
from engine import directions
from engine.globals import G
from engine import say


def _create_rooms(number_of_rooms):
    return random.sample(rooms.all_rooms(), number_of_rooms)


def _get_random_start():
    # TODO: Condition this on how the last death actually occurred.
    cause_of_death = random.choice(
        [
            "being impaled",
            "slowly suffocating as a glabrous tentacle horror looks on",
        ]
    )
    for text in [
        f"The memory of {cause_of_death} fades away.",
        "You know only that you have been here for interminable years, "
        "that you have died innumerable times, and that someone once told "
        "you there was a way out. You were told this an eon ago, or maybe "
        "a day, but the stubborn hope of escape glisters in your mind.",
    ]:
        say.insayne(text)


def _start_game(_):

    # Creates the player character and ensures game will restart upon death.
    G.player = actor.create_actor(
        health=10,
        psyche=10,
        strength=10,
        stamina=10,
        will=10,
        wisdom=10,
        insanity=0,
        name="player",
    )
    G.player.log_stats = True
    G.player.upon_death(_start_game)

    # Creates a small dungeon.
    rooms = _create_rooms(4)
    last_exit = None
    last_room = None
    possible_exits = [
        directions.north,
        directions.south,
        directions.east,
        directions.west,
    ]
    for i, room in enumerate(rooms):
        #TODO: finish generalizing rooms here.
        if i == 0:
            G.current_room = room
        if last_room is not None:
            exits = [
                    exit
                    for exit in possible_exits
                    if exit is not last_exit]
            exit = random.choice(exits)
            room.add_exit(exit, last_room)
            last_exit = exit.opposite  # Tracks the exit that cannot be used for next room.
        last_room = room

    # Places a monster in a random room.
    occupied_room = random.choice(rooms)
    occupied_room.add_character(npcs.fish_man())
    occupied_room.add_character(npcs.mad_librarian())

    # Starts it up.
    _get_random_start()
    commands.enter_room(G.current_room)


_start_game(None)
G.player.upon_death(_start_game)
adventurelib.say("")  # Necessary for space before first prompt.
adventurelib.start()
