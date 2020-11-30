import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyTimer(QWidget):
    def __init__(self, parent=None):
        super(MyTimer, self).__init__(parent)
        self.resize(200, 100)
        self.setWindowTitle("QTimerDemo")

        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(10)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X", time.localtime()))

        layout = QVBoxLayout()
        layout.addWidget(self.lcd)
        self.setLayout(layout)

        # 新建一个QTimer对象
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()

        # 信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)

    # 定义槽
    def onTimerOut(self):
        self.lcd.display(time.strftime("%X", time.localtime()))


app = QApplication(sys.argv)
t = MyTimer()
t.show()
sys.exit(app.exec_())