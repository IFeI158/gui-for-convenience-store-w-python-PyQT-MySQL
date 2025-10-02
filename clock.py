import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QFont

class ClockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("시계")

        # 레이아웃
        layout = QVBoxLayout(self)

        # 시계 라벨
        self.clock_label = QLabel()
        self.clock_label.setFont(QFont("Arial", 30, QFont.Bold))  # 글씨 크기 및 굵기 설정
        layout.addWidget(self.clock_label)

        # 타이머 설정 (1초마다 시간 갱신)
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)

        # 시작 시 바로 한 번 표시
        self.update_clock()

    def update_clock(self):
        now = QTime.currentTime().toString("HH:mm:ss")
        self.clock_label.setText(now)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClockWindow()
    window.show()
    sys.exit(app.exec_())
