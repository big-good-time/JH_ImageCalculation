from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QMenu, QWidget, QLabel, QMessageBox, QStatusBar, QToolBar
from PySide6.QtCore import QThread, Slot, Signal
from PySide6.QtGui import QAction
from LeftWidget import LeftWidget
from FileTree import FileTree
from ImageWidget import ImageWidget
import mimetypes
from ImageRead import ImageRead
from dataModel import DataModel
import os
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.dataModel = DataModel()
        self.app = app
        self.resize(800, 600)
        self.setupUi()
        self.bind()
        self.setMenu()
        self.loadStyleSheet(self.dataModel.data['style_sheet'])

    def setupUi(self):
        
        self.leftWidget = LeftWidget(self.dataModel)
        self.fileTree = FileTree()

        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.leftWidget)
        self.leftLayout.addWidget(self.fileTree)

        self.imageWidget = ImageWidget(path=None)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.imageWidget)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.parmanent_label = QLabel('Ready')
        self.status_bar.addPermanentWidget(self.parmanent_label)

    
    def bind(self):
        self.fileTree.sig_selectedPath.connect(self.setImage)
        self.leftWidget.sig_warn.connect(partial(self.showMsg, '提醒', '此模式只针对 world 截图！谨慎使用！'))
        self.fileTree.sig_copyPath.connect(partial(self.showMsg, '提醒', '路径已拷贝。'))
    
    def setMenu(self):
        self.menu = self.menuBar()
        self.styleMenu = QMenu('主题', self)

        self.menu.addMenu(self.styleMenu)

        file_list = []
        for root, dirs, files in os.walk('./Style'):
            for file in files:
                if file.endswith('.qss'):
                    file_list.append(os.path.join(root, file))
        
        for file in file_list:
            action = QAction(file, self)
            action.triggered.connect(partial(self.loadStyleSheet, file))
            self.styleMenu.addAction(action)
    
    def loadStyleSheet(self, file):
        with open(file, 'r') as f:
            styleSheet = f.read()
        self.app.setStyleSheet(styleSheet)
        self.dataModel.data['style_sheet'] = file
        self.dataModel.updateData()

    
    def showMsg(self, title: str, msg: str):
        QMessageBox.information(self, title, msg)
    
    def setImage(self, path: str):
        if not self.is_image_file(path): return

        self.status_bar.showMessage(f'正在处理：{path}')

        self.imageWidget.setImage(path)

        self.worker = ImageWorker(self.dataModel, path, self.leftWidget.worldStatic.isChecked())
        self.worker.finished.connect(self.update_msg_label)
        self.worker.error.connect(lambda: self.status_bar.showMessage('处理失败！'))
        self.worker.start()
    
    @Slot(str)
    def update_msg_label(self, msg: str):
        self.leftWidget.msgLabel.setText(msg)
        self.status_bar.showMessage('处理完成！')
    
    def is_image_file(self, path: str) -> bool:
        mime_type, _ = mimetypes.guess_type(path)
        return mime_type and mime_type.startswith('image')
    
    def resizeEvent(self, event):
        self.imageWidget.setFixedWidth(self.width() // 2)
        super().resizeEvent(event)

class ImageWorker(QThread):
    finished = Signal(str)
    error = Signal()

    def __init__(self, data: DataModel, path: str, is_world: bool = False):
        super().__init__()
        self.path = path
        self.dataModel = data
        self.is_world = is_world

    def run(self):
        
        try:
            ir = ImageRead(self.path, self.dataModel.data['black_down_price'], self.dataModel.data['color_down_price'],
                        self.dataModel.data['black_up_price'], self.dataModel.data['color_up_price'], 
                        self.is_world)
            size = f'图片尺寸：{ir.height}, {ir.width}<br>'
            all_per = f'总覆盖率：{ir.all_per}%<br>'
            black_per = f'黑覆盖率：{ir.black_per}%<br>'
            color_per = f'彩覆盖率：{ir.color_per}%<br>'
            black_price = f'黑色费用：{ir.black_price} 元<br>'
            color_price = f'彩色费用：{ir.color_price} 元<br>'
            all_price = f'总费用：{ir.all_price} 元'

            self.finished.emit(size + all_per + black_per + color_per + black_price + color_price + all_price)
        except Exception as e:
            print(e)
            self.error.emit()