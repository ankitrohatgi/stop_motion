from PySide6.QtWidgets import QApplication
import sys
from stop_motion.main_window import MainWindow

def launch():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(window.clean_up)
    app.exec()

