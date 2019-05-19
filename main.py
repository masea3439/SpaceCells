# Commit message change
import pygame
from visualiser import Visualiser
from game_map import GameMap
import time


def game_loop():
    game_running = True
    game_map = GameMap(2000, 1600, 900)
    visualiser = Visualiser(1600, 900, game_map, 10)
    pygame.init()
    right_mouse_pressed = False
    clicked_mouse_position = None
    fps = 60
    last_frame_time = time.time()
    panned = False
    dragged = False

    # The game loop
    while game_running:
        # Only run the game loop fps times per second
        current_time = time.time()
        sleep_time = 1. / fps - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
        last_frame_time = time.time()

        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            game_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Unselect currently selected ships
                game_map.unselect()
                clicked_mouse_position = pygame.mouse.get_pos()
                clicked_mouse_position = game_map.screen_to_true(clicked_mouse_position)
                dragged = False
            elif event.button == 3:
                right_mouse_pressed = True
            elif event.button == 5:
                game_map.change_zoom(-0.1)
            elif event.button == 4:
                game_map.change_zoom(0.1)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # Check if ships are selected
                if not dragged:
                    game_map.check_selection_click(clicked_mouse_position)

                elif clicked_mouse_position is not None:
                    game_map.check_selection_box(clicked_mouse_position)
                clicked_mouse_position = None
            elif event.button == 3:
                right_mouse_pressed = False
                if not panned:
                    game_map.set_destination()
            panned = False

        elif event.type == pygame.MOUSEMOTION:
            if clicked_mouse_position is not None:
                dragged = True
            if right_mouse_pressed:
                game_map.pan(pygame.mouse.get_rel())
                panned = True
            else:
                #  update the location of the mouse for get_rel
                pygame.mouse.get_rel()

        game_map.update()
        visualiser.render_game(clicked_mouse_position)


if __name__ == '__main__':
    game_loop()