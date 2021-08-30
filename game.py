#!/usr/bin/env python3
import tcod


def main() -> None:
    # --- config settings ---
    screen_width = 80
    screen_height = 50
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)
    tileset = tcod.tileset.load_tilesheet(
        "data/img/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
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
            root_console.print(x=player_x, y=player_y, string="@")
            
            # --- update the screen ---
            context.present(root_console)

            # --- capture input ---
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()
