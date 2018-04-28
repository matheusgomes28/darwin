import sys
from PIL import Image
from PyQt4 import QtGui, QtCore, uic
import os, os.path, csv


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('eval_gui.ui', self)
        self.show()
        self.answers = []

        image_path = '../../images/preprocessed'
        self.images = [name for name in os.listdir(image_path) if os.path.isfile(image_path + name)]
        self.fileNum = len(self.images)
        self.fileCount = 0

        print('Number of files: {}'.format(self.fileNum))

        self.correctButton.clicked.connect(lambda: self.correct_image('Test'))
        self.nearButton.clicked.connect(lambda: self.near_image('Test'))
        self.incorrectButton.clicked.connect(lambda: self.incorrect_image('Test'))

        # Create a scene for the Graphics view
        self.sceneOriginal = QtGui.QGraphicsScene()
        self.original.setScene(self.sceneOriginal)

        # Loading with widget QImage
        image_data = open("img.jpg", "rb")
        image_widget = QtGui.QImage()   
        image_widget.loadFromData(bytes(image_data.read()))

        # Get the pixel map data
        px_map = QtGui.QPixmap.fromImage(image_widget)
        px_map_resized = px_map.scaledToHeight(350)
        graphics_obj = QtGui.QGraphicsPixmapItem(px_map_resized)
        self.sceneOriginal.addItem(graphics_obj)
        self.sceneOriginal.update()

    def correct_image(self, filename):
        self.update(filename, 1)

    def near_image(self, filename):
        self.update(filename, 2)

    def incorrect_image(self, filename):
        self.update(filename, 0)

    def update(self, filename, answer):
        print('Answer {}: {}'.format(self.fileCount + 1, answer))
        self.answers.append((filename, answer))

        self.fileCount += 1
        if self.fileCount > self.fileNum:
            with open('images.csv', 'w') as out:
                csv_out = csv.writer(out)
                csv_out.writerow(['filename', 'answer'])
                for row in self.answers:
                    csv_out.writerow(row)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

