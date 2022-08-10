import pickle
import socket
from _thread import *
import sys

# localhost- we are only gonna able to connect over our local network (only who is on our Wi-Fi network)
from player import Player

server = "192.168.1.178"
port = 5555

# initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Type of connection

try:
    # setting up a connection
    s.bind((server, port))
except socket.error as e:
    str(e)

# listening for the connection
s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

def threaded_client(conn, player):
    """
    continually run while our client is still connected
    :param conn: stands for connection
    :return:
    """
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # 2048: amount of information I trying to receive
            players[player] = data
            # reply = data.decode("utf-8")  # sending an info over a client server system we have to encode the info
            if not data:
                print("Disconnected")
                break
            else:
                print("Player: ",player)
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            # encode string into bytes object
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


current_player = 0

# continuously look for connections
while True:
    # addr: IP address, conn: object describe what connected
    conn, addr = s.accept()  # accept any incoming connection
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
