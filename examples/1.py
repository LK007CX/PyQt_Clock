
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *


class DigitalClock(QLCDNumber):


    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)
        self.__InitData() #初始化类的数据
        self.__InitView() #初始化界面
        
    def __InitData(self):
        #初始化数据
        self.__ShowColon = True #是否显示时间如[12:07]中的冒号，用于冒号的闪烁
        self.__dragPosition = QPoint(0,0) #用于保存鼠标相对于电子时钟左上角的偏移值
        
        self.__timer = QTimer(self) #新建一个定时器
        #关联timeout信号和showTime函数，每当定时器过了指定时间间隔，就会调用showTime函数
        self.__timer.timeout.connect(self.showTime)
        
        self.__timer.start(1000) #设置定时间隔为1000ms即1s，并启动定时器
        
    
    def __InitView(self):
        #初始化界面
        palette = QPalette() #新建调色板
        palette.setColor(QPalette.Window, Qt.blue) #将调色板中的窗体背景色设置为蓝色
        self.setPalette(palette) #在本窗体载入此调色板
        self.setWindowFlags(Qt.FramelessWindowHint) #设置窗体为无边框模式
        self.setWindowOpacity(0.5)  #设置窗体的透明度为0.5
        self.resize(200,60) #设置界面尺寸，宽150px,高60px
        self.setNumDigits(8) #允许显示8个字符  原因，自己数右边几个字符 【HH:MM:SS】
        self.showTime() #初始化时间的显示
        
    
    def showTime(self):
        #更新时间的显示
        time = QTime.currentTime() #获取当前时间
        time_text = time.toString(Qt.DefaultLocaleLongDate) #获取HH:MM:SS格式的时间，在中国获取后是这个格式，其他国家我不知道，如果有土豪愿意送我去外国旅行的话我就可以试一试
        
        #冒号闪烁
        if self.__ShowColon == True:
            self.__ShowColon = False
        else:
            time_text = time_text.replace(':',' ')
            self.__ShowColon = True
        
        self.display(time_text) #显示时间
        
    def mousePressEvent(self, mouseEvent):
        #鼠标按下事件
        btn_code = mouseEvent.button()

        if btn_code == Qt.LeftButton:
            #如果是鼠标左键按下
            self.__dragPosition = mouseEvent.globalPos() - self.frameGeometry().topLeft()
            print(self.__dragPosition)
            mouseEvent.accept()
        elif btn_code == Qt.RightButton:
            print("It will close")
            self.close() #鼠标右键关闭时钟
    
    def mouseMoveEvent(self, mouseEvent):
        #鼠标移动事件
        #在鼠标拖动下，使用move函数移动电子时钟
        #move的参数是QPoint类型，可理解为形如(x,y)的矢量
        self.move(mouseEvent.globalPos()-self.__dragPosition)
        mouseEvent.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = DigitalClock(None) #新建电子时钟
    clock.show() #显示电子时钟
    sys.exit(app.exec_()) #进入消息循环
