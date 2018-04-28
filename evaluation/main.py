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

        image_path = 'original/'
        self.images = [name for name in os.listdir(image_path) if os.path.isfile(image_path + name)]
        self.fileNum = len(self.images)
        self.fileCount = 0

        print('Number of files: {}'.format(self.fileNum))

        self.correctButton.clicked.connect(lambda: self.correct_image('Test'))
        self.nearButton.clicked.connect(lambda: self.near_image('Test'))
        self.incorrectButton.clicked.connect(lambda: self.incorrect_image('Test'))

        img1_scene = QtGui.GraphicsScene()
        self.original.setScene(img1_scene)
        img = Image.open(self.images[0])
        view = QtGui.GraphicsView(img1_scene)

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

