#!/usr/bin/env python3
import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def main() -> None:
    # --- config settings ---
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    
    tileset = tcod.tileset.load_tilesheet(
        "data/img/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    event_handler = EventHandler()

    # --- generate the characters ---
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {player, npc}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    # --- generate the console ---
    with tcod.context.new_terminal(
        screen_width, 
        screen_height, 
        tileset = tileset,
        title = "My First Roguelike",
        vsync = True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # --- main game loop ---
        while True:
            # --- draw to screen ---
            engine.render(console=root_console, context=context)
            
            # --- get input ---
            events = tcod.event.wait()

            # --- process input ---
            engine.handle_events(events)


if __name__ == "__main__":
    main()
