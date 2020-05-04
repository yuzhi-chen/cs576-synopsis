from random import shuffle
from PySide import QtCore, QtGui

class ClickableLabel(QtGui.QLabel):
    clicked = QtCore.Signal(str)

    def __init__(self, width, height, color):
        super(ClickableLabel, self).__init__()
        pixmap = QtGui.QPixmap(width, height)
        pixmap.fill(QtGui.QColor(color))
        self.setPixmap(pixmap)
        self.setObjectName(color)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QGridLayout(self)
        colors = 'red green blue orange purple yellow'.split()
        for row in range(len(colors)):
            shuffle(colors)
            for column, color in enumerate(colors):
                label = ClickableLabel(25, 25, color)
                label.clicked.connect(self.handleLabelClicked)
                layout.addWidget(label, row, column)

    def handleLabelClicked(self, name):
        print('"%s" clicked' % name)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 200, 200)
    window.show()
    sys.exit(app.exec_())