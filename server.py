import socket
from _thread import *
import pickle
from server_gui import server_gui
import pygame

from game import Game

server = "localhost"
port = 5555
connectedAccounts = {'id': []}

# pygame.font.init()
start_new_thread(server_gui, (0, 0, 0))
# width = 700
# height = 700
# win = pygame.display.set_mode((width, height))
# pygame.display.set_caption("Server")
# win.blit("asd", (400, 350))
# pygame.display.update()

# while True:
#     pygame.display.update()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


# def server_gui():

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    server_gui.set_gui_con(conn, gameId)
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:

    # pygame.display.update()

    # test()
    conn, addr = s.accept()
    # start_new_thread(test, (conn, 0, 1))
    connectedAccounts['id'].append(addr)
    print("Connected to:", addr)
    print(connectedAccounts)
    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    print("gameid: " + str(gameId))

    if idCount % 2 == 1:
        print("gameid: " +str(gameId))
        games[gameId] = Game(gameId)
        print("Creating a new game..." + str(gameId))
        server_gui.set_players(connectedAccounts['id'][idCount - 1], 0, gameId, conn)
    else:
        # here we know we have two players
        print("id count: " +str(idCount))

        server_gui.set_players(connectedAccounts['id'][idCount - 2], connectedAccounts['id'][idCount-1], gameId, conn)
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
