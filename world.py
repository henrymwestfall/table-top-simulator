import random

from components import Component
from renderer import Renderer

class World(object):
    def __init__(self, game_name):
        self.game_name = game_name
        self.public_components = []
        self.hidden_areas = {}
        self.client_mice = {}
        self.holding_something = {}

        self.renderer = Renderer()

        self.load_game()

    def load_game(self):
        back = "./Dominion/card_back.png"
        path = lambda name: f"./Dominion/{name}.png"
        
        for i in range(60):
            component = Component(65, 95, front=path("copper"), back=back)
            component.order = i
            self.public_components.append(component)
        for i in range(40):
            component = Component(190, 95, front=path("silver"), back=back)
            component.order = i
            self.public_components.append(component)
        for i in range(30):
            component = Component(315, 95, front=path("gold"), back=back)
            component.order = i
            self.public_components.append(component)

        for i in range(8):
            component = Component(65, 280, front=path("estate"), back=back)
            component.order = i
            self.public_components.append(component)
        for i in range(8):
            component = Component(190, 280, front=path("duchy"), back=back)
            component.order = i
            self.public_components.append(component)
        for i in range(8):
            component = Component(315, 280, front=path("province"), back=back)
            component.order = i
            self.public_components.append(component)

        for i in range(10):
            component = Component(65, 465, front=path("curse"), back=back)
            component.order = i
            self.public_components.append(component)
        component = Component(315, 465, front=path("trash"), back=back)
        component.order = 0
        self.public_components.append(component)
        
            
        
    def new_client(self, client):
        self.hidden_areas[client] = []
        self.holding_something[client] = False
        self.client_mice[client] = (0, 0)

    def get_order(self, component):
        return component.order

    def update(self, client_states):
        for client in client_states:
            self.client_mice[client] = client_states[client]["mousepos"]
            
            client_side_focus = client_states[client]["focus"]
            focus = None
            if client_side_focus != None:
                for component in self.public_components + self.hidden_areas[client]:
                    if component.id == client_side_focus.id:
                        focus = component
            
            if focus == None:
                continue
            elif not client_states[client]["mousedown"]: # focus exists, mouse is up
                focus_rect = self.renderer.get_rect(focus)
                if focus.master == id(client): # dropped it
                    highest = -1
                    for component in self.public_components + self.hidden_areas[client]:
                        if component.id == focus.id:
                            continue
                        component_rect = self.renderer.get_rect(component)
                        if component_rect.colliderect(focus_rect) and component.order > highest:
                            highest = component.order
                    focus.order = highest + 1
                    focus.master = None
            else: # focus exists, mouse is down
                #print(focus in self.public_components)
                focus.master = id(client)
                focus.order = float('inf')
        components = self.public_components.copy()
        for hidden_area in self.hidden_areas.values():
            components += hidden_area
        for component in components:
            component.update(client_states, self.renderer.get_rect(component))
