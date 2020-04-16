import random
import copy

import pygame as pg

#from settings import *

SCALE = 2

def generate_stack(component, count): # generate a stack from passed component
    component.order = 0
    new_components = []

    last = component
    for i in range(count):
        new = copy.deepcopy(component)
        new.order = last.order + 1
        last = new
        new_components.append(new)

    return new_components

def id_generator():
    i = -1
    while True:
        i += 1
        yield i
identifier = id_generator()

class Component(object):
    def __init__(self, x, y, width=60 * SCALE, height=90 * SCALE, front="", back=""):
        self.x, self.y = x, y
        self.pos = x, y
        self.width, self.height = width, height
        self.front = front # path to front of component
        self.back = back # path to back of component
        self.is_face_up = True # if True, self.front is shown
        self.faces = {True: self.front, False: self.back} # maps is_face_up to a side
        self.image = self.faces.get(self.is_face_up)

        self.master = None # the player this component OR the Deck it belongs to

        self.order = 0 # order 0 means it is the bottom of any stack

        self.rect = None

        self.id = next(identifier)

    def flip(self):
        self.is_face_up = not self.is_face_up
        self.image = self.faces.get(self.is_face_up)

    def update(self, client_states, rect):
        if self.master == None:
            return
        for client in client_states:
            if id(client) == self.master:
                master = client
        if rect.collidepoint(client_states[master]["mousepos"]):
            self.x, self.y = client_states[master]["mousepos"]
        else:
            self.master = None
                
