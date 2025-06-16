# App/Nucleo/Janela_principal.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QFont

# IMPORTAR AS CLASSES COMPLETAS DOS MÓDULOS
# Certifique-se de que estes caminhos estão corretos e apontam para os arquivos com as UIs completas
from App.Nucleo.Vendas.Ui_vendas import Ui_Vendas
from App.Nucleo.Clientes.Ui_clientes import Ui_Clientes
# (Você criará os módulos completos para Produtos, Estoque e Relatórios futuramente)
# from App.Nucleo.Produtos.Ui_produtos import Ui_Produtos
# from App.Nucleo.Estoque.Ui_estoque import Ui_Estoque
# from App.Nucleo.Relatorios.Ui_relatorios import Ui_Relatorios
# from App.Nucleo.Configuracoes.Ui_configuracoes import Ui_Configuracoes # Futura importação

# --- Classe para a Tela Inicial / Boas-vindas ---
class Ui_WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Bem-vindo ao Meu Sistema ERP!")
        label.setFont(QFont("Arial", 24, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #34495e;")
        layout.addWidget(label)

        sub_label = QLabel("Selecione uma opção no menu lateral para começar.")
        sub_label.setFont(QFont("Arial", 14))
        sub_label.setAlignment(Qt.AlignCenter)
        sub_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        layout.addWidget(sub_label)

        # Para centralizar o texto verticalmente
        layout.addStretch(1)
        layout.addWidget(label)
        layout.addWidget(sub_label)
        layout.addStretch(1)

        self.setStyleSheet("background-color: #ecf0f1;")

# --- Classes Placeholder para módulos AINDA NÃO DESENVOLVIDOS COMPLETAMENTE ---
class Ui_Produtos(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Produtos (Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #e0f7fa; color: #333; font-size: 20px;")

class Ui_Estoque(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Estoque (Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #ffe0b2; color: #333; font-size: 20px;")

class Ui_Relatorios(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Relatórios (Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #e1bee7; color: #333; font-size: 20px;")

# NOVA CLASSE PLACEHOLDER PARA CONFIGURAÇÕES
class Ui_Configuracoes(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Conteúdo da Tela de Configurações (Placeholder)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setStyleSheet("background-color: #bbdefb; color: #333; font-size: 20px;")


class JanelaPrincipal(QMainWindow):
    logout_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerenciamento")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setupUi()

    def setupUi(self):
        # --- 1. Painel do Menu Lateral Esquerdo ---
        self.side_menu_frame = QFrame(self)
        self.side_menu_frame.setFixedWidth(200)
        self.side_menu_frame.setStyleSheet("background-color: #2c3e50; color: white;")
        self.side_menu_layout = QVBoxLayout(self.side_menu_frame)
        self.side_menu_layout.setContentsMargins(10, 20, 10, 20)
        self.side_menu_layout.setSpacing(10)

        menu_title = QLabel("Meu Sistema ERP")
        font_title = QFont("Arial", 14, QFont.Bold)
        menu_title.setFont(font_title)
        menu_title.setAlignment(Qt.AlignCenter)
        menu_title.setStyleSheet("margin-bottom: 20px; color: #ecf0f1;")
        self.side_menu_layout.addWidget(menu_title)

        from PySide6.QtWidgets import QButtonGroup
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self._handle_menu_button_click)

        self.btn_inicio = self._create_menu_button("Início", None)
        self.side_menu_layout.addWidget(self.btn_inicio)

        # ORDEM DOS BOTÕES DO MENU
        self.btn_produtos = self._create_menu_button("Produtos", "Recursos/icones/produtos.png")
        self.btn_estoque = self._create_menu_button("Estoque", "Recursos/icones/estoque.png")
        self.btn_vendas = self._create_menu_button("Vendas", "Recursos/icones/vendas.png")
        self.btn_clientes = self._create_menu_button("Clientes", "Recursos/icones/clientes.png")
        self.btn_relatorios = self._create_menu_button("Relatórios", "Recursos/icones/relatorios.png")
        self.btn_configuracoes = self._create_menu_button("Configurações", "Recursos/icones/configuracoes.png") # NOVO BOTÃO

        self.side_menu_layout.addWidget(self.btn_produtos)
        self.side_menu_layout.addWidget(self.btn_estoque)
        self.side_menu_layout.addWidget(self.btn_vendas)
        self.side_menu_layout.addWidget(self.btn_clientes)
        self.side_menu_layout.addWidget(self.btn_relatorios)
        self.side_menu_layout.addWidget(self.btn_configuracoes) # ADICIONANDO O NOVO BOTÃO

        self.side_menu_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.btn_logout = QPushButton("Deslogar")
        self.btn_logout.setFont(QFont("Arial", 6, QFont.Bold))
        self.btn_logout.setFixedHeight(25)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.side_menu_layout.addWidget(self.btn_logout)
        self.btn_logout.clicked.connect(self.logout_requested.emit)

        self.main_layout.addWidget(self.side_menu_frame)

        # --- 2. Área de Conteúdo Principal (QStackedWidget) ---
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setStyleSheet("background-color: #f0f2f5;")

        self.page_welcome = Ui_WelcomePage()
        self.stacked_widget.addWidget(self.page_welcome) # Índice 0

        self.page_produtos = Ui_Produtos()
        self.page_estoque = Ui_Estoque()
        self.page_vendas = Ui_Vendas()
        self.page_clientes = Ui_Clientes()
        self.page_relatorios = Ui_Relatorios()
        self.page_configuracoes = Ui_Configuracoes() # NOVA PÁGINA

        self.stacked_widget.addWidget(self.page_produtos)    # Índice 1
        self.stacked_widget.addWidget(self.page_estoque)     # Índice 2
        self.stacked_widget.addWidget(self.page_vendas)      # Índice 3
        self.stacked_widget.addWidget(self.page_clientes)    # Índice 4
        self.stacked_widget.addWidget(self.page_relatorios)  # Índice 5
        self.stacked_widget.addWidget(self.page_configuracoes) # NOVO ÍNDICE 6

        self.main_layout.addWidget(self.stacked_widget, 1)

        # --- 3. Painel Lateral Direito (Lembretes e Promoções) ---
        self.right_panel_frame = QFrame(self)
        self.right_panel_frame.setFixedWidth(250)
        self.right_panel_frame.setStyleSheet("background-color: #ecf0f1; border-left: 1px solid #bdc3c7;")
        self.right_panel_layout = QVBoxLayout(self.right_panel_frame)
        self.right_panel_layout.setContentsMargins(15, 20, 15, 20)
        self.right_panel_layout.setSpacing(15)

        right_panel_title = QLabel("Lembretes & Promoções")
        font_right_title = QFont("Arial", 12, QFont.Bold)
        right_panel_title.setFont(font_right_title)
        right_panel_title.setAlignment(Qt.AlignCenter)
        right_panel_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        self.right_panel_layout.addWidget(right_panel_title)

        self.reminders_promotions_content = QLabel("Conteúdo para lembretes e promoções virá aqui.")
        self.reminders_promotions_content.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.reminders_promotions_content.setWordWrap(True)
        self.reminders_promotions_content.setStyleSheet("color: #7f8c8d; font-style: italic;")
        self.right_panel_layout.addWidget(self.reminders_promotions_content)
        self.right_panel_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.main_layout.addWidget(self.right_panel_frame)


        # --- Conectar os botões do menu aos índices do QStackedWidget central ---
        self.btn_inicio.clicked.connect(lambda: self._show_page_and_manage_right_panel(0))
        self.btn_produtos.clicked.connect(lambda: self._show_page_and_manage_right_panel(1))
        self.btn_estoque.clicked.connect(lambda: self._show_page_and_manage_right_panel(2))
        self.btn_vendas.clicked.connect(lambda: self._show_page_and_manage_right_panel(3))
        self.btn_clientes.clicked.connect(lambda: self._show_page_and_manage_right_panel(4))
        self.btn_relatorios.clicked.connect(lambda: self._show_page_and_manage_right_panel(5))
        self.btn_configuracoes.clicked.connect(lambda: self._show_page_and_manage_right_panel(6)) # NOVA CONEXÃO

        # Estado inicial: Mostrar a tela de boas-vindas e o painel de lembretes
        self.stacked_widget.setCurrentIndex(0)
        self.right_panel_frame.show()


    def _create_menu_button(self, text, icon_path=None):
        button = QPushButton(text)
        button.setFixedSize(180, 50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4a6582;
            }
            QPushButton:checked {
                background-color: #1abc9c;
            }
        """)
        button.setCheckable(True)
        self.button_group.addButton(button)
        
        if icon_path:
            try:
                icon = QIcon(icon_path)
                button.setIcon(icon)
                button.setIconSize(QSize(24, 24))
                button.setLayoutDirection(Qt.LeftToRight)
            except Exception as e:
                print(f"Erro ao carregar ícone {icon_path}: {e}")
        return button

    def _handle_menu_button_click(self, button):
        for b in self.button_group.buttons():
            if b != button:
                b.setChecked(False)

    def _show_page_and_manage_right_panel(self, index):
        self.stacked_widget.setCurrentIndex(index)

        # Esconde o painel lateral direito para telas que precisam de mais espaço
        # E mostra para a tela de início ou outras que não precisam do espaço total
        if index == 0: # Índice da tela de Boas-vindas
            self.right_panel_frame.show()
        elif index == 3: # Índice da tela de Vendas (PDV)
            self.right_panel_frame.hide()
        elif index == 4: # Índice da tela de Clientes (Cadastro/Gestão)
            self.right_panel_frame.hide()
        elif index == 6: # Índice da tela de Configurações - Adicionado aqui
            self.right_panel_frame.hide() # Configurações provavelmente precisa de tela cheia
        else: # Para outras telas, você decide se mostra ou esconde
            self.right_panel_frame.show()