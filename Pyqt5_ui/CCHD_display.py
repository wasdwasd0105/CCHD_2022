from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QVBoxLayout,QPushButton,QLineEdit,QHBoxLayout,QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPalette
import sys
import pandas
import os

curdir = os.path.dirname(os.path.realpath(__file__))
cchd_resultfile = os.path.join(curdir, '..', 'Data', 'CCHD_result.csv')

cchd_result = pandas.read_csv(cchd_resultfile)
class Qlabel_demo(QWidget):
    def __init__(self,parent=None):
        super(Qlabel_demo,self).__init__(parent)

        nameL=QLabel("Case name",self)
        nameE=QLineEdit(self)
        nameE.setText(cchd_result[-1:]['case_name'].tolist()[0])
        nameE.setAlignment(Qt.AlignCenter)
        nameE.setReadOnly(True)

        resultL=QLabel("Result",self)
        resultE=QLineEdit(self)
        resultE.setText(cchd_result[-1:]['result'].tolist()[0])
        if cchd_result[-1:]['result'].tolist()[0] == 'CCHD':
            resultE.setStyleSheet('QLineEdit {background: rgb(255, 0, 0);}')
        else:
            resultE.setStyleSheet('QLineEdit {background: rgb(0, 255, 0);}')
        resultE.setAlignment(Qt.AlignCenter)
        resultE.setReadOnly(True)

        FootratioL=QLabel("Foot AWAD ratio",self)
        FootratioE=QLineEdit(self)
        FootratioE.setText("{:.3f}".format(100 * cchd_result[-1:]['foot_awad_ratio'].tolist()[0]))
        FootratioE.setAlignment(Qt.AlignCenter)
        FootratioE.setReadOnly(True)

        HandratioL=QLabel("Hand AWAD ratio",self)
        HandratioE=QLineEdit(self)
        HandratioE.setText("{:.3f}".format(100 * cchd_result[-1:]['hand_awad_ratio'].tolist()[0]))
        HandratioE.setAlignment(Qt.AlignCenter)
        HandratioE.setReadOnly(True)


        btn=QPushButton("OK")
        btn.clicked.connect(self.btnState)

        mainLayout=QGridLayout(self)
        mainLayout.addWidget(nameL,0,0)
        mainLayout.addWidget(nameE,0,1,1,2)
        mainLayout.addWidget(resultL,1,0)
        mainLayout.addWidget(resultE,1,1,1,2)
        mainLayout.addWidget(FootratioL,2,0)
        mainLayout.addWidget(FootratioE,2,1,1,2)
        mainLayout.addWidget(HandratioL,3,0)
        mainLayout.addWidget(HandratioE,3,1,1,2)
        mainLayout.addWidget(btn,4,0,2,4)

    def btnState(self):
        exit()


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=Qlabel_demo()
    win.setWindowTitle('CCHD results')
    win.show()
    sys.exit(app.exec_())
