# login_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from cdb_helper import DB, DB_CONFIG
from PyQt5.QtGui import QFont
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인")
        self.db = DB(**DB_CONFIG)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow("아이디", self.username)
        form.addRow("비밀번호", self.password)

        self.btn_login = QPushButton("로그인")
        font = QFont("Arial", 16, QFont.Bold)  # 글씨 크기 16, 굵게
        self.btn_login.setFont(font)            # 버튼에 폰트 적용
        self.btn_login.setStyleSheet("""
        QPushButton {
        border: 4px solid black;  /* 테두리 굵게 */
        border-radius: 15px;        /* 모서리 둥글게 */
        color: black;               /* 글자색 */
        font-weight: bold;          /* 글자 굵게 */
        font-size: 16pt;            /* 글자 크기 */
    }
""")
        self.btn_login.clicked.connect(self.try_login)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def try_login(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()
        if not uid or not pw:
            QMessageBox.warning(self, "오류", "아이디와 비밀번호를 모두 입력하세요.")
            return

        ok = self.db.verify_user(uid, pw)
        if ok:
            self.accept()
        else:
            QMessageBox.critical(self, "실패", "아이디 또는 비밀번호가 올바르지 않습니다.")