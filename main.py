import sys
import os

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coord = 52.724508, 41.453693
        self.map_zoom = 18
        self.getImage()
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

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(30, 30)
        self.image.resize(540, 540)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
