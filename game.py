#!/usr/bin/env python3
import traceback
from numpy import save

import tcod

import color
import exceptions
import input_handlers


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """
    If the current event handler has an active engine, then save it.
    """
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def toggle_fullscreen(context: tcod.context.Context) -> None:
    """Toggle a context window between fullscreen and windowed modes."""
    if not context.sdl_window_p:
        return
    fullscreen = tcod.lib.SDL_GetWindowFlags(context.sdl_window_p) & (
        tcod.lib.SDL_WINDOW_FULLSCREEN | tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP
    )
    tcod.lib.SDL_SetWindowFullscreen(
        context.sdl_window_p,
        0 if fullscreen else tcod.lib.SDL_WINDOW_FULLSCREEN_DESKTOP,
    )

def main() -> None:
    # --- config settings ---
    screen_width = 80
    screen_height = 50
    
    tileset = tcod.tileset.load_tilesheet(
        "data/img/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    # Setup the event handler (set to the main menu to start new game/load game/etc.).
    handler: input_handlers.BaseEventHandler = input_handlers.MainMenu()

    # --- generate the console ---
    with tcod.context.new_terminal(
        screen_width, 
        screen_height, 
        tileset = tileset,
        title = "My First Roguelike",
        vsync = True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # FIXME - temporarily forcing to fullscreen while testing.
        # toggle_fullscreen should probably live in engine.py
        # Going fullscreen should be controled by a CLI flag and also in-game options menu
        toggle_fullscreen(context)
        # --- main game loop ---
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
