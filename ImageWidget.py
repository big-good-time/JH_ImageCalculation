from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QMainWindow, QMenu
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ImageWidget(QWidget):
    def __init__(self, path: str | None = None):
        super().__init__()

        self.imageLabel = QLabel(self)
        # self.imageLabel.setFixedSize(800, 600)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setStyleSheet('''
            QLabel {
                border: 1px solid #808080;
            }
        ''')

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)
        self.setImage(path)

    
    def setImage(self, path: str | None = None):
        if not path: return
        self.img = QPixmap(path)
        scaled_pixmap = self.img.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.imageLabel.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QApplication()
    window = ImageWidget()
    window.show()
    app.exec()