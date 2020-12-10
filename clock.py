from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from math import *
import sys
import datetime
import apprcc_rc
StyleSheet = '''
#timeLabel {
    color: white;
    font-size: 300px;

    font-family: MicroSoft Yahei;

}
QWidget {
    background-color: rgb(45, 45, 45);
}
#exitPushButton {
    min-height: 50px;
    min-width: 50px;
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
#dateTimeLabel {
    color: white;
    font-size: 25px;
    font-weight: normal;
    font-family: MicroSoft Yahei;
    font-style:italic;
}
'''


class ClockWidget(QWidget):
    def __init__(self, parent=None):
        super(ClockWidget, self).__init__(parent)
        self.setWindowTitle("PyQt时钟")

        self.timeLabel = QLabel(self, objectName='timeLabel')
        self.dateTimeLabel = QLabel(self, objectName='dateTimeLabel')
        self.lifeLabel = QLabel(self, objectName='lifeLabel')
        self.exitPushButton = QPushButton('', objectName='exitPushButton')
        self.tray_icon = QSystemTrayIcon(self)
        self.backend = BackendThread()

        self.init_ui()

    def init_ui(self):
        # layout
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.addWidget(self.lifeLabel, 0, Qt.AlignRight)
        layout.addStretch()
        layout.addWidget(self.timeLabel, 0, Qt.AlignCenter)
        layout.addWidget(self.dateTimeLabel, 0, Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.exitPushButton, 0, Qt.AlignRight)
        self.setLayout(layout)

        self.lifeLabel.setText("                永远相信\n美好的事情即将发生")
        self.lifeLabel.setAlignment(Qt.AlignRight)

        # 托盘
        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)
        hide_action = QAction("隐藏", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # icon
        windowIcon = QIcon()
        windowIcon.addPixmap(QPixmap(":/image/image/clock.png"))
        self.setWindowIcon(windowIcon)
        exitIcon = QIcon()
        exitIcon.addPixmap(QPixmap(":/image/image/cc-exit.png"))
        self.exitPushButton.setIcon(exitIcon)
        trayIcon = QIcon()
        trayIcon.addPixmap(QPixmap(":/image/image/clock.png"))
        self.tray_icon.setIcon(trayIcon)
        showIcon = QIcon()
        showIcon.addPixmap(QPixmap(":/image/image/show.png"))
        show_action.setIcon(showIcon)
        quitIcon = QIcon()
        quitIcon.addPixmap(QPixmap(":/image/image/exit_tray.png"))
        quit_action.setIcon(quitIcon)
        hideIcon = QIcon()
        hideIcon.addPixmap(QPixmap(":/image/image/hide.png"))
        hide_action.setIcon(hideIcon)

        # 事件绑定
        self.exitPushButton.clicked.connect(self.exit_app)
        self.exitPushButton.setIconSize(QSize(25, 25))
        self.backend.update_date.connect(self.handle_display)
        self.backend.start()

    def handle_display(self, time, dateTime):
        self.timeLabel.setText(time)
        self.dateTimeLabel.setText(dateTime)

    def exit_app(self):
        self.hide()
        self.tray_icon.showMessage(
            "桌面小时钟",
            "程序被最小化到托盘",
            QSystemTrayIcon.Information,
            2000
        )


class BackendThread(QThread):

    update_date = pyqtSignal(str, str)

    def run(self):
        while True:
            data = datetime.datetime.now()
            current_time = data.strftime("%H:%M:%S")
            current_dateTime = data.strftime("%A    %Y-%m-%d")
            self.update_date.emit(str(current_time), str(current_dateTime))
            self.sleep(1)


def showAllScreen():
    primary_screen = QApplication.primaryScreen()
    screens = QApplication.screens()
    for screen in screens:
        if screen is not primary_screen:
            auxiliary_screen = screen
            break
        else:
            auxiliary_screen = None
    return primary_screen, auxiliary_screen


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = ClockWidget()
    clock.setStyleSheet(StyleSheet)
    # primary_screen, auxiliary_screen = showAllScreen()
    # clock.setGeometry(primary_screen.geometry())
    # clock.setGeometry(auxiliary_screen.geometry())
    # clock.showFullScreen()
    clock.show()
    app.exec_()