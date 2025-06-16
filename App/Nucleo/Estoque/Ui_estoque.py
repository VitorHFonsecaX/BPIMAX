# App/Nucleo/Estoque/Ui_estoque.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox,
    QSpinBox # QSpinBox está em QtWidgets, não precisa mudar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon
# Não precisa importar QDoubleValidator aqui, pois não está sendo usado diretamente.
# Se for usar para alguma validação futura, lembre-se de importar de QtGui.

class Ui_Estoque(QWidget):
    def __init__(self):
        super().__init__()
        # Simula uma conexão com os dados de produtos para visualização e ajuste
        # Em uma aplicação real, você buscaria isso de um banco de dados
        self.produtos_em_estoque = [
            {"codigo": "P001", "nome": "Caneta Esferográfica Azul", "estoque": 150, "localizacao": "Prateleira A1"},
            {"codigo": "P002", "nome": "Caderno Universitário 10 Matérias", "estoque": 80, "localizacao": "Corredor B2"},
            {"codigo": "P003", "nome": "Apagador para Quadro Branco", "estoque": 40, "localizacao": "Prateleira A5"},
            {"codigo": "P004", "nome": "Lápis de Cor Faber-Castell", "estoque": 200, "localizacao": "Gaveta C3"},
        ]
        self.setupUi()
        self._populate_estoque_table(self.produtos_em_estoque)


    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        self.setStyleSheet("QLabel, QLineEdit, QComboBox, QTableWidget { color: black; }")

        title_label = QLabel("Gestão de Estoque")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(title_label)

        # Barra de Ferramentas / Filtros
        toolbar_layout = QHBoxLayout()
        
        self.search_estoque_input = QLineEdit()
        self.search_estoque_input.setPlaceholderText("Buscar Produto no Estoque (Nome, Código...)")
        self.search_estoque_input.setFixedHeight(30)
        self.search_estoque_input.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.search_estoque_input)
        
        toolbar_layout.addStretch(1)

        # Botões de Ação de Estoque (Ex: Entrada, Saída)
        self.btn_entrada_estoque = QPushButton("Entrada de Estoque")
        self.btn_entrada_estoque.setFixedHeight(35)
        self.btn_entrada_estoque.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_entrada_estoque.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btn_entrada_estoque.setIcon(QIcon("Recursos/icones/add_to_stock.png"))
        toolbar_layout.addWidget(self.btn_entrada_estoque)

        self.btn_saida_estoque = QPushButton("Saída de Estoque")
        self.btn_saida_estoque.setFixedHeight(35)
        self.btn_saida_estoque.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_saida_estoque.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        self.btn_saida_estoque.setIcon(QIcon("Recursos/icones/remove_from_stock.png"))
        toolbar_layout.addWidget(self.btn_saida_estoque)


        main_layout.addLayout(toolbar_layout)

        # Tabela de Estoque
        self.estoque_table = QTableWidget()
        self.estoque_table.setColumnCount(4) # Código, Nome, Estoque Atual, Localização
        self.estoque_table.setHorizontalHeaderLabels(["Código", "Nome do Produto", "Estoque Atual", "Localização"])
        self.estoque_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.estoque_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.estoque_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.estoque_table.setStyleSheet("""
            QTableWidget {
                color: black;
                background-color: #f8f8f8;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                color: black;
                padding: 5px;
                border: 1px solid #ccc;
            }
        """)
        main_layout.addWidget(self.estoque_table)

        self.search_estoque_input.textChanged.connect(self._apply_estoque_filters)
    
    def _populate_estoque_table(self, data):
        self.estoque_table.setRowCount(0)
        for row_idx, produto in enumerate(data):
            self.estoque_table.insertRow(row_idx)
            self.estoque_table.setItem(row_idx, 0, QTableWidgetItem(produto["codigo"]))
            self.estoque_table.setItem(row_idx, 1, QTableWidgetItem(produto["nome"]))
            self.estoque_table.setItem(row_idx, 2, QTableWidgetItem(str(produto["estoque"])))
            self.estoque_table.setItem(row_idx, 3, QTableWidgetItem(produto["localizacao"]))
            
            for col in range(self.estoque_table.columnCount()):
                item = self.estoque_table.item(row_idx, col)
                if item:
                    item.setForeground(Qt.black)

    def _apply_estoque_filters(self):
        search_text = self.search_estoque_input.text().lower()
        
        filtered_data = []
        for produto in self.produtos_em_estoque:
            match_search = (search_text in produto["nome"].lower() or 
                            search_text in produto["codigo"].lower() or
                            search_text in produto["localizacao"].lower())
            
            if match_search:
                filtered_data.append(produto)
        
        self._populate_estoque_table(filtered_data)