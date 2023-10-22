import random
import socket
import select
from config import port
import pygame.event

class Network(object):
    def  __init__(self, addr="127.0.0.1"):
        self.clientport = random.randrange(8000, 8999)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to localhost - set to external ip to connect from other computers
        self.conn.bind(("127.0.0.1", self.clientport))
        self.addr = addr
        self.serverport = port
        
        self.read_list = [self.conn]
        self.write_list = []
        
        self.create_room_event = pygame.USEREVENT + 1
        self.join_room_event = pygame.USEREVENT + 2
        self.start_event = pygame.USEREVENT + 3
        
        self.next_phrase_event = pygame.USEREVENT + 4
        self.finish_event = pygame.USEREVENT + 5
        self.error_event = pygame.USEREVENT + 6
        
    def send(self, message):
        print(f"Sending message: {message}")
        self.conn.sendto(bytes(message, "utf-8"), (self.addr, self.serverport))
        
    def check_network(self):
        readable, writable, exceptional = (
                select.select(self.read_list, self.write_list, [], 0)
            )
        for f in readable:
            if f is self.conn:
                msg, addr = f.recvfrom(32)
                msg = msg.decode("utf-8")
                if len(msg) >= 1:
                    cmd = msg[0]
                    if cmd == "m":  # Message
                        if len(msg) >= 2:
                            msg_type = msg[1]
                            if msg_type == "c":
                                room_code=int(msg[2:])
                                pygame.event.post(pygame.event.Event(self.create_room_event, room_code=room_code))
                            elif msg_type == "j":
                                room_code=int(msg[2:])
                                pygame.event.post(pygame.event.Event(self.join_room_event, room_code=room_code))
                            elif msg_type == "s":
                                pygame.event.post(pygame.event.Event(self.start_event))
                    else:
                        print ("Unexpected: {0}".format(msg))