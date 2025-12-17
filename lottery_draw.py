# 抽奖

#!/usr/bin/env python3
from xlrd import open_workbook
import sys
import random
import os.path
#from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

Pro_SET = set()
City_SET = set()
Coun_SET = set()

def get_all_names():
    p_path = os.path.dirname(os.path.realpath(__file__))
    #p_path = os.path.dirname(os.path.realpath(sys.executable)) #打包时使用
    table = open_workbook(p_path + '/县市全集.xlsx').sheet_by_index(0)
    for cell in table.col_values(0):
        if not cell:
            break
        if cell.endswith('0000'):
            Pro_SET.add(cell.strip())
        elif cell.endswith('00'):
            City_SET.add(cell.strip())
        else:
            Coun_SET.add(cell.strip())
    
        
class LotteryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        get_all_names()

    def initUI(self):
        self.setWindowTitle('抽取')
        self.setGeometry(300,300,300,200)
        layout = QVBoxLayout()
        self.startbtn = QPushButton('开始', self)
        self.startbtn.clicked.connect(self.startLottery)
        self.exitbtn = QPushButton('退出', self)
        self.exitbtn.clicked.connect(QApplication.quit)
        layout.addWidget(self.startbtn)
        layout.addWidget(self.exitbtn)
        self.provincelabel = QLabel(self)
        self.countrylabel = QLabel(self)
        layout.addWidget(self.provincelabel)
        layout.addWidget(self.countrylabel)
        self.setLayout(layout)

    def startLottery(self):
        self.provincelabel.setText('')
        self.countrylabel.setText('')
        country = list(Coun_SET)
        result = random.choice(country)
        #查找相应省和市，存在直辖区的情况
        for pro in Pro_SET:
            if pro.split(' ')[1][0:2] == result.split(' ')[1][0:2]:
                city = pro.split(' ')[0]
        for cit in City_SET:
            if cit.split(' ')[1][0:4] == result.split(' ')[1][0:4]:
                city = city + ' ' + cit.split(' ')[0]
        self.countrylabel.setText(result)
        self.provincelabel.setText(city)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow = LotteryApp()
    myshow.show()
    sys.exit(app.exec_())