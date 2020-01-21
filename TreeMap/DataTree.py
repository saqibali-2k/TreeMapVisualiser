from __future__ import annotations
from typing import Tuple, Optional

"""
Data Structure that represents the tree map diagram.

INVARIANTS: if self.children == [] then self.expanded == false
            len(self.build_map(width, height)) == len(self.get_categories())
"""


class DataTree:
    rect: Tuple[int, int, int, int]

    def __init__(self, name, size, category):
        # The subcategories
        self.children = []
        # Whether the subcategories should be shown
        self.expanded = False
        self.name = name
        # numerical data value (i.e total votes)
        self.size = size
        # categorical data (i.e riding winner)
        self.category = category
        self.rect = (0, 0, 0, 0)
        self.parent = None

    def _build_children_horizontally(self, start_x: float, start_y: float, width: float, height: float) -> None:
        curr_x, curr_y = start_x, start_y
        for child in self.children[:-1]:
            ratio = child.size / self.size
            child.build_map(curr_x, curr_y, round(width * ratio), height)
            curr_x += round(width * ratio)
        self.children[-1].build_map(curr_x, curr_y, start_x + width - curr_x, height)

    def _build_children_vertically(self, start_x: float, start_y: float, width: float, height: float) -> None:
        curr_x, curr_y = start_x, start_y
        for child in self.children[:-1]:
            ratio = child.size / self.size
            child.build_map(curr_x, curr_y, width, round(height * ratio))
            curr_y += round(height * ratio)
        self.children[-1].build_map(curr_x, curr_y, width, start_y + height - curr_y)

    """Builds rectangle coordinates for front-end
    """

    def build_map(self, start_x: int, start_y: int, width: int, height: int) -> None:
        if not self.expanded:
            self.rect = (start_x, start_y, width, height)
        elif len(self.children) != 0:
            self.rect = (start_x, start_y, width, height)
            if width > height:
                self._build_children_horizontally(start_x, start_y, width, height)
            else:
                self._build_children_vertically(start_x, start_y, width, height)

    def expand(self) -> None:
        if len(self.children) != 0:
            self.expanded = True

    def close_all(self) -> None:
        if len(self.children) != 0:
            self.expanded = False
            for child in self.children:
                child.close_all()

    def get_tree(self, x, y) -> DataTree:
        c = self.rect
                                 # start_x < x < start_x + width
        if not self.expanded and c[0] <= x <= c[2] + c[0] and c[1] <= y <= c[3] + c[1]:
            return self
        elif self.expanded:
            for child in self.children:
                potential_result = child.get_tree(x, y)
                if potential_result is not None:
                    return potential_result

    def get_rectangles(self) -> list:
        if not self.expanded:
            return [self.rect]
        else:
            lst = []
            for child in self.children:
                lst += child.get_rectangles()
            return lst

    def get_categories(self) -> list:
        if not self.expanded:
            return [self.category]
        else:
            lst = []
            for child in self.children:
                lst += child.get_categories()
            return lst

    def close_parent(self) -> None:
        if self.parent is not None:
            self.parent.expanded = False


def dict_to_tree(data: dict) -> Optional[DataTree]:
    if data == {}:
        return
    name = data['name']
    size = data['size']
    category = data['category']
    if data['subtrees'] == {}:
        return DataTree(name, size, category)
    else:
        root = DataTree(name, size, category)
        categories = {}
        for sub_dict in data['subtrees']:
            child = dict_to_tree(data['subtrees'][sub_dict])
            root.children.append(child)
            child.parent = root
            root.size += child.size
            if child.category not in categories:
                categories[child.category] = 0
            categories[child.category] += 1
        key_val = categories.popitem()
        highest_cat, highest_count = key_val[0], key_val[1]
        for cat in categories:
            if highest_count < categories[cat]:
                highest_count = categories[cat]
                highest_cat = cat
        root.category = highest_cat
        return root
