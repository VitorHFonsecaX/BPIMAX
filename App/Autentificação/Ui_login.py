from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class TelaLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Sistema de Loja")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Usuário:"))
        self.usuario_input = QLineEdit()
        layout.addWidget(self.usuario_input)

        layout.addWidget(QLabel("Senha:"))
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.senha_input)

        self.botao_login = QPushButton("Entrar")
        layout.addWidget(self.botao_login)

        self.setLayout(layout)
