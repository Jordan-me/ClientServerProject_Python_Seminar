import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QVBoxLayout, QTableWidget, QPushButton, \
    QTableWidgetSelectionRange


# date|player 1 name|player 2 name|score|winner
class Table(QTableWidget):
    def __init__(self, warning_msg):
        QTableWidget.__init__(self)
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.current_free_index = 0
        self.rows = {}
        self.tableWidget.doubleClicked.connect(self.getSelectedRowData)
        self.selectedRow = -1
        self.warning_msg = warning_msg

    def set_cols(self, cols=[]):
        col_index = 0
        self.tableWidget.setColumnCount(len(cols))
        for name in cols:
            self.tableWidget.setHorizontalHeaderItem(col_index, QTableWidgetItem(name))
            col_index += 1

    def add_row(self, row=[]):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)  # adding a new row
        for i in range(len(row)):
            item = QTableWidgetItem(row[i])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(self.current_free_index, i, item)

    def getSelectedRowData(self):
        self.warning_msg.hide()
        for currentItem in self.tableWidget.selectedItems():
            self.tableWidget.setRangeSelected(
                QTableWidgetSelectionRange(currentItem.row(), 0, currentItem.row(), self.tableWidget.columnCount() - 1),
                1)
            self.selectedRow = currentItem.row()

    def update_row(self, entry_index, row):
        for i in range(len(row)):
            item = QTableWidgetItem(row[i])
            self.tableWidget.setItem(entry_index, i, QTableWidgetItem(row[i]))

    def disable_row(self):
        # check which row has selected
        game_id = -1
        if self.selectedRow == -1:
            self.warning_msg.setText("Please select game to close [Double-Click on row]")
            self.warning_msg.show()
        elif self.rows[self.selectedRow].close:
            self.warning_msg.setText("This Game already closed")
            self.warning_msg.show()
        else:
            self.warning_msg.hide()
            game_id = self.rows[self.selectedRow].id
            self.selectedRow = -1
        return game_id

    def getIdByRowIndex(self, row_index):
        for k, v in self.rows.items():
            if v[0] == row_index:
                return k
    def isFound(self,game):
        for key in self.rows:
            if self.rows[key].isEqual(game):
                return key
        return -1


    def update_data(self, new_data):
        for i in range(len(new_data)):
            game = new_data[i]
            index = self.isFound(game)
            if index == -1:
                self.rows[self.current_free_index] = game
                self.add_row([game.time_created, game.p1Name, game.p2Name, str(game.wins), game.getWinnerName()])
                self.current_free_index += 1
            else:
                self.update_row(index,
                                [game.time_created, game.p1Name, game.p2Name, str(game.wins), game.getWinnerName()])

        self.tableWidget.update()
