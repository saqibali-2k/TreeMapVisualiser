from pygame import draw, display, font
from typing import List, Dict

from DataTree import DataTree
from pygame.locals import *


class MapDrawer:
    tree: DataTree
    assignments: Dict[str, tuple]

    def __init__(self, tree: DataTree, assignments: Dict[str, tuple]):
        self.assignments = assignments
        self.root_tree = tree
        self.curr_tree = tree
        self.WIDTH = 500
        self.HEIGHT = 500
        self.DISPLAY = display.set_mode((self.WIDTH + 450, self.HEIGHT), 0, 32)
        tree.build_map(0, 0, self.WIDTH, self.HEIGHT)
        # Display the tutorial information
        font.init()
        tutorial = font.SysFont('Comic Sans MS', 15)
        tut1 = "Press q to reset."
        tut2 = "Press e to expand"
        tut3 = "Press o to enlarge"

        tut1_surface = tutorial.render(tut1, False, (255, 255, 255))
        tut2_surface = tutorial.render(tut2, False, (255, 255, 255))
        tut3_surface = tutorial.render(tut3, False, (255, 255, 255))
        self.DISPLAY.blit(tut1_surface, (530, 440))
        self.DISPLAY.blit(tut2_surface, (530, 460))
        self.DISPLAY.blit(tut3_surface, (530, 480))

    def set_cat_colors(self, colour_assign: dict):
        self.assignments = colour_assign

    def update_map(self):
        self.curr_tree.build_map(0, 0, self.WIDTH, self.HEIGHT)

    def update_screen(self):
        display.update()

    def draw_rectangles(self):
        rectangles = self.curr_tree.get_rectangles()
        categories = self.curr_tree.get_categories()
        print(rectangles)
        assert len(rectangles) == len(categories)
        for rect, cat in zip(rectangles, categories):
            curr_color = (169, 169, 169)  # GREY
            if cat in self.assignments:
                curr_color = self.assignments[cat]
            draw.rect(self.DISPLAY, curr_color, rect)
            draw.rect(self.DISPLAY, (0, 0, 0), rect, 1)

    def expand(self, x, y):
        target = self.curr_tree.get_tree(x, y)
        target.expand()

    def enlarge(self, x, y):
        target = self.curr_tree.get_tree(x, y)
        self.curr_tree = target
        target.build_map(0, 0, self.WIDTH, self.HEIGHT)
        self.draw_rectangles()

    def close_all(self):
        self.root_tree.close_all()
        self.curr_tree = self.root_tree

    def update_text(self, x, y) -> None:
        draw.rect(self.DISPLAY, (0, 0, 0), (510, 0, 440, 400))
        information = font.SysFont('Comic Sans MS', 16)
        target = self.curr_tree.get_tree(x, y)
        name = "Name: " + target.name
        size = "Size: " + str(target.size)
        category = "Category: " + target.category

        name_surface = information.render(name, False, (255, 255, 255))
        size_surface = information.render(size, False, (255, 255, 255))
        category_surface = information.render(category, False, (255, 255, 255))
        self.DISPLAY.blit(name_surface, (530, 20))
        self.DISPLAY.blit(size_surface, (530, 40))
        self.DISPLAY.blit(category_surface, (530, 60))

    def close_parent(self, x, y):
        target = self.curr_tree.get_tree(x, y)
        target.close_parent()
        self.draw_rectangles()