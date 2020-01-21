from pygame import mouse
from CSVElectionInterpreter import *
from DataTree import *
from MapDrawer import *
import keyboard
import pygame
from DataTree import DataTree
PATH = 'data'
COLOR_ASSIGNMENTS = {'Green Party': (127, 255, 0), 'Conservative': (100, 149, 237), 'Liberal': (220, 20, 60),
                     'NDP': (255, 127, 80), 'Bloc Québécois': (255, 255, 255), 'other': (50, 50, 50)}


class View:
    def __init__(self):
        reader = CSVElectionInterpreter(PATH)
        formatted_info = reader.get_dict()
        tree = dict_to_tree(formatted_info)
        self.drawer = MapDrawer(tree, COLOR_ASSIGNMENTS)

    def loop(self):
        running = True
        pygame.display.update()
        pos = None
        self.drawer.update_map()
        self.drawer.draw_rectangles()
        while running:
            self.drawer.update_screen()
            all_events = pygame.event.get()
            for event in all_events:
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[0] <= 500:
                        self.drawer.update_text(pos[0], pos[1])
            if keyboard.is_pressed('o'):
                # enlarge
                if pos is not None:
                    self.drawer.enlarge(pos[0], pos[1])
                    print('1')
                pos = None
            elif keyboard.is_pressed('q'):
                # close tree
                print('2')
                self.drawer.close_all()
                self.drawer.draw_rectangles()
                pos = None
            elif keyboard.is_pressed('e'):
                # expand
                if pos is not None:
                    self.drawer.expand(pos[0], pos[1])
                    self.drawer.update_map()
                    self.drawer.draw_rectangles()
                    pos = None
            elif keyboard.is_pressed('z'):
                running = False


v = View()
v.loop()

