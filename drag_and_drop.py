from PyQt5.QtWidgets import (QPushButton, QWidget, QApplication, QProgressBar,
                             QTableWidget, QTableWidgetItem, QHBoxLayout,
                             QHeaderView, QLabel, QAbstractItemView)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import sys
from converter import available_formats, process
import os
import ntpath
import subprocess, os


def open_with_application(path):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', path))
    elif os.name == 'nt':  # For Windows
        os.startfile(path)
    elif os.name == 'posix':  # For Linux, Mac, etc.
        subprocess.call(('xdg-open', path))


class TableWidgetItem(QLabel):
    def __init__(self, parent, *args):
        resp = super().__init__(*args)
        self.parent = parent
        self.rowIndex = None
        return resp

    def mouseDoubleClickEvent(self, e):
        if self.rowIndex != None and self.parent.files[self.
                                                       rowIndex]['new_path']:
            open_with_application(self.parent.files[self.rowIndex]['new_path'])

    def setRowIndex(self, rowIndex):
        self.rowIndex = rowIndex


class ProgressBar(QProgressBar):
    def __init__(self, parent, *args):
        resp = super().__init__(parent, *args)
        self.parent = parent
        self.rowIndex = None
        return resp

    def mouseDoubleClickEvent(self, e):
        if self.rowIndex != None and self.parent.files[self.
                                                       rowIndex]['new_path']:
            open_with_application(self.parent.files[self.rowIndex]['new_path'])

    def setRowIndex(self, rowIndex):
        self.rowIndex = rowIndex


class Table(QTableWidget):
    def __init__(self, *args):
        resp = super().__init__(*args)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.files = {}
        return resp

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.setColumnWidth(0, self.width() * 0.5)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setColumnWidth(1, self.width() * 0.5 - 1)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.verticalHeader().setFixedWidth(0)

    def dragEnterEvent(self, e):
        valid = True
        for url in e.mimeData().urls():
            ext = os.path.splitext(url.fileName())[1]
            if not ext or ext[1:] not in available_formats or url.path(
            ) in self.files:
                valid = False
                break
        if valid:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        e.accept()
        urls = e.mimeData().urls()
        for url in urls:
            ext = os.path.splitext(url.fileName())[1]
            path = url.path()
            if os.name == 'nt' and path[0] == '/':
                path = path[1:]
            self.addFile(path)
            if not ext or ext[1:] not in available_formats:
                pass

    def dragMoveEvent(self, e):
        if (e.source() == self): e.ignore()
        else: e.accept()

    def dropMimeData(self, e):
        e.accept()

    def addFile(self, path):
        filename = ntpath.basename(path)
        rowsCount = self.rowCount()
        self.setRowCount(rowsCount + 1)
        self.files[rowsCount] = {'path': path, 'new_path': None}
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_item = TableWidgetItem(self, filename)
        self.setCellWidget(rowsCount, 0, table_item)
        pbar = ProgressBar(self)
        pbar.setRowIndex(rowsCount)
        table_item.setRowIndex(rowsCount)
        self.setCellWidget(rowsCount, 1, pbar)

        pbar.setValue(0)
        process(path, handler=pbar, files_status_handler=self.files[rowsCount])


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # self.button = QPushButton('Ընտրել', self)
        # self.button.move(100, 65)

        # self.pbar = QProgressBar(self)
        # self.pbar.setGeometry(5, -15, 290, 100)
        # layout = QHBoxLayout(self)

        self.table = Table(self)
        self.table.setGeometry(0, 0, 300, 150)
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Filename', 'Progress'])
        # self.table.setCellWidget(0, 0, QPushButton('This is button'))

        # layout.addWidget(self.table)
        # self.setLayout(layout)

        self.setWindowTitle('Armenian ANSI to Unicode')
        self.setGeometry(400, 300, 450, 400)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.table.resize(self.width(), self.height())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()
