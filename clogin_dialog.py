# login_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from cdb_helper import DB, DB_CONFIG

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("로그인")
        self.setFixedSize(400, 250)  # 창 크기 고정
        self.db = DB(**DB_CONFIG)

        # 공통 폰트
        label_font = QFont("Arial", 14, QFont.Bold)
        input_font = QFont("Arial", 12)

        # 입력칸 스타일
        line_edit_style = """
        QLineEdit {
            border: 2px solid black;    /* 테두리 굵기 */
            border-radius: 15px;        /* 모서리 둥글게 */
            padding: 5px;               /* 안쪽 여백 */
            font-size: 12pt;            /* 글자 크기 */
        }
        """

        # 아이디 입력
        self.username = QLineEdit()
        self.username.setFixedHeight(40)
        self.username.setFont(input_font)
        self.username.setStyleSheet(line_edit_style)

        # 비밀번호 입력
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(40)
        self.password.setFont(input_font)
        self.password.setStyleSheet(line_edit_style)

        # 라벨 글씨 스타일을 QFormLayout에 적용
        form = QFormLayout()
        form.addRow(self._styled_label("아이디", label_font), self.username)
        form.addRow(self._styled_label("비밀번호", label_font), self.password)

        # 로그인 버튼
        self.btn_login = QPushButton("로그인")
        btn_font = QFont("Arial", 16, QFont.Bold)
        self.btn_login.setFont(btn_font)
        self.btn_login.setStyleSheet("""
            QPushButton {
                border: 4px solid black; 
                border-radius: 15px;
                color: black;
                font-weight: bold;
                font-size: 16pt;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.btn_login.setFixedHeight(50)
        self.btn_login.clicked.connect(self.try_login)

        # 전체 레이아웃
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)  # 상, 좌, 하, 우 여백
        layout.setSpacing(15)  # 내부 위젯 간 간격
        layout.addLayout(form)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def _styled_label(self, text, font):
        """QFormLayout용 라벨 생성"""
        from PyQt5.QtWidgets import QLabel
        label = QLabel(text)
        label.setFont(font)
        return label

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
