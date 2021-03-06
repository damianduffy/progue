"""
Handle the loading and initialisation of game sessions.
"""

from __future__ import annotations

import copy
import lzma
import pickle

import color
from engine import Engine
import entity_factories
from game_map import GameWorld


def new_game() -> Engine:
    """
    Return a new game session as an Engine instance
    """
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # --- Create the player character ---
    # Note I can't use spawn() because it requires a GameMap which isn't created and which itself requires Player
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine, 
        max_rooms=max_rooms, 
        room_min_size=room_min_size, 
        room_max_size=room_max_size, 
        map_width=map_width, 
        map_height=map_height, 
    )
    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    """
    Equip the starting equipment for the player.
    """
    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine

def load_game(filename: str) -> Engine:
    """ Load an engine instance from a file. """
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine