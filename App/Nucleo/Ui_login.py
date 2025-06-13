# App/Nucleo/Ui_login.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap

class Ui_Login(QWidget):
    # Sinal personalizado que será emitido quando o login for bem-sucedido
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Configurações básicas da janela de login
        self.setWindowTitle("Login do Sistema")
        # Tamanho fixo e mais adequado para uma tela de login
        self.setFixedSize(450, 550) # Largura, altura

        # Layout principal vertical para centralizar o frame de login
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # Margens zero para controle total com spacers
        main_layout.setSpacing(0)

        # Frame principal para o formulário de login
        login_frame = QFrame(self)
        login_frame.setFrameShape(QFrame.NoFrame) # Sem borda de frame
        login_frame.setFrameShadow(QFrame.Plain)
        # Estilo para o frame: um fundo claro e sombra sutil para destacar
        login_frame.setStyleSheet("""
            QFrame {
                background-color: #f7f9fc;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }
        """)
        login_frame.setMinimumSize(350, 450) # Garante um tamanho mínimo para o frame do formulário
        login_frame.setMaximumSize(350, 450) # Garante um tamanho máximo

        frame_layout = QVBoxLayout(login_frame)
        frame_layout.setContentsMargins(30, 30, 30, 30) # Margens internas do frame
        frame_layout.setSpacing(15) # Espaçamento entre os widgets dentro do frame

        # 1. Logo da Aplicação
        self.logo_label = QLabel() # Inicializa sem texto, será preenchido pela imagem ou placeholder
        try:
            # Tenta carregar a imagem do logo
            pixmap = QPixmap("Recursos/icones/logo_app.png")
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.logo_label.setAlignment(Qt.AlignCenter)
            else:
                self.logo_label.setText("LOGO") # Fallback se a imagem não for encontrada
                self.logo_label.setFont(QFont("Arial", 28, QFont.Bold))
                self.logo_label.setStyleSheet("color: #34495e;")
                self.logo_label.setAlignment(Qt.AlignCenter)
        except Exception as e:
            # Fallback robusto caso haja erro no caminho ou carregamento
            self.logo_label.setText("LOGO")
            self.logo_label.setFont(QFont("Arial", 28, QFont.Bold))
            self.logo_label.setStyleSheet("color: #34495e;")
            self.logo_label.setAlignment(Qt.AlignCenter)
            print(f"Aviso: Não foi possível carregar 'Recursos/icones/logo_app.png'. Erro: {e}")

        frame_layout.addWidget(self.logo_label)

        # Espaçador
        frame_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # 2. Título "Login"
        title_label = QLabel("Entrar no Sistema")
        font_title = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(font_title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        frame_layout.addWidget(title_label)

        # 3. Campo Usuário
        label_usuario = QLabel("Usuário:")
        label_usuario.setStyleSheet("color: #34495e; font-weight: bold;")
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu nome de usuário")
        self.input_usuario.setFixedHeight(35) # Altura fixa
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        frame_layout.addWidget(label_usuario)
        frame_layout.addWidget(self.input_usuario)

        # 4. Campo Senha
        label_senha = QLabel("Senha:")
        label_senha.setStyleSheet("color: #34495e; font-weight: bold;")
        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Digite sua senha")
        self.input_senha.setEchoMode(QLineEdit.Password)
        self.input_senha.setFixedHeight(35) # Altura fixa
        self.input_senha.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)
        frame_layout.addWidget(label_senha)
        frame_layout.addWidget(self.input_senha)

        # Espaçador
        frame_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # 5. Botão Login
        self.btn_login = QPushButton("Login")
        font_button = QFont("Arial", 14, QFont.Bold)
        self.btn_login.setFont(font_button)
        self.btn_login.setFixedHeight(45) # Altura um pouco maior
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; /* Verde esmeralda */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60; /* Verde mais escuro ao passar o mouse */
            }
            QPushButton:pressed {
                background-color: #1e8449; /* Verde ainda mais escuro ao clicar */
            }
        """)
        frame_layout.addWidget(self.btn_login)

        # Adiciona espaçadores expansíveis para centralizar o login_frame no main_layout
        main_layout.addStretch(1) # Empurra o frame para baixo
        main_layout.addWidget(login_frame, alignment=Qt.AlignCenter) # Centraliza o frame
        main_layout.addStretch(1) # Empurra o frame para cima

        # Define o foco inicial no campo de usuário
        self.input_usuario.setFocus()

        # Conecta o sinal do botão (apenas para demonstração da UI)
        self.btn_login.clicked.connect(self._simulate_login)

    def _simulate_login(self):
        # Este método é um placeholder para simular o login para fins de UI.
        # No futuro, aqui você chamaria a lógica de autenticação do Controlador.
        print(f"Simulando login com Usuário: {self.input_usuario.text()} e Senha: {'*' * len(self.input_senha.text())}")
        # Emitir o sinal de login bem-sucedido para que a janela principal possa ser mostrada
        self.login_successful.emit()