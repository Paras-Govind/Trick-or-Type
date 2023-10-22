import random
import socket
import select
from config import port

class GameServer(object):
    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to localhost - set to external ip to connect from other computers
        self.listener.bind(("127.0.0.1", port))
        self.read_list = [self.listener]
        self.write_list = []
        
        self.stepsize = 5
        self.clients = {}
        self.rooms = {}

    def send(self, message, addr):
        self.listener.sendto(bytes(message, "utf-8"), addr)
        
    def run(self):
        print ("Waiting...")
        try:
            while True:
                readable, writable, exceptional = (
                    select.select(self.read_list, self.write_list, [])
                    )
                for f in readable:
                    if f is self.listener:
                        msg, addr = f.recvfrom(32)
                        msg = msg.decode("utf-8")
                        print(f"Received message: {msg}")
                        if len(msg) >= 1:
                            cmd = msg[0]
                            if cmd == "c":  # New Connection
                                self.clients[addr] = msg[1:]
                                print("New client")
                            elif cmd == "m":  # Message
                                if len(msg) >= 2:
                                    msg_type = msg[1]
                                    if msg_type == "c" and addr in self.clients:
                                        while True:
                                            room_code = random.randint(10000, 99999)
                                            if room_code not in self.rooms.keys():
                                                self.rooms[room_code] = [addr]
                                                break
                                        self.send(f"mc{room_code}", addr)
                                    elif msg_type == "j" and addr in self.clients:
                                        room_code = int(msg[2:])
                                        print(f"Valid room code: {room_code in self.rooms.keys()}")
                                        print(f"Room has space: {len(self.rooms[room_code]) < 2}")
                                        if room_code in self.rooms.keys() and len(self.rooms[room_code]) < 2:
                                            self.rooms[room_code].append(addr)
                                            self.send(f"mj{room_code}", addr)
                                            print(f"Sent mj{room_code}")
                                        else:
                                            self.send(f"me{room_code}", addr)
                                            print(f"Sent me{room_code}")
                                    elif msg_type == "s" and addr in self.clients:
                                        room_code = int(msg[2:])
                                        for player in self.rooms[room_code]:
                                            self.send(f"ms{room_code}", player)
                                            print(f"Sent ms{room_code}")
                                    elif msg_type == "n" and addr in self.clients:
                                        room_code = int(msg[2:])
                                        for player in self.rooms[room_code]:
                                            if player != addr:
                                                self.send(f"mn", player)
                                                print(f"Sent mn")
                            elif cmd == "d":  # Player Quitting
                                if addr in self.clients:
                                    del self.clients[addr]
                            else:
                                print ("Unexpected: {0}".format(msg))
        except KeyboardInterrupt:
            print("Interupted")
            return

if __name__ == "__main__":
    g = GameServer()
    g.run()