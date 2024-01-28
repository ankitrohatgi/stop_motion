from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QThread, QTimer, QMutex, Signal
from PySide6.QtGui import QPixmap, QImage
import cv2 as cv

class StreamingVideoThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent, capture_mutex):
        super().__init__(parent)
        self.parent = parent
        self.cap_mutex = capture_mutex
        self.keep_running = True

    def stop_stream(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.cap_mutex.lock()
            if self.parent.video_capture == None:
                self.keep_running = False
                break
            ret, bgr_frame = self.parent.video_capture.read()
            self.cap_mutex.unlock()
            if not ret:
                break
            frame = cv.cvtColor(bgr_frame, cv.COLOR_RGB2BGR)
            qimage = get_qimage_from_cv(frame)
            self.updateFrame.emit(qimage)


class VideoPlayer(QLabel):
    def __init__(self):
        super().__init__()
    
    def stream_camera(self, camera_config):
        pass

    def capture(self):
        pass

    def get_capture_count(self):
        pass

