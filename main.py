import sys
import os

import requests

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.Qt import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coord = 52.724508, 41.453693
        self.map_zoom = 21
        self.initUI()

    def getImage(self):
        map_request = f'http://static-maps.yandex.ru/1.x/?ll={self.coord[1]},{self.coord[0]}&z={self.map_zoom}&l=map'
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, 'wb') as pngfile:
            pngfile.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(30, 30)
        self.image.resize(540, 540)
        self.updateLabel()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp and self.map_zoom < 21:
            self.map_zoom += 1
            self.updateLabel()
        elif key == Qt.Key_PageDown and self.map_zoom >= 1:
            self.map_zoom -= 1
            self.updateLabel()

    def updateLabel(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
