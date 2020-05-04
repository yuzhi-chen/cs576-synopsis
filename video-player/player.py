from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtCore import Qt, QUrl, pyqtSignal
import os
import subprocess

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(0, 0, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):
        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        #create videowidget object

        videowidget = QVideoWidget()


        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)



        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)



        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)


        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        synopImageLayout = QHBoxLayout()
        synopImageLayout.setContentsMargins(1, 1, 1, 1)
        image1 = ClickLabel()
        pixmap = QPixmap('../test.jpg')
        image1.setPixmap(pixmap)
        image1.setFixedSize(100, 50)

        image1.clicked.connect(self.synopsis_click_handler)
        synopImageLayout.addWidget(image1)


        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        vboxLayout.addLayout(synopImageLayout)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)


        #media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)


    def open_file(self):

        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if os.path.splitext(filename)[1] == '.avi':
            output_name = os.path.dirname(filename) + '/output.mp4'
            print(output_name)
            convert_avi_to_mp4(filename, output_name)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(output_name)))
            self.playBtn.setEnabled(True)

        elif filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def synopsis_click_handler(self):
        self.mediaPlayer.setPosition(0)


def convert_avi_to_mp4(input_file, output_name):
    cmd = "ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input=input_file, output=output_name)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()


class ClickLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())