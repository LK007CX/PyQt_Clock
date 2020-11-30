from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
import sys


StyleSheet = '''
#timeLabel {
    color: white;
    font-size: 500px;
    font-family: MicroSoft Yahei;
}

QWidget {
    background-color: red;
}

#exitPushButton {
    max-height: 48px;
    border-top-right-radius: 0px; /*右上角圆角*/
    border-bottom-left-radius: 0px; /*左下角圆角*/
}
#exitPushButton:hover {
    background-color: #ffb74d;
}
#exitPushButton:pressed {
    background-color: #ffe0b2;
}

#lifeLabel {
    color: white;
    font-size: 20px;
    font-family: MicroSoft Yahei;
}
'''


class ClockWidget(QWidget):
    def __init__(self, parent=None):
        super(ClockWidget, self).__init__(parent)
        self.setWindowTitle("PyQt时钟")
        # self.resize(400, 400)
        self.timeLabel = QLabel(self, objectName='timeLabel')
        self.lifeLabel = QLabel(self, objectName='lifeLabel')
        self.backend = BackendThread()
        self.exitPushButton = QPushButton(QIcon('./image/exit.png'), '', objectName='exitPushButton')

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)

        layout.addWidget(self.lifeLabel, 0, Qt.AlignRight)
        layout.addStretch()
        layout.addWidget(self.timeLabel, 0, Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.exitPushButton, 0, Qt.AlignRight)

        self.setLayout(layout)

        self.lifeLabel.setText("                永远相信\n美好的事情即将发生")
        # self.lifeLabel.setWordWrap(True)
        self.lifeLabel.setAlignment(Qt.AlignRight)


        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.exitPushButton.clicked.connect(self.exit_app)
        self.backend.update_date.connect(self.handle_display)
        self.backend.start()

    def handle_display(self, time):
        self.timeLabel.setText(time)

    def exit_app(self):
        self.hide()
        self.tray_icon.showMessage(
            "Tray Program",
            "Application was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )



class BackendThread(QThread):

    update_date = pyqtSignal(str)

    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            current_time = data.toString("hh:mm")
            self.update_date.emit(str(current_time))
            self.sleep(60)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.setStyleSheet(StyleSheet)
    clock.showFullScreen()
    app.exec_()