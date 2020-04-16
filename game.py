import pickle
import sys

import pygame as pg

from renderer import Renderer
from network import Network
from colors import *

class Game(object):
    def __init__(self):
        self.network = Network()
        self.mouse_pos = (0, 0)
        self.focus = None
        self.mouse_down = False
        self.keypresses = []

        self.renderer = Renderer(flags=pg.DOUBLEBUF|pg.HWSURFACE)

    def run(self):
        run = True
        while run:
            events = pg.event.get()

            if pg.QUIT in events:
                pg.quit()
                break

            self.mouse_pos = pg.mouse.get_pos()
            self.mouse_down = any(pg.mouse.get_pressed())
            self.key_presses = pg.key.get_pressed()

            reply = self.send_data()
            if reply != None:
                try:
                    mice_positions, components, hidden_area = reply
                except ValueError as e:
                    print(reply)
                    raise e
            else:
                continue

            self.focus = None
            all_components = sorted(components + hidden_area, key=lambda c: c.order, reverse=True)
            for component in all_components:
                if self.renderer.get_rect(component).collidepoint(self.mouse_pos):
                    self.focus = component
                    break
                
            self.renderer.clear_add_ons()
            if self.focus != None:
                self.renderer.draw_border(self.focus, color=(CYAN), margin=5)
            self.renderer.render(*all_components)
            self.renderer.draw_mice(self.mouse_pos, *mice_positions)
            self.renderer.show()

        sys.exit()

    def send_data(self):
        data = (self.mouse_pos, self.focus, self.mouse_down, self.keypresses)
        reply = self.network.send(data)
        return reply

if __name__ == "__main__":
    g = Game()
    g.run()
