import sys, random
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QAction, QMenu
from PyQt5.QtCore import Qt, pyqtSignal


class MyWin(QMainWindow):
    def __init__(self):
        super(MyWin, self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("ScreenShot Tool")
        self.resize(200, 100)
        self.btn = QPushButton('Take a pic', self)
        self.btn.setGeometry(20, 20, 60, 60)
        self.btn.clicked.connect(self.click_btn)

    def click_btn(self):
        self.showMinimized()
        self.screenshot = ScreenShotsWin()
        self.screenshot.showFullScreen()


class ScreenShotsWin(QMainWindow):
    oksignal = pyqtSignal()

    def __init__(self):
        super(ScreenShotsWin, self).__init__()
        self.initUI()
        self.start = (0, 0)  
        self.end = (0, 0)  

    def initUI(self):
        self.setWindowOpacity(0.4)
        self.btn_ok = QPushButton('ok', self)
        self.oksignal.connect(lambda: self.screenshots(self.start, self.end))

    def screenshots(self, start, end):
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])

        des = QApplication.desktop()
        screen = QApplication.primaryScreen()
        if screen:
            self.setWindowOpacity(0.0)
            pix = screen.grabWindow(des.winId(), x, y, width, height)
        default_name = random.randint(1000000, 3000000)
        fileName = QFileDialog.getSaveFileName(self, 'Save to destination', str(default_name), ".jpg")
        if fileName[0]:
            pix.save(fileName[0] + fileName[1])

        self.close()

    def paintEvent(self, event):
        x = self.start[0]
        y = self.start[1]
        w = self.end[0] - x
        h = self.end[1] - y

        pp = QPainter(self)
        pp.drawRect(x, y, w, h)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.start = (event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())

            self.oksignal.emit()
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton:
            self.end = (event.pos().x(), event.pos().y())
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dbb = MyWin()
    dbb.show()
    sys.exit(app.exec_())
