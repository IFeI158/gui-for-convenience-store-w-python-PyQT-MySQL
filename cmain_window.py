from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout,
)
from PyQt5.QtGui import QFont, QIcon
from cdb_helper import DB, DB_CONFIG
import sys
from clock import ClockWindow  # 시계 창 import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("편의점 관리")
        self.setWindowIcon(QIcon("CU.png"))
        self.resize(400, 300)
        self.db = DB(**DB_CONFIG)

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        # 입력폼 + 버튼
        form_box = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_amount = QLineEdit()
        self.btn_add = QPushButton("발주")
        self.btn_add.clicked.connect(self.add_amount)
        self.btn_del = QPushButton("판매")
        self.btn_del.clicked.connect(self.sub_amount)
        self.btn_time = QPushButton("시간") 
        self.btn_time.clicked.connect(self.show_clock_window)

        form_box.addWidget(QLabel("상품명"))
        form_box.addWidget(self.input_name)
        form_box.addWidget(QLabel("수량"))
        form_box.addWidget(self.input_amount)
        form_box.addWidget(self.btn_add)
        form_box.addWidget(self.btn_del)
        form_box.addWidget(self.btn_time)
        vbox.addLayout(form_box)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","상품명","수량","판매가","발주가","선택"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        # 오른쪽 자산 테이블
        self.rtable = QTableWidget()
        self.rtable.setColumnCount(1)
        self.rtable.setHorizontalHeaderLabels(["자산"])
        self.rtable.setEditTriggers(self.rtable.NoEditTriggers)
        self.rtable.verticalHeader().setVisible(False)

        # 숫자 버튼 1~9, 10은 백스페이스
        self.num_layout = QGridLayout()
        for i in range(1, 10):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            font = QFont("Arial", 16, QFont.Bold)
            btn.setFont(font)
            btn.setStyleSheet("background-color: gray; color: white;")
            btn.clicked.connect(lambda _, x=i: self.num_clicked(x))
            self.num_layout.addWidget(btn, (i-1)//5, (i-1)%5)
        btn_back = QPushButton("←")
        btn_back.setFixedSize(40, 40)
        btn_back.setFont(QFont("Arial", 16, QFont.Bold))
        btn_back.clicked.connect(self.backspace_clicked)
        self.num_layout.addWidget(btn_back, 1, 4)

        right_vbox = QVBoxLayout()
        right_vbox.addWidget(self.rtable)
        right_vbox.addLayout(self.num_layout)

        hbox = QHBoxLayout()
        hbox.addWidget(self.table)
        hbox.addLayout(right_vbox)
        vbox.addLayout(hbox)

        self.load_inv()
        self.load_bal()
        self.adjustSize()

    # 숫자 버튼 관련
    def num_clicked(self, num):
        current = self.input_amount.text()
        self.input_amount.setText(current + str(num))

    def backspace_clicked(self):
        current = self.input_amount.text()
        self.input_amount.setText(current[:-1])

    def select_name(self, row):
        name = self.table.item(row, 1).text()
        self.input_name.setText(name)

    # 재고/자산 불러오기
    def load_inv(self):
        rows = self.db.fetch_inventory()
        self.table.setRowCount(len(rows))
        for r,(mid,name,amount, price, Ocost) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(mid)))
            self.table.setItem(r, 1, QTableWidgetItem(name))
            self.table.setItem(r, 2, QTableWidgetItem(str(amount)))
            self.table.setItem(r, 3, QTableWidgetItem(str(price)))
            self.table.setItem(r, 4, QTableWidgetItem(str(Ocost)))

            btn = QPushButton("선택")
            btn.clicked.connect(lambda _, row=r: self.select_name(row))
            self.table.setCellWidget(r, 5, btn)

        self.table.resizeColumnsToContents()

    def load_bal(self):
        bal = self.db.fetch_bal()
        self.rtable.setRowCount(1)
        self.rtable.setItem(0, 0, QTableWidgetItem(str(bal)))
        self.rtable.resizeColumnsToContents()

    # 발주/판매 처리
    def add_amount(self):
        name = self.input_name.text().strip()
        amount_text = self.input_amount.text().strip()
        if not name or not amount_text:
            QMessageBox.warning(self,"오류", "이름과 수량을 모두 입력하세요.")
            return
        amount = int(amount_text)
        bal = self.db.fetch_bal()
        ok = self.db.add_amount(name,amount)
        if ok:
            price = self.db.fetch_Ocost(name)
            total_cost =  price * amount
            if total_cost <= bal:
                bal = self.db.subtract_balance(total_cost)
                QMessageBox.information(self,"완료","발주했습니다")
                self.input_name.clear()
                self.input_amount.clear()
                self.load_inv()
                self.load_bal()
            else:
                 QMessageBox.critical(self,"오류","잔액 부족")
        else:
            QMessageBox.critical(self,"실패","발주 중 오류가 발생했습니다.")        

    def sub_amount(self):
        name = self.input_name.text().strip()
        amount_text = self.input_amount.text().strip()
        if not name or not amount_text:
            QMessageBox.warning(self, "오류", "이름과 수량 모두 입력하세요.")
            return
        amount = int(amount_text)
        bal = self.db.fetch_bal()
        num = self.db.fetch_amount(name)
        ok = self.db.subtract_amount(name, amount)
        if ok:
            price = self.db.fetch_price(name)
            total_cost =  price * amount
            if num >= amount:
                bal= self.db.add_balance(total_cost)            
                QMessageBox.information(self, "완료", "판매처리 했습니다")
                self.input_name.clear()
                self.input_amount.clear()
                self.load_inv()
                self.load_bal()
            else:
                 QMessageBox.critical(self,"오류","수량 부족")
        else:
            QMessageBox.critical(self, "실패", "판매처리 중 오류가 발생했습니다.")

    # 시계 창 띄우기
    def show_clock_window(self):
        self.clock_window = ClockWindow()  # clock.py의 ClockWindow
        self.clock_window.show()

