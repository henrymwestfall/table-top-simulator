import pygame as pg

from colors import *

class Renderer(object):
    def __init__(self, flags=0):
        self.screen = pg.display.set_mode((1200, 600), flags=flags)
        self.image_cache = {}
        self.client_add_ons = {"below": {}, "above": {}}

        self.mouse_colors = [RED, BLUE, GREEN, YELLOW, MAGENTA]

    def clear_add_ons(self):
        self.client_add_ons = {"below": {}, "above": {}}

    def get_image(self, element):
        image = self.image_cache.get(element.image, None)
        if image == None:
            image = pg.image.load(element.image)
            self.image_cache[element.image] = image
        image = pg.transform.scale(image, (element.width, element.height))
        return image

    def get_rect(self, element, image=None):
        if image == None:
            image = self.get_image(element)
        rect = image.get_rect()
        rect.center = element.x, element.y
        return rect

    def draw_border(self, element, color, margin):
        elem_rect = self.get_rect(element)
        image = pg.Surface([elem_rect.width + 2 * margin, elem_rect.height + 2 * margin])
        image.fill(color)
        rect = image.get_rect()
        rect.centerx, rect.centery = elem_rect.centerx, elem_rect.centery

        try:
            self.client_add_ons["below"][element].append((image, rect))
        except KeyError:
            self.client_add_ons["below"][element] = [(image, rect)]
           
    def render(self, *elements):
        self.screen.fill(WHITE)
        sorted_elements = sorted(elements, key=lambda e: e.order)
        for element in sorted_elements:
            if element in self.client_add_ons["below"]:
                for add_on in self.client_add_ons["below"][element]:
                    image, rect = add_on
                    self.screen.blit(image, rect)

            image = self.get_image(element)
            rect = self.get_rect(element, image)
            self.screen.blit(image, rect)
            
            if element in self.client_add_ons["above"]:
                for add_on in self.client_add_ons["above"][element]:
                    image, rect = add_on
                    self.screen.blit(image, rect)

    def draw_mice(self, client_mouse_pos, *mice_positions):
        for i, mouse_pos in enumerate(mice_positions):
            if client_mouse_pos == mouse_pos:
                continue
            else:
                pg.draw.circle(self.screen, self.mouse_colors[i], mouse_pos, 5)

    def show(self):
        pg.display.flip()
            
