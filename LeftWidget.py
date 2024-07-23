
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QApplication, QTextEdit, QRadioButton, QMessageBox
from PySide6.QtCore import Signal, Qt
from dataModel import DataModel

class LeftWidget(QWidget):
    sig_warn = Signal()

    def __init__(self, dataModel: DataModel):
        super().__init__()
        self.dataModel = dataModel
        self.setupUi()
        self.bind()
    
    def setupUi(self):
        self.normalStatic = QRadioButton(self)
        self.normalStatic.setText('普通模式')
        self.normalStatic.setChecked(True)
        self.worldStatic = QRadioButton(self)
        self.worldStatic.setText('World截图模式')

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.normalStatic)
        topLayout.addWidget(self.worldStatic)

        self.blackDownPriceLabel = QLabel('黑墨基础价', self)
        self.blackDownPriceEdit = QLineEdit(self.dataModel.data['black_down_price'], self)
        self.blackUpPriceLabel = QLabel('黑墨递增价', self)
        self.blackUpPriceEdit = QLineEdit(self.dataModel.data['black_up_price'], self)
        
        self.colorDownPriceLabel = QLabel('彩墨基础价', self)
        self.colorDownPriceEdit = QLineEdit(self.dataModel.data['color_down_price'], self)
        self.colorUpPriceLabel = QLabel('彩墨递增价', self)
        self.colorUpPriceEdit = QLineEdit(self.dataModel.data['color_up_price'], self)

        self.msgLabel = QLabel('计算结果将在这里显示', self)
        self.msgLabel.setFixedHeight(200)

        self.msgLabel.setStyleSheet('QLabel{border: 1px}')

        oneHLayout = QHBoxLayout()
        oneHLayout.addWidget(self.blackDownPriceLabel)
        oneHLayout.addWidget(self.blackDownPriceEdit)
        oneHLayout.addWidget(self.blackUpPriceLabel)
        oneHLayout.addWidget(self.blackUpPriceEdit)

        twoHLayout = QHBoxLayout()
        twoHLayout.addWidget(self.colorDownPriceLabel)
        twoHLayout.addWidget(self.colorDownPriceEdit)
        twoHLayout.addWidget(self.colorUpPriceLabel)
        twoHLayout.addWidget(self.colorUpPriceEdit)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(topLayout)
        self.mainLayout.addLayout(oneHLayout)
        self.mainLayout.addLayout(twoHLayout)
        self.mainLayout.addWidget(self.msgLabel)

        self.setLayout(self.mainLayout)
    
    def bind(self):
        self.worldStatic.clicked.connect(lambda: self.sig_warn.emit())

        self.blackDownPriceEdit.textChanged.connect(self.update_data)
        self.blackUpPriceEdit.textChanged.connect(self.update_data)
        self.colorDownPriceEdit.textChanged.connect(self.update_data)
        self.colorUpPriceEdit.textChanged.connect(self.update_data)

    
    def copyPath(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.msgLabel.text())

        msg = QMessageBox()
        msg.setText('图片路径已复制。')
    
    def update_data(self):
        self.dataModel.data['black_down_price'] = self.blackDownPriceEdit.text()
        self.dataModel.data['black_up_price'] = self.blackUpPriceEdit.text()
        self.dataModel.data['color_down_price'] = self.colorDownPriceEdit.text()
        self.dataModel.data['color_up_price'] = self.colorUpPriceEdit.text()

        self.dataModel.updateData()



if __name__ == '__main__':
    app = QApplication()
    window = LeftWidget()
    window.show()
    app.exec()