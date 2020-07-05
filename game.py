from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import functools
from random import *


class gameClass(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('game.ui',self)
        self.show()
        self.area = self.findChildren(QLabel)
        i = 0
        self.tickmap = QPixmap('tick.jpg')
        self.crossmap = QPixmap('cross.png')
        self.turn = randint(0,1)
        self.empty = []
        self.mark = []
        self.p1Name = self.findChild(QLineEdit,'line01')
        self.p2Name = self.findChild(QLineEdit,'line02')
        self.t1 = self.findChild(QRadioButton,'turn1')
        self.t2 = self.findChild(QRadioButton,'turn2')
        self.tScore = 0
        self.cScore = 0
        for x in self.area:
            x.mousePressEvent = functools.partial(self.showPic,x)
            x.setText(str(i))
            self.empty.append(True)
            self.mark.append('n')
            i = i + 1
        if self.turn==0:
            self.t1.setChecked(True)
            self.t2.setChecked(False)
        else:
            self.t1.setChecked(False)
            self.t2.setChecked(True)
        self.scoreReset = self.findChild(QPushButton,'rstScr')
        self.scoreReset.clicked.connect(self.clearScores)

    def reset(self):
        self.turn = randint(0,1)
        i = 0
        for x in self.area:
            x.clear()
            self.empty[i] = True
            self.mark[i] = 'n'
            i = i + 1
        if self.turn==0:
            self.t1.setChecked(True)
            self.t2.setChecked(False)
        else:
            self.t1.setChecked(False)
            self.t2.setChecked(True)

    def clearScores(self):
        resp = QMessageBox.information(self,'???','Do you really want to clear scores???',QMessageBox.Yes|QMessageBox.No)
        if resp==QMessageBox.Yes:
            self.cScore = 0
            self.tScore = 0
            self.t1.setText(str(self.cScore))
            self.t2.setText(str(self.tScore))
        else:
            pass

    def showPic(self, source=None, event=None):
        #QMessageBox.information(self,'info',source.objectName())
        n = source.objectName()
        if self.turn ==0 and self.empty[int(n[-2:])]:
            source.setPixmap(self.tickmap.scaled(source.width(),source.height(),Qt.KeepAspectRatio))
            self.turn=1
            self.empty[int(n[-2:])] = False
            self.mark[int(n[-2:])] = 't'
            self.t2.setChecked(True)
            self.t1.setChecked(False)
        elif self.turn==1 and self.empty[int(n[-2:])]:
            self.turn=0
            source.setPixmap(self.crossmap.scaled(source.width(),source.height(),Qt.KeepAspectRatio))
            self.empty[int(n[-2:])] = False
            self.mark[int(n[-2:])] = 'c'
            self.t1.setChecked(True)
            self.t2.setChecked(False)
        self.checkWin()


    def checkWin(self):
        list1 = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for y in list1:
            mc = 0
            mt = 0
            for x in y:
                if self.mark[x]=='c':
                    mc = mc + 1
                elif self.mark[x]=='t':
                    mt = mt + 1
            #print(y)
            #print(mc,mt)
            if mt==3:
                QMessageBox.information(self,'info',self.p1Name.text()+' Won',QMessageBox.Ok)
                #print(str(self.tScore),str(self.cScore))
                self.reset()
                self.tScore = 1 + self.tScore
                self.t1.setText(str(self.tScore))
                break
            elif mc==3:
                QMessageBox.information(self,'info',self.p2Name.text()+' Won',QMessageBox.Ok)
                self.reset()
                self.cScore = 1 + self.cScore
                self.t2.setText(str(self.cScore))
                #print(str(self.tScore),str(self.cScore))
                break
        i = False
        for x in self.empty:
            i = x or i
        if not i:
            QMessageBox.information(self,'info','That''s a tie!!!!', QMessageBox.Ok)
            self.reset()


app = QApplication(sys.argv)
window = gameClass()
sys.exit(app.exec())
