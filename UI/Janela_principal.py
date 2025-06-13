from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt

class JanelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Loja")
        self.resize(1000, 600)

        # Layout geral (horizontal)
        layout_geral = QHBoxLayout(self)

        # === Menu Lateral ===
        self.menu_lateral = QVBoxLayout()
        self.menu_lateral.setAlignment(Qt.AlignTop)

        self.btn_produtos = QPushButton("Produtos")
        self.btn_vendas = QPushButton("Vendas")
        self.btn_clientes = QPushButton("Clientes")
        self.btn_estoque = QPushButton("Estoque")
        self.btn_relatorios = QPushButton("Relatórios")
        self.menu_lateral.addWidget(self.btn_produtos)
        self.menu_lateral.addWidget(self.btn_vendas)
        self.menu_lateral.addWidget(self.btn_clientes)
        self.menu_lateral.addWidget(self.btn_estoque)
        self.menu_lateral.addWidget(self.btn_relatorios)

        # === Área de conteúdo ===
        self.paginas = QStackedWidget()
        self.paginas.addWidget(QLabel("Página de Produtos"))
        self.paginas.addWidget(QLabel("Página de Vendas"))
        self.paginas.addWidget(QLabel("Página de Clientes"))
        self.paginas.addWidget(QLabel("Página de Estoque"))
        self.paginas.addWidget(QLabel("Página de Relatórios"))

        # Conectando os botões às páginas
        self.btn_produtos.clicked.connect(lambda: self.paginas.setCurrentIndex(0))
        self.btn_vendas.clicked.connect(lambda: self.paginas.setCurrentIndex(1))
        self.btn_clientes.clicked.connect(lambda: self.paginas.setCurrentIndex(2))
        self.btn_estoque.clicked.connect(lambda: self.paginas.setCurrentIndex(3))
        self.btn_relatorios.clicked.connect(lambda: self.paginas.setCurrentIndex(4))

        # Adiciona os layouts ao layout principal
        layout_geral.addLayout(self.menu_lateral, 1)
        layout_geral.addWidget(self.paginas, 4)