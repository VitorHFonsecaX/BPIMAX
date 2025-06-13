# App/Nucleo/Ui_login.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap # Para o logo, se for usar imagem

class Ui_Login(QWidget):
    # Sinal personalizado que será emitido quando o login for bem-sucedido
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Configurações básicas da janela de login
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 500) # x, y, largura, altura

        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50) # Margens internas
        main_layout.setSpacing(20) # Espaçamento entre os widgets

        # Frame para agrupar os elementos do formulário de login (opcional, para estilização)
        login_frame = QFrame(self)
        login_frame.setFrameShape(QFrame.StyledPanel)
        login_frame.setFrameShadow(QFrame.Raised)
        frame_layout = QVBoxLayout(login_frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(15)

        # 1. Logo da Aplicação (placeholder)
        self.logo_label = QLabel("Logo da Aplicação") # Ou use QPixmap para carregar a imagem
        # Exemplo para carregar imagem (comente a linha acima e descomente as abaixo para usar):
        # try:
        #     pixmap = QPixmap("Recursos/icones/logo_app.png") # Caminho relativo da raiz do projeto
        #     if not pixmap.isNull():
        #         self.logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #         self.logo_label.setAlignment(Qt.AlignCenter)
        #     else:
        #         self.logo_label.setText("Erro ao carregar logo")
        # except Exception as e:
        #     self.logo_label.setText(f"Logo (Erro: {e})")

        font_logo = QFont("Arial", 24, QFont.Bold)
        self.logo_label.setFont(font_logo)
        self.logo_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(self.logo_label)

        # Espaçador
        frame_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # 2. Título "Login"
        title_label = QLabel("Entrar no Sistema")
        font_title = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(font_title)
        title_label.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title_label)

        # 3. Campo Usuário
        label_usuario = QLabel("Usuário:")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu nome de usuário")
        frame_layout.addWidget(label_usuario)
        frame_layout.addWidget(self.input_usuario)

        # 4. Campo Senha
        label_senha = QLabel("Senha:")
        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Digite sua senha")
        self.input_senha.setEchoMode(QLineEdit.Password) # Para esconder a senha
        frame_layout.addWidget(label_senha)
        frame_layout.addWidget(self.input_senha)

        # Espaçador
        frame_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # 5. Botão Login
        self.btn_login = QPushButton("Login")
        font_button = QFont("Arial", 12, QFont.Bold)
        self.btn_login.setFont(font_button)
        self.btn_login.setFixedHeight(40) # Altura fixa para o botão
        self.btn_login.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;") # Estilo básico
        frame_layout.addWidget(self.btn_login)

        # Adiciona o frame ao layout principal
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)) # Espaçador superior
        main_layout.addWidget(login_frame)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)) # Espaçador inferior

        # Conectar o sinal do botão (apenas para demonstração da UI)
        self.btn_login.clicked.connect(self._simulate_login)

    def _simulate_login(self):
        # Este método é um placeholder para simular o login para fins de UI.
        # No futuro, aqui você chamaria a lógica de autenticação do Controlador.
        print(f"Simulando login com Usuário: {self.input_usuario.text()} e Senha: {'*' * len(self.input_senha.text())}")
        # Emitir o sinal de login bem-sucedido para que a janela principal possa ser mostrada
        self.login_successful.emit()