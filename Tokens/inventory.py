import copy
import pygame

class Inventory:

    def __init__(self):
        self.size = 32
        self.items = []
        self.quantities = []
        self.active_slots = 5
        for i in range(self.size):
            self.items.append(None)
            self.quantities.append(None)

    def add(self, item):
        
        if item in self.items:
            index = self.items.index(item)
            self.quantities[index] += 1
            return True
        else:
            for index, item in enumerate(self.items):
                if item is None:
                    self.items[index] = self.item
                    self.quantities[index] = 1
                    return True

        return False

    def render_bar(self, g):
        for i in range(self.active_slots):
            slot = pygame.Rect(400 + (i*80), 600, 80, 80)
            pygame.draw.rect(g, (255, 255, 255, 100), slot)

    def render_full(self, g):
        pass

    def use(self, index):

        if self.items[index] != None:
            item = self.items[index]
            self.quantities[index] -= 1
            
            if self.quantities[index] == 0:
                self.items[index] = None
                self.quantities[index] = None

            return copy.deepcopy(item)

        return None
