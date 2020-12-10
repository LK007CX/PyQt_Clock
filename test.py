from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import apprcc_rc

class Win(QWidget):

    def __init__(self):
        super(Win, self).__init__()
        self.pushButton = QPushButton(self, objectName='timeLabel')
        icon = QIcon()
        icon.addPixmap(QPixmap(":/image/image/clock.png"), QIcon.Normal, QIcon.On)
        self.pushButton.setIcon(icon)
        # self.pushButton.setObjectName("pushButton")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())