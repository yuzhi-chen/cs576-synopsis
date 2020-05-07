from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QBrush
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QSignalMapper
import os
import subprocess
from pathlib import Path

dirname = os.path.dirname(__file__)
parent_dir = Path(__file__).parent.parent

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Media Player")
        self.setGeometry(0, 0, 700, 600)
        self.setWindowIcon(QIcon('player.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.init_ui()
        self.show()
        self.audio_process = False
        self.position = 0
        self.filename = '.'

    def init_ui(self):
        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        #create videowidget object

        videoHboxLayout = QHBoxLayout()
        self.videowidget = QVideoWidget()
        self.videowidget.setFixedHeight(300)
        self.videowidget.setFixedWidth(352)

        self.imagewidget = QLabel()
        self.imagewidget.setFixedWidth(352)
        self.imagewidget.setFixedHeight(300)

        videoHboxLayout.addWidget(self.videowidget)
        videoHboxLayout.addWidget(self.imagewidget)
        videoHboxLayout.setContentsMargins(0, 0, 0, 0)
        videoHboxLayout.setSpacing(0)

        #create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)



        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)


        self.stopBtn = QPushButton()
        self.stopBtn.setEnabled(False)
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.reset_video)


        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.stopBtn)

        synopLayout = QVBoxLayout()
        synopLayout.setContentsMargins(0, 0, 0, 0)
        synopLayout.setSpacing(0)
        self.generate_synopsis_video(synopLayout)
        self.generate_synopsis_image(synopLayout)


        # image1 = ClickLabel()
        # pixmap = QPixmap('../test.jpg')
        # image1.setPixmap(pixmap)
        # image1.setFixedSize(100, 50)
        #
        # image1.clicked.connect(self.synopsis_click_handler)
        # synopImageLayout.addWidget(image1)


        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(videoHboxLayout)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
        vboxLayout.addLayout(synopLayout)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(self.videowidget)

        pal = self.palette()
        pal.setBrush(QPalette.Window, QBrush(QPixmap("../keyimages/1.png")));
        self.videowidget.setPalette(pal)

        #media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)

        self.imagewidget.hide()

    def generate_synopsis_video(self, synopLayout):

        frame_folder = os.path.join(parent_dir, 'keyframes')
        image_dir = os.listdir(frame_folder)
        image_dir.remove('.gitignore')
        image_dir.remove('.DS_Store')
        image_dir.sort(key=lambda img: (int(img.split('_')[0][-1])*10000+int(img.split('_')[1].split('.')[0])))
        images = [image for image in image_dir]
        count = 0

        synopImageLayout = QHBoxLayout()
        synopImageLayout.setContentsMargins(0, 0, 0, 0)
        synopImageLayout.setSpacing(0)

        for imageName in images:
            # frame_time = int(imageName.split('_')[1].split('.')[0])
            video_no = int(imageName.split('_')[0][-1])
            timestamp = (int(imageName.split('_')[1].split('.')[0]))
            image_label = ClickLabel()
            pixmap = QPixmap(os.path.join(parent_dir, 'keyframes', imageName))\
                .scaled(44, 36, Qt.KeepAspectRatio, Qt.FastTransformation)
            image_label.setPixmap(pixmap)
            image_label.clicked.connect(lambda t=timestamp, n=video_no: self.synopsis_click_handler(t, n))
            synopImageLayout.addWidget(image_label)
            count += 1
            if count == 17:
                synopLayout.addLayout(synopImageLayout)
                synopImageLayout = QHBoxLayout()
                synopImageLayout.setContentsMargins(0, 0, 0, 0)
                synopImageLayout.setSpacing(0)
                count = 0

    def generate_synopsis_image(self, synopLayout):
        image_folder = os.path.join(parent_dir, 'keyimages')
        image_dir = os.listdir(image_folder)
        image_dir.remove('.DS_Store')
        image_dir.sort(key=lambda img: int(img.split('.')[0]))
        images = [image for image in image_dir]
        count = 0
        rowcount = 0
        synopImageLayout = QHBoxLayout()
        synopImageLayout.setContentsMargins(0, 0, 0, 0)
        synopImageLayout.setSpacing(0)
        for imageName in images:
            image_no = int(imageName.split('.')[0])
            image_label = ClickLabel()
            pixmap = QPixmap(os.path.join(image_folder, imageName)) \
                .scaled(44, 36, Qt.KeepAspectRatio, Qt.FastTransformation)
            image_label.setPixmap(pixmap)
            image_label.clicked.connect(lambda filename=os.path.join(image_folder, imageName):
                                        self.image_synopsis_click_handler(filename))
            synopImageLayout.addWidget(image_label)
            count += 1
            if count == 17:
                synopLayout.addLayout(synopImageLayout)
                rowcount += 1
                if rowcount > 3:
                    return
                synopImageLayout = QHBoxLayout()
                synopImageLayout.setContentsMargins(0, 0, 0, 0)
                synopImageLayout.setSpacing(0)
                count = 0


    def open_video_file(self, filename):
        path = os.path.join(parent_dir, 'videos')
        mp4_path = os.path.join(path, 'mp4')
        avi_path = os.path.join(path, 'avi')
        mp4_name = filename + '.mp4'
        avi_name = filename + '.avi'
        mp4_dir = os.listdir(mp4_path)
        for mp4 in mp4_dir:
            if mp4_name == mp4:
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(mp4_path, mp4_name))))
                self.stopBtn.setEnabled(True)
                self.playBtn.setEnabled(True)
                self.filename = mp4_name
                return

        convert_avi_to_mp4(os.path.join(avi_path, avi_name), os.path.join(mp4_path, mp4_name))
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(mp4_path, mp4_name))))
        self.playBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        self.filename = mp4_name

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if os.path.splitext(filename)[1] == '.avi':
            output_name = os.path.dirname(filename) + '/output.mp4'
            convert_avi_to_mp4(filename, output_name)
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(output_name)))
            self.playBtn.setEnabled(True)

        elif filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            if self.audio_process:
                self.audio_process.kill()
                self.audio_process = False

        else:
            self.mediaPlayer.play()
            self.create_audio_process('../videos/{filename}/audio.wav'.format(filename=self.filename.split('.')[0]),
                                      self.position/1000)

    def reset_video(self):
        self.mediaPlayer.pause()
        self.mediaPlayer.setPosition(0)
        if self.audio_process:
            self.audio_process.kill()
            self.audio_process = False

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def create_audio_process(self, filename, start_time):
        if self.audio_process:
            self.audio_process.kill()
        cmd = "python3 audio.py {filename} {start}".format(filename=filename, start=start_time)
        self.audio_process = subprocess.Popen(cmd, shell=True)


    def position_changed(self, position):
        self.position = position


    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.play_video()
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def stop_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.play_video()

    def image_synopsis_click_handler(self, filename):
        self.imagewidget.show()
        self.videowidget.hide()
        self.stop_video()
        self.playBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        pixmap = QPixmap(filename)
        self.imagewidget.setPixmap(pixmap)

    def synopsis_click_handler(self, frame, video_no):
        self.imagewidget.hide()
        self.videowidget.show()
        self.playBtn.setEnabled(True)
        self.stopBtn.setEnabled(True)
        new_filename = 'video'+str(video_no)
        if self.filename.split('.')[0] != new_filename:
            self.open_video_file(new_filename)

        time = frame/30*1000
        self.mediaPlayer.setPosition(time)
        self.position = time
        self.stop_video()
        # wav_path = os.path.join(os.path.join(parent_dir, 'videos'), new_filename)
        # self.create_audio_process(os.path.join(wav_path, 'audio.wav'), self.position//1000)

def audio_play(audio_player, start_time):
    audio_player.play(start_time)


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

# audio_player = AudioPlayer(filename)
# self.p = multiprocessing.Process(target=audio_play, args=(audio_player, start_time))
# self.p.start()
# self.p.join()

window = Window()
sys.exit(app.exec_())