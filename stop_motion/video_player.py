from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QThread, QTimer, QMutex, Signal, Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QResizeEvent
import cv2 as cv
import time
import os


def get_qimage_from_cv(img):
    height, width, channel = img.shape
    bytesPerLine= 3 * width
    qimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return qimg

class StreamingVideoThread(QThread):
    updateFrame = Signal(QImage, cv.Mat)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.keep_running = True

    def stop_stream(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.parent.capture_mutex.lock()
            if self.parent.video_capture == None:
                self.keep_running = False
                break
            ret, bgr_frame = self.parent.video_capture.read()
            self.parent.capture_mutex.unlock()
            if not ret:
                break
            frame = cv.cvtColor(bgr_frame, cv.COLOR_BGR2RGB)
            qimage = get_qimage_from_cv(frame)
            self.updateFrame.emit(qimage, bgr_frame)


class VideoPlayer(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(0, 0, 0)")
        self.is_streaming = False
        self.video_capture = None
        self.capture_mutex = QMutex()
        self.streaming_thread = None
        self.num_captured_frames = 0
        self.latest_qimage = None
        self.original_pixmap = None
        self.scaled_size = None

    def _update_image(self, qimage, cvimage):
        self.latest_qimage = qimage
        self.latest_cvimage = cvimage
        self.setPixmap(QPixmap(qimage))

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.setPixmap(self.original_pixmap)
    
    def sizeHint(self) -> QSize:
        if self.scaled_size != None:
            return self.scaled_size
        return super().sizeHint()

    def setPixmap(self, pixmap: QPixmap) -> None:
        if pixmap is None:
            return
        self.original_pixmap = pixmap
        scaled_pixmap = self.original_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.scaled_size = scaled_pixmap.size()
        return super().setPixmap(scaled_pixmap)

    def stream_camera(self, config):
        self.stop_streaming()
        self.config = config
        camera_config = config["camera"]
        self.video_capture = cv.VideoCapture(camera_config["device"])
        if self.video_capture.isOpened():
            if "width" in camera_config:
                self.video_capture.set(cv.CAP_PROP_FRAME_WIDTH, camera_config["width"])
            if "height" in camera_config:
                self.video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, camera_config["height"])
            self.streaming_thread = StreamingVideoThread(self)
            self.streaming_thread.updateFrame.connect(self._update_image)
            self.streaming_thread.start()
            self.is_streaming = True

    def stop_streaming(self):
        self.is_streaming = False
        self.num_captured_frames = 0
        if self.streaming_thread is not None:
            self.streaming_thread.stop_stream()
            self.capture_mutex.lock()
            if self.video_capture is not None:
                self.video_capture.release()
            self.capture_mutex.unlock()

    def capture(self):
        if not self.is_streaming:
            return
        out_dir = self.config["recording"]["path"]
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        epoch_ms = int(time.time()*1000.0)
        img_name =  "frame_{}.png".format(epoch_ms)
        img_path = os.path.join(out_dir, img_name)
        cv.imwrite(img_path, self.latest_cvimage)
        self.num_captured_frames += 1

    def get_capture_count(self):
        return self.num_captured_frames

