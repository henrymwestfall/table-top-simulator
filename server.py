import socket
import pickle
from threading import *
import sys

from world import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '172.16.1.12'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection")

currentId = 0

world = World("Dominion")
client_states = {}
connected_players = 0

def threaded_client(client):
    global connected_players
    data = pickle.dumps(currentId)  
    client.send(data)
    _ = client.recv(2048)

    world.hidden_areas[client] = []
    hidden_area = world.hidden_areas[client]

    client_states[client] = {"mousepos": (0,0), "focus": None, "mousedown": False, "keypresses": []}

    connected_players += 1
    
    while True:
        try:
            data = pickle.dumps((tuple(world.client_mice.values()), world.public_components, hidden_area))
            client.send(data)
            
            data = client.recv(2048)

            if not data:
                client.send(str.encode("Goodbye"))
                break
            else:
                mouse_pos, focus, mouse_down, keypresses = pickle.loads(data)
                client_states[client]["mousepos"] = mouse_pos
                client_states[client]["focus"] = focus
                client_states[client]["mousedown"] = mouse_down
                client_states[client]["keypresses"] = keypresses

        except Exception as e:
            print(str(e))
            break
    print("Lost connection")
    del client_states[client]
    client.close()

def server_thread():
    while True:
        if connected_players == 0:
            continue

        world.update(client_states)

t = Thread(target=server_thread)
t.start()

while True:
    try:
        conn, addr = s.accept()
    except KeyboardInterrupt as e:
        print("Server stopped")
        raise e
    print("Connected to: ", addr)

    t = Thread(target=threaded_client, args=(conn,))
    t.start()
