from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QApplication
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Loja")
        self.resize(1000, 600)

        # Aplicar estilo QSS
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5; /* Cor de fundo geral */
                font-family: 'Segoe UI', sans-serif;
            }
            #menuLateral {
                background-color: #2c3e50; /* Cor de fundo do menu lateral */
                border-right: 1px solid #34495e;
                padding: 10px;
            }
            QPushButton {
                background-color: #3498db; /* Azul primário */
                color: white;
                border: none;
                padding: 12px 15px;
                text-align: left; /* Alinha texto à esquerda */
                border-radius: 5px;
                margin-bottom: 8px; /* Espaço entre botões */
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9; /* Azul mais escuro no hover */
            }
            QPushButton:checked { /* Estilo para o botão selecionado/ativo */
                background-color: #e67e22; /* Laranja para destaque */
                font-weight: bold;
                border-left: 5px solid #d35400; /* Borda lateral para destaque */
            }
            QLabel {
                font-size: 24px;
                color: #34495e;
                padding: 20px;
                text-align: center;
            }
            QStackedWidget {
                background-color: white;
                border-radius: 8px;
                margin: 10px; /* Margem em volta da área de conteúdo */
            }
        """)

        # Layout geral (horizontal)
        layout_geral = QHBoxLayout(self)
        layout_geral.setContentsMargins(0, 0, 0, 0) # Remove margens do layout geral
        layout_geral.setSpacing(0) # Remove espaçamento entre os elementos principais

        # === Menu Lateral ===
        self.menu_lateral = QVBoxLayout()
        self.menu_lateral.setAlignment(Qt.AlignTop)
        self.menu_lateral.setContentsMargins(15, 20, 15, 20) # Margens internas do menu
        self.menu_lateral.setSpacing(10) # Espaçamento entre os widgets do menu

        # Container para o menu lateral para aplicar o QSS
        menu_container = QWidget()
        menu_container.setObjectName("menuLateral")
        menu_container.setLayout(self.menu_lateral)
        menu_container.setFixedWidth(200) # Largura fixa para o menu lateral

        # Criação de botões com ícones e conectando
        self.btn_produtos = self._create_nav_button("Produtos", "icons/produtos.png", 0)
        self.btn_vendas = self._create_nav_button("Vendas", "icons/vendas.png", 1)
        self.btn_clientes = self._create_nav_button("Clientes", "icons/clientes.png", 2)
        self.btn_estoque = self._create_nav_button("Estoque", "icons/estoque.png", 3)
        self.btn_relatorios = self._create_nav_button("Relatórios", "icons/relatorios.png", 4)

        self.menu_lateral.addWidget(self.btn_produtos)
        self.menu_lateral.addWidget(self.btn_vendas)
        self.menu_lateral.addWidget(self.btn_clientes)
        self.menu_lateral.addWidget(self.btn_estoque)
        self.menu_lateral.addWidget(self.btn_relatorios)
        self.menu_lateral.addStretch() # Empurra os botões para cima

        # === Área de conteúdo ===
        self.paginas = QStackedWidget()
        self.paginas.addWidget(self._create_content_page("Página de Produtos - Gerencie seus itens aqui."))
        self.paginas.addWidget(self._create_content_page("Página de Vendas - Registre novas vendas e acompanhe o histórico."))
        self.paginas.addWidget(self._create_content_page("Página de Clientes - Visualize e edite informações dos clientes."))
        self.paginas.addWidget(self._create_content_page("Página de Estoque - Monitore e atualize seu inventário."))
        self.paginas.addWidget(self._create_content_page("Página de Relatórios - Analise dados e gere relatórios."))

        # Adiciona os layouts ao layout principal
        layout_geral.addWidget(menu_container)
        layout_geral.addWidget(self.paginas, 1) # Ocupa o restante do espaço

        # Define o primeiro botão como checked/ativo ao iniciar
        self.btn_produtos.setChecked(True)
        self.btn_produtos.clicked.emit() # Garante que a página inicial seja carregada

    def _create_nav_button(self, text, icon_path, page_index):
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24)) # Define o tamanho do ícone
        btn.setCheckable(True) # Torna o botão "selecionável"
        btn.setAutoExclusive(True) # Garante que apenas um botão por vez pode ser checked
        btn.clicked.connect(lambda: self.paginas.setCurrentIndex(page_index))
        return btn

    def _create_content_page(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        # Cria um contêiner para cada página para aplicar estilos individuais, se necessário
        page_widget = QWidget()
        page_layout = QVBoxLayout(page_widget)
        page_layout.addWidget(label)
        page_layout.setAlignment(Qt.AlignCenter)
        return page_widget