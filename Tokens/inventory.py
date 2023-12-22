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
            for index, slot in enumerate(self.items):
                if slot is None:
                    self.items[index] = item
                    self.quantities[index] = 1
                    return True

        return False

    def render_bar(self, g):
        for i in range(self.active_slots):
            x = 400 + (i*90)
            y = 600
            slot = pygame.Rect(x, y, 80, 80)
            pygame.draw.rect(g, (255, 255, 255, 100), slot)
            if self.items[i] != None:
                slot = pygame.Rect(x + 15, y + 15, 50, 50)
                pygame.draw.rect(g, (0,0,0), slot)
                
                font = pygame.font.SysFont("Arial", 20)
                txt = font.render(str(self.quantities[i]), True, (0,0,0))
                g.blit(txt, (x+2, y + 60))


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
