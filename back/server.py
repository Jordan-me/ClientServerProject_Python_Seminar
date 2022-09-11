import socket
from _thread import *
import pickle

from back.log_service import add_log_warnning, add_log_info
from back.game import Game


class Server:
    def __init__(self, players_connected={'id': []}, games={}, id_count=0):
        # initialize server parameters
        self.id_count = id_count
        self.players_connected = players_connected
        self.host = "localhost"
        self.port = 5555
        self.games = games


    def run(self):
        # start listening to socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host, self.port))
            add_log_info("Server: run, start listening to (" + str(self.host) + "," + str(self.port) + ")")
        except socket.error as e:
            add_log_warnning("Server: run, " + str(e))

        s.listen(2)
        add_log_info("Server: run, Waiting for a connection, Server Started")

        while True:
            # search for connection
            conn, addr = s.accept()
            self.players_connected['id'].append(addr)
            add_log_info("Server: run, got connection (" + str(conn) + "," + str(addr) + ")")
            self.id_count += 1
            p = 0
            game_id = (self.id_count - 1) // 2
            add_log_info("Server: run, access to game_id: " + str(game_id))
            if self.id_count % 2 == 1:
                self.games[game_id] = Game(game_id)
                add_log_info("Server: run, Creating a new game... " + str(game_id))
            else:
                # here we know we have two players
                add_log_info("Server: run, 2 players had connected to game_id: " + str(game_id) + " successfully")
                self.games[game_id].ready = True
                p = 1

            start_new_thread(self.threaded_client, (conn,addr, p, game_id))

    def threaded_client(self, conn,addr, p, game_id):
        conn.send(str.encode(str(p)))
        reply = ""
        while True:
            try:
                data = conn.recv(4096).decode()

                if game_id in self.games:
                    game = self.games[game_id]

                    if game.close:
                        break

                    if not data:
                        break
                    else:
                        if data == "reset":
                            game.resetWent()
                            add_log_info("Server: threaded_client, reset to game_id: " + str(game_id) + "successfully")
                        elif data[0] == 'N':  # Names
                            game.set_name(data[1:], p)
                            add_log_info(
                                "Server: threaded_client, got name for player " + str(p) + "in game_id: " + str(
                                    game_id) + "successfully")
                        elif data[0] == 'W':  # Winner
                            game.wins[int(data[1:])] += 1
                            add_log_info(
                                "Server: threaded_client, win added for player " + str(int(data[1:])) + "in game_id: " + str(
                                    game_id) + "successfully")
                        elif data[0] == 'Q':  # Quite
                            game.ready = False
                            add_log_info(
                                "Server: threaded_client, Quite action")
                        elif data != "get":
                            add_log_info(
                                "Server: threaded_client, get game requested - start play! + (game_id: " + str(game_id) + ")")
                            game.play(p, data)

                        conn.sendall(pickle.dumps(game))
                else:
                    break
            except:
                break

        add_log_info("Server: threaded_client, Lost connection (" + str(conn) + ", " + str(addr) + ")")

        conn.close()

if __name__ == "__main__":
    # when running client manually
    Server().run()
else:
    # when running server
    add_log_info("Server: server_main, entered to server.py file")

