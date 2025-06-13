# App/Nucleo/Janela_principal.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

# Classes de UI para cada módulo (serão mais elaboradas no futuro)
class Ui_Produtos(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Produtos")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #e0f7fa;") # Cor para diferenciar

class Ui_Estoque(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Estoque")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #ffe0b2;") # Cor para diferenciar

class Ui_Vendas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Vendas")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #c8e6c9;") # Cor para diferenciar

class Ui_Clientes(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Clientes")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #f8bbd0;") # Cor para diferenciar

class Ui_Relatorios(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Relatórios")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #e1bee7;") # Cor para diferenciar


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerenciamento")
        self.setGeometry(100, 100, 1024, 768) # x, y, largura, altura

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0) # Remove margens do layout principal
        self.main_layout.setSpacing(0) # Remove espaçamento entre os widgets

        self.setupUi()

    def setupUi(self):
        # 1. Painel do Menu Lateral
        self.side_menu_frame = QFrame(self)
        self.side_menu_frame.setFixedWidth(200) # Largura fixa para o menu
        self.side_menu_frame.setStyleSheet("background-color: #2c3e50; color: white;") # Cor de fundo do menu
        self.side_menu_layout = QVBoxLayout(self.side_menu_frame)
        self.side_menu_layout.setContentsMargins(10, 20, 10, 20)
        self.side_menu_layout.setSpacing(10)

        # Título do Menu/Logo
        menu_title = QLabel("Meu Sistema ERP")
        font_title = QFont("Arial", 14, QFont.Bold)
        menu_title.setFont(font_title)
        menu_title.setAlignment(Qt.AlignCenter)
        menu_title.setStyleSheet("margin-bottom: 20px; color: #ecf0f1;")
        self.side_menu_layout.addWidget(menu_title)

        # Botões do Menu
        self.btn_produtos = self._create_menu_button("Produtos", "Recursos/icones/produtos.png")
        self.btn_estoque = self._create_menu_button("Estoque", "Recursos/icones/estoque.png")
        self.btn_vendas = self._create_menu_button("Vendas", "Recursos/icones/vendas.png")
        self.btn_clientes = self._create_menu_button("Clientes", "Recursos/icones/clientes.png")
        self.btn_relatorios = self._create_menu_button("Relatórios", "Recursos/icones/relatorios.png")

        self.side_menu_layout.addWidget(self.btn_produtos)
        self.side_menu_layout.addWidget(self.btn_estoque)
        self.side_menu_layout.addWidget(self.btn_vendas)
        self.side_menu_layout.addWidget(self.btn_clientes)
        self.side_menu_layout.addWidget(self.btn_relatorios)

        self.side_menu_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)) # Espaçador para empurrar botões para cima

        self.main_layout.addWidget(self.side_menu_frame)

        # 2. Área de Conteúdo Principal (QStackedWidget)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setStyleSheet("background-color: #f0f2f5;") # Cor de fundo da área de conteúdo

        # Adiciona as páginas de cada módulo ao QStackedWidget
        self.page_produtos = Ui_Produtos()
        self.page_estoque = Ui_Estoque()
        self.page_vendas = Ui_Vendas()
        self.page_clientes = Ui_Clientes()
        self.page_relatorios = Ui_Relatorios()

        self.stacked_widget.addWidget(self.page_produtos)    # Index 0
        self.stacked_widget.addWidget(self.page_estoque)     # Index 1
        self.stacked_widget.addWidget(self.page_vendas)      # Index 2
        self.stacked_widget.addWidget(self.page_clientes)    # Index 3
        self.stacked_widget.addWidget(self.page_relatorios)  # Index 4

        self.main_layout.addWidget(self.stacked_widget)

        # Conectar os botões do menu aos índices do QStackedWidget
        self.btn_produtos.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_estoque.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_vendas.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_clientes.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.btn_relatorios.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))


    def _create_menu_button(self, text, icon_path=None):
        button = QPushButton(text)
        button.setFixedSize(180, 50) # Largura e altura fixas para o botão
        button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4a6582;
            }
            QPushButton:checked {
                background-color: #1abc9c; /* Cor para botão selecionado */
            }
        """)
        button.setCheckable(True) # Torna o botão selecionável (toggle)
        # Ajuste para garantir que apenas um botão fique "selecionado"
        if hasattr(self, 'button_group'):
            self.button_group.addButton(button)
        else:
            from PySide6.QtWidgets import QButtonGroup
            self.button_group = QButtonGroup(self)
            self.button_group.setExclusive(True) # Apenas um botão pode ser checado por vez
            self.button_group.addButton(button)


        if icon_path:
            # Tenta carregar o ícone. Se falhar, o botão aparecerá sem ícone.
            try:
                icon = QIcon(icon_path)
                button.setIcon(icon)
                button.setIconSize(QSize(24, 24)) # Tamanho do ícone
                # Ajusta o texto para ficar ao lado do ícone
                button.setLayoutDirection(Qt.LeftToRight) # Ícone à esquerda, texto à direita
            except Exception as e:
                print(f"Erro ao carregar ícone {icon_path}: {e}")
        return button