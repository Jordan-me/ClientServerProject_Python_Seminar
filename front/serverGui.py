import multiprocessing
import sched
import threading
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton

from back.log_service import add_log_info, load_from_file, add_log_warnning, write_to_file
from back.server import Server
from front.client import Client
from front.widgets.table import Table


class ServerGui:
    def __init__(self, argv=None, width=650, height=400):
        # define base window & total layout
        self.app = QApplication(argv)
        self.qwidget = QWidget()
        self.qwidget.setWindowTitle("Server Gui")
        self.qwidget.resize(width, height)
        self.server_layout = QVBoxLayout()
        # define first horizontal layout
        self.h_layout = QHBoxLayout()
        self.name = QLineEdit()
        self.warning = QLabel('')
        self.warning.hide()
        self.name.mousePressEvent = self.clickLine
        self.add_player_btn = QPushButton("Add Player")
        self.add_player_btn.clicked.connect(self.add_player_to_game)
        self.add_player_btn.setStyleSheet(
            "border-style: outset;min-width: 10em;min-height: 1.5em; font: bold 14px;border-radius: "
            "10px;border-color: beige; background: #82E0AA ; border-color: beige;")
        self.h_layout.addWidget(self.name)
        self.h_layout.addWidget(self.add_player_btn)
        self.h_layout.addWidget(self.warning)
        self.server_layout.addLayout(self.h_layout)

        # define vbox layout for leaderboard table
        self.v_layout = QVBoxLayout()
        self.warning_table = QLabel('')
        self.warning_table.hide()
        self.table = Table(self.warning_table)
        self.table.set_cols(["Date", "Player 1", "Player 2", "Score", "Winner"])
        self.close_game_btn = QPushButton("Close Game")
        self.close_game_btn.clicked.connect(self.close_game)
        self.close_game_btn.setStyleSheet(
            "border-style: outset;min-width: 10em;min-height: 2em; font: bold 14px;border-radius: "
            "10px;border-color: beige; background: #F1948A ; border-color: beige;")
        self.close_server_btn = QPushButton("Exit")
        self.close_server_btn.clicked.connect(self.exit)
        self.close_server_btn.setStyleSheet(
            "border-style: outset;min-width: 10em;min-height: 2em; font: bold 14px;border-radius: "
            "10px;border-color: beige; background: #F1948A ; border-color: beige;")
        self.h_layout_bottom = QHBoxLayout()
        self.h_layout_bottom.addWidget(self.close_game_btn)
        self.h_layout_bottom.addWidget(self.close_server_btn)
        self.v_layout.addWidget(self.warning_table)
        self.v_layout.addWidget(self.table.tableWidget)
        self.v_layout.addLayout(self.h_layout_bottom)

        self.server_layout.addLayout(self.v_layout)
        self.qwidget.setLayout(self.server_layout)
        self.qwidget.show()
        self.players_connected, self.games, self.id_count = load_from_file()
        self.server = Server(self.players_connected, self.games, self.id_count)
        self.server_thread = threading.Thread(
            target=self.server.run)
        # activate server's thread
        self.server_thread.start()
        add_log_info("ServerGui: server started successfully")

        self.table_thread = threading.Thread(
            target=self.update_view)
        self.table.update_data(self.games)
        self.table_thread.start()

    def update_view(self):
        while True:
            time.sleep(1)
            self.table.update_data(self.server.games)

    def clickLine(self, mouseEvent):
        self.warning.hide()
        self.name.setPlaceholderText("Type your name")

    def add_player_to_game(self):
        txt = self.name.text()
        txt = txt.replace(' ', '_')
        if len(txt) != 0 and txt.replace('_', '').isalpha():
            # if the names are not the same
            self.name.setText('')
            create_player_process(txt)

            add_log_info("ServerGui: add_player_to_game, player " + txt + "added successfully")
            self.warning.setText(txt + " wait for game to start")
            self.warning.show()
            add_log_info("ServerGui: add_player_to_game, open client for player " + txt)
        else:
            add_log_info("ServerGui: add_player_to_game, must required a valid name")
            self.warning.setText("Please type a valid name")
            self.warning.show()

    def close_game(self):
        game_id = self.table.disable_row()
        if game_id != -1:
            self.server.games[game_id].close = True
            add_log_info("ServerGui: close_game, GameID = " + str(game_id) + " has selected to be close")
        else:
            add_log_info("ServerGui: close_game, No game has been chosen to close")

    def exit(self):
        """
        closing all connections and closing the app
        """
        # write to file all the games from table
        write_to_file(self.server.players_connected, self.server.games)
        # Close all open games
        add_log_info("ServerGui: exit, Preparing close all games")
        for game_id in self.server.games:
            self.server.games[game_id].close = True
        add_log_info("ServerGui: exit, all the open games closed successfully")
        # Close server thread
        add_log_info("ServerGui: exit, Preparing close server thread")

        super().exit_app()


def create_player_process(name):
    """
    creating and starting new game process
    :param player_new: player object
    """
    add_log_info("ServerGui: create_player_process, open client for"+name +" successfully")
    player_process = multiprocessing.Process(target=Client, args=(name,))
    player_process.start()
