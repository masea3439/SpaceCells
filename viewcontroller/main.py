import pygame
from viewcontroller.visualiser import Visualiser
from model.game_map import GameMap
from viewcontroller.enemy_ai import PodManager
import time

test_env = False


def game_loop():
    """
    pr = cProfile.Profile()
    pr.enable()
    tick = 0
    """
    pygame.init()
    game_running = True
    game_map = GameMap(2000, 1600, 900)
    visualiser = Visualiser(1600, 900, game_map, 10)
    if test_env:
        pods = []
    else:
        pods = [PodManager(game_map, game_map.all_ships['pirate'][0:3]),
                PodManager(game_map, game_map.all_ships['pirate'][3:6]),
                PodManager(game_map, game_map.all_ships['pirate'][6:9])]
    right_mouse_pressed = False
    clicked_mouse_position = None
    fps = 60
    pod_update_time = 60
    last_frame_time = time.time()
    panned = False
    dragged = False
    paused = False

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
                clicked_mouse_position = game_map.screen_to_true(pygame.mouse.get_pos())
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
                    game_map.handel_order()
            panned = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if paused:
                    paused = False
                else:
                    paused = True

        elif event.type == pygame.MOUSEMOTION:
            if clicked_mouse_position is not None:
                dragged = True
            if right_mouse_pressed:
                game_map.pan(pygame.mouse.get_rel())
                panned = True
            else:
                #  update the location of the mouse for get_rel
                pygame.mouse.get_rel()

        if not paused:
            game_map.update()
            if pod_update_time == 0:
                for pod in pods:
                    pod.update()
                pod_update_time = 60
            else:
                pod_update_time -= 1
        visualiser.render_game(clicked_mouse_position)

        """
        tick += 1
        if tick == 1000:
            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            print(s.getvalue())
            game_running = False
        """


if __name__ == '__main__':
    game_loop()
