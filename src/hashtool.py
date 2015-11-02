# -*- coding: utf-8 -*-
import sys
from hashlib import new as hashlib_new
from hashlib import algorithms as hashlib_algorithms
from PySide.QtGui import *
from PySide.QtCore import *

def calculateFileHash(fname, algorithm='md5'):
    m = hashlib_new(algorithm)
    fobj = open(fname, 'rb')
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

        self.setWindowTitle('Hashsum calculation')
        self.setMinimumWidth(420)

        grid = QGridLayout()
        grid.setColumnStretch(0,0)
        grid.setColumnStretch(1,1)
        self.setLayout(grid)

        grid.addWidget(QLabel(u"File", self),0,0)
        row1 = QHBoxLayout()
        row1.setStretch(0,1)
        row1.setStretch(1,0)
        self.leInputFile = QLineEdit(self)
        row1.addWidget(self.leInputFile)
        self.btnInputFile = QPushButton("...", self)
        self.btnInputFile.setMaximumSize(QSize(20,28))
        row1.addWidget(self.btnInputFile)
        grid.addLayout(row1,0,1)

        grid.addWidget(QLabel(u"Checksum", self),1,0)
        row2 = QHBoxLayout()
        self.cmbMethod = QComboBox(self)
        self.cmbMethod.addItems([str(a).upper() for a in hashlib_algorithms])
        self.cmbMethod.setMaximumSize(QSize(72,28))
        self.cmbMethod.setCurrentIndex(hashlib_algorithms.index("sha1"))
        row2.addWidget(self.cmbMethod)
        self.labelResult = QLabel("", self)
        self.labelResult.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.labelResult.setTextInteractionFlags(Qt.TextSelectableByMouse|Qt.TextSelectableByKeyboard)
        row2.addWidget(self.labelResult)
        grid.addLayout(row2,1,1)

        grid.addWidget(QLabel(u"Compare", self),2,0)
        row3 = QHBoxLayout()
        self.leProvidedHashSum = QLineEdit(self)
        self.leProvidedHashSum.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        clip = QApplication.clipboard().text()
        if clip != "":
            self.leProvidedHashSum.setText(clip)
        row3.addWidget(self.leProvidedHashSum)
        grid.addLayout(row3,2,1)

        grid.addWidget(QLabel(u"Result", self),3,0)
        self.labelCompareResult = QLabel("", self)
        self.labelCompareResult.setAutoFillBackground(True)
        self.labelCompareResult.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.labelCompareResult,3,1)

        self.stdButtons = QDialogButtonBox(QDialogButtonBox.Close, Qt.Horizontal, self)
        grid.addWidget(self.stdButtons,5,0,1,2)
        grid.addItem(QSpacerItem(10,10, QSizePolicy.Expanding, QSizePolicy.Expanding), 4,0)

        self.stdButtons.clicked.connect(self.close)
        self.btnInputFile.clicked.connect(self.selectFile)
        self.leProvidedHashSum.textChanged.connect(self.compareResult)
        self.leInputFile.textChanged.connect(self.recalculate)
        self.cmbMethod.currentIndexChanged.connect(self.recalculate)

        self.show()


    def setResultColor(self, color):
        palette = self.labelCompareResult.palette()
        palette.setColor(self.labelCompareResult.backgroundRole(), color)
        self.labelCompareResult.setPalette(palette)


    def compareResult(self):
        if self.labelResult.text() == "" or self.leProvidedHashSum.text() == "":
            self.labelCompareResult.setText("")
            self.setResultColor(self.palette().window().color())
        elif self.labelResult.text() == self.leProvidedHashSum.text():
            self.labelCompareResult.setText("OK")
            self.setResultColor(Qt.green)
        else:
            self.labelCompareResult.setText("!NO MATCH!")
            self.setResultColor(Qt.red)


    def recalculate(self):
        fname = self.leInputFile.text()
        if fname is not None and fname != '':
            fi = QFileInfo(fname)
            if fi.exists() and fi.isFile():
                self.labelResult.setText(calculateFileHash(fname, self.cmbMethod.currentText()))
                self.compareResult()


    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file','~')
        if fname is not None and fname != '':
            self.leInputFile.setText(fname)



def main():
    app = QApplication(sys.argv)
    ex = DlgHashTool()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
