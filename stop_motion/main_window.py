from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QAction
from stop_motion.video_player import VideoPlayer
import yaml


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Stop Motion")
        self._init_menubar()
        self._init_widgets()
        self.statusBar().showMessage("Start taking pictures!")

    def _init_widgets(self):
        self.video_player = VideoPlayer()
        self.capture_button = QPushButton("Snap!")
        self.capture_button.setShortcut("Space")
        self.capture_button.clicked.connect(self.capture)
        vbox = QVBoxLayout()
        vbox.addWidget(self.video_player)
        vbox.addWidget(self.capture_button)
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

    def _init_menubar(self):
        menubar = self.menuBar()

        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(exit_action)

    def load_config(self, file):
        config_data = None
        with open(file, "r") as f:
            config_data = yaml.load(f, Loader=yaml.SafeLoader)
        self.video_player.stream_camera(config_data)

    def capture(self):
        self.video_player.capture()
        num_snaps = self.video_player.get_capture_count()
        self.statusBar().showMessage(f"Number of pictures: {num_snaps}")

    def clean_up(self):
        print("shutting down, bye!")
        self.video_player.stop_streaming()
