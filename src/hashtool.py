# -*- coding: utf-8 -*-
import sys
import hashlib
from PySide.QtGui import *
from PySide.QtCore import *

def calculateFileHash(fname, mthod='md5'):
    m = hashlib.md5()
    fobj = open(fname, 'r')
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    fobj.close()
    return m.hexdigest()


class DlgHashTool(QDialog):

    def __init__(self):
        super(DlgHashTool, self).__init__()
        self.initUI()

    def initUI(self):
        stdButtons = QDialogButtonBox(QDialogButtonBox.Close, Qt.Horizontal, self)
        grid = QGridLayout()

        grid.addWidget(QLabel(u"Datei", self),0,0)

        row1 = QHBoxLayout()
        self.leInputFile = QLineEdit(self)
        self.leInputFile.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred))
        row1.addWidget(self.leInputFile)
        self.btnInputFile = QPushButton("...", self)
        #self.btnInputFile.setMaximumSize(QSize(40,28))
        self.btnInputFile.clicked.connect(self.selectFile)
        row1.addWidget(self.btnInputFile)

        grid.addLayout(row1,0,1)

        grid.addWidget(QLabel(u"Berechnen", self),1,0)
        row2 = QHBoxLayout()
        self.cmbMethod = QComboBox(self)
        self.cmbMethod.addItems(["md5", "sha1", "sha256", "sha512"])
        self.cmbMethod.setMaximumSize(QSize(60,28))
        row2.addWidget(self.cmbMethod)
        self.labelResult = QLabel("-", self)
        self.labelResult.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        row2.addWidget(self.labelResult)
        grid.addLayout(row2,1,1)

        grid.addWidget(QLabel(u"Prüfsumme", self),2,0)
        row3 = QHBoxLayout()
        self.leProvidedHashSum = QLineEdit(self)
        row3.addWidget(self.leProvidedHashSum)
        grid.addLayout(row3,2,1)

        grid.addWidget(stdButtons,4,0,1,2)
        grid.addItem(QSpacerItem(10,10, QSizePolicy.Expanding, QSizePolicy.Expanding), 3,0)
        self.setLayout(grid)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tool')
        self.show()

    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file','~')
        if fname is not None:
            self.leInputFile.setText(fname)
            self.labelResult.setText(calculateFileHash(fname))



def main():
    app = QApplication(sys.argv)
    ex = DlgHashTool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
