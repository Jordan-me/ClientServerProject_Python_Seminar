import pickle
import socket
from _thread import *
import sys

# Unlimited games running at the same time, those games will be access by their id
from game import Game

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

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    """
    continually run while our client is still connected
    :param conn: stands for connection
    :return:
    """
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:  # check if the game still exist
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)  # the data is move

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game: ", gameId)
    except:
        pass

    idCount -=1
    conn.close()


# continuously look for connections
while True:
    # addr: IP address, conn: object describe what connected
    conn, addr = s.accept()  # accept any incoming connection
    print("Connected to:", addr)
    idCount += 1
    p = 0  # current player
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True  # the second player has connected to the game
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
