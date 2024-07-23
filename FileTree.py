from PySide6.QtWidgets import QApplication, QScrollArea, QTreeView, QLabel, QVBoxLayout, QWidget, QFileSystemModel
from PySide6.QtCore import QItemSelection, Signal, Qt
from PySide6.QtGui import QMouseEvent

class FileTree(QWidget):
    sig_selectedPath = Signal(str)
    sig_copyPath = Signal()

    def __init__(self):
        super().__init__()

        # 创建文件系统模型
        self.model = QFileSystemModel()
        self.model.setRootPath('') # 设置根路径为空，表示整个文件系统

        # 创建树视图
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index('')) # 设置根索引为空，表示整个文件系统
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setColumnWidth(0, 250) # 设置第一列的宽度

        # 创建标签显示选中的文件路径
        self.labelScrollArea = QScrollArea()
        self.labelScrollArea.setFixedHeight(30)
        
        self.label = ClickableLabel("选中的文件路径将在这里显示（点我拷贝）")
        self.labelScrollArea.setWidget(self.label)
        self.labelScrollArea.setWidgetResizable(True)

        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.labelScrollArea)
        self.setLayout(layout)

        self.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self.bind()
    
    def bind(self):
        self.label.clicked.connect(self.copyPath)

    def copyPath(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.label.text())
        self.sig_copyPath.emit()

    def on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        # 获取选中的索引
        index = self.tree.currentIndex()
        if not index.isValid():
            self.label.setText('没有选中文件')
            return

        # 获取文件路径
        file_path = self.model.filePath(index)
        self.label.setText(f'{file_path}')
        self.sig_selectedPath.emit(file_path)
    
class ClickableLabel(QLabel):
    clicked = Signal()

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.buttons() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(ev)


if __name__ == '__main__':
    app = QApplication()
    window = FileTree()
    window.show()
    app.exec()