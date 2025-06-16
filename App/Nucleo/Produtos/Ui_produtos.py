# App/Nucleo/Produtos/Ui_produtos.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget, QGroupBox,
    QMessageBox, QSpacerItem, QSizePolicy, QFormLayout, QComboBox
    # QDoubleValidator REMOVIDO DAQUI
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon, QDoubleValidator # <--- CORRIGIDO AQUI: QDoubleValidator de QtGui

class Ui_Produtos(QWidget):
    def __init__(self):
        super().__init__()
        self.produtos_data = [] # Lista para armazenar os dados dos produtos
        self.setupUi()
        self._load_sample_produtos_data() # Carrega alguns dados de exemplo

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        self.setStyleSheet("QLabel, QLineEdit, QComboBox, QTableWidget { color: black; }")

        self.produtos_stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.produtos_stacked_widget)

        # --- Página 1: Listagem de Produtos ---
        self.list_produtos_page = QWidget()
        self.produtos_stacked_widget.addWidget(self.list_produtos_page)
        self._setup_list_produtos_page()

        # --- Página 2: Formulário de Cadastro/Edição de Produto ---
        self.new_produto_page = QWidget()
        self.produtos_stacked_widget.addWidget(self.new_produto_page)
        self._setup_new_produto_page()

        self.produtos_stacked_widget.setCurrentIndex(0) # Inicia na página de listagem

    def _setup_list_produtos_page(self):
        layout = QVBoxLayout(self.list_produtos_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        title_label = QLabel("Gestão de Produtos")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title_label)

        # Barra de Ferramentas / Filtros
        toolbar_layout = QHBoxLayout()
        
        self.search_produto_input = QLineEdit()
        self.search_produto_input.setPlaceholderText("Buscar Produto (Nome, Código...)")
        self.search_produto_input.setFixedHeight(30)
        self.search_produto_input.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.search_produto_input)
        
        toolbar_layout.addStretch(1)

        self.btn_new_produto = QPushButton("Novo Produto")
        self.btn_new_produto.setFixedHeight(35)
        self.btn_new_produto.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_new_produto.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_new_produto.setIcon(QIcon("Recursos/icones/add.png"))
        self.btn_new_produto.clicked.connect(self._show_new_produto_form)
        toolbar_layout.addWidget(self.btn_new_produto)

        layout.addLayout(toolbar_layout)

        # Tabela de Produtos
        self.produtos_table = QTableWidget()
        self.produtos_table.setColumnCount(4) # Código, Nome, Preço, Estoque (Qtde)
        self.produtos_table.setHorizontalHeaderLabels(["Código", "Nome do Produto", "Preço de Venda", "Estoque Atual"])
        self.produtos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.produtos_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.produtos_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.produtos_table.itemDoubleClicked.connect(self._edit_produto)
        self.produtos_table.setStyleSheet("""
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
        layout.addWidget(self.produtos_table)

        self.search_produto_input.textChanged.connect(self._apply_produto_filters)

    def _setup_new_produto_page(self):
        layout = QVBoxLayout(self.new_produto_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.new_produto_title_label = QLabel("Cadastrar Novo Produto")
        self.new_produto_title_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(self.new_produto_title_label)

        # Formulário de Produto
        form_groupbox = QGroupBox("Dados do Produto")
        form_groupbox.setStyleSheet("QGroupBox { color: black; }")
        form_layout = QFormLayout(form_groupbox)
        form_layout.setContentsMargins(10, 20, 10, 10)
        form_layout.setSpacing(10)

        input_style = "border: 1px solid #bdc3c7; border-radius: 5px; padding: 8px; color: black;"

        self.produto_id_label = QLabel("Código do Produto: (Novo)")
        self.produto_id_label.setStyleSheet("font-weight: bold; color: #34495e;")
        form_layout.addRow(self.produto_id_label)

        self.nome_produto_input = QLineEdit()
        self.nome_produto_input.setPlaceholderText("Nome ou Descrição do Produto")
        self.nome_produto_input.setStyleSheet(input_style)
        form_layout.addRow("Nome:", self.nome_produto_input)

        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("0.00")
        self.preco_input.setValidator(QDoubleValidator(0.0, 999999.99, 2)) # Validador para preço
        self.preco_input.setStyleSheet(input_style)
        form_layout.addRow("Preço de Venda:", self.preco_input)
        
        self.estoque_input = QLineEdit()
        self.estoque_input.setPlaceholderText("0")
        self.estoque_input.setValidator(QDoubleValidator(0.0, 999999.0, 0)) # Validador para inteiros
        self.estoque_input.setStyleSheet(input_style)
        form_layout.addRow("Estoque Inicial:", self.estoque_input)

        layout.addWidget(form_groupbox)
        layout.addStretch(1)

        # Botões de Ação
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addStretch(1)

        self.btn_cancel_produto = QPushButton("Cancelar")
        self.btn_cancel_produto.setFixedHeight(35)
        self.btn_cancel_produto.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.btn_cancel_produto.clicked.connect(self._cancel_produto_form)
        action_buttons_layout.addWidget(self.btn_cancel_produto)

        self.btn_save_produto = QPushButton("Salvar Produto")
        self.btn_save_produto.setFixedHeight(35)
        self.btn_save_produto.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_save_produto.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btn_save_produto.clicked.connect(self._save_produto)
        action_buttons_layout.addWidget(self.btn_save_produto)

        layout.addLayout(action_buttons_layout)

    def _load_sample_produtos_data(self):
        self.produtos_data = [
            {"codigo": "P001", "nome": "Caneta Esferográfica Azul", "preco": 2.50, "estoque": 150},
            {"codigo": "P002", "nome": "Caderno Universitário 10 Matérias", "preco": 18.90, "estoque": 80},
            {"codigo": "P003", "nome": "Apagador para Quadro Branco", "preco": 5.00, "estoque": 40},
        ]
        self._populate_produtos_table(self.produtos_data)

    def _populate_produtos_table(self, data):
        self.produtos_table.setRowCount(0)
        for row_idx, produto in enumerate(data):
            self.produtos_table.insertRow(row_idx)
            self.produtos_table.setItem(row_idx, 0, QTableWidgetItem(produto["codigo"]))
            self.produtos_table.setItem(row_idx, 1, QTableWidgetItem(produto["nome"]))
            self.produtos_table.setItem(row_idx, 2, QTableWidgetItem(f"R$ {produto['preco']:.2f}"))
            self.produtos_table.setItem(row_idx, 3, QTableWidgetItem(str(produto["estoque"])))
            
            for col in range(self.produtos_table.columnCount()):
                item = self.produtos_table.item(row_idx, col)
                if item:
                    item.setForeground(Qt.black)

    def _apply_produto_filters(self):
        search_text = self.search_produto_input.text().lower()
        
        filtered_data = []
        for produto in self.produtos_data:
            match_search = (search_text in produto["nome"].lower() or 
                            search_text in produto["codigo"].lower())
            
            if match_search:
                filtered_data.append(produto)
        
        self._populate_produtos_table(filtered_data)

    def _show_new_produto_form(self):
        self.new_produto_title_label.setText("Cadastrar Novo Produto")
        self.produto_id_label.setText("Código do Produto: (Novo)")
        self.nome_produto_input.clear()
        self.preco_input.clear()
        self.estoque_input.clear()
        self.produtos_stacked_widget.setCurrentIndex(1)
        self.nome_produto_input.setFocus()

    def _edit_produto(self, item):
        produto_codigo = self.produtos_table.item(item.row(), 0).text()
        self.current_editing_produto_codigo = produto_codigo
        
        selected_produto = next((p for p in self.produtos_data if p["codigo"] == produto_codigo), None)

        if selected_produto:
            self.new_produto_title_label.setText(f"Editar Produto: {selected_produto['nome']}")
            self.produto_id_label.setText(f"Código do Produto: {selected_produto['codigo']}")
            self.nome_produto_input.setText(selected_produto["nome"])
            self.preco_input.setText(str(selected_produto["preco"]))
            self.estoque_input.setText(str(selected_produto["estoque"]))
            self.produtos_stacked_widget.setCurrentIndex(1)
            self.nome_produto_input.setFocus()
        else:
            QMessageBox.warning(self, "Erro", "Produto não encontrado para edição.")

    def _save_produto(self):
        nome = self.nome_produto_input.text().strip()
        preco_text = self.preco_input.text().replace(',', '.') # Substitui vírgula por ponto para float
        estoque_text = self.estoque_input.text().strip()

        if not nome or not preco_text:
            QMessageBox.warning(self, "Erro ao Salvar", "Nome e Preço são campos obrigatórios.")
            return
        
        try:
            preco = float(preco_text)
            estoque = int(estoque_text) if estoque_text else 0
        except ValueError:
            QMessageBox.warning(self, "Erro de Formato", "Preço deve ser um número e Estoque um número inteiro.")
            return

        is_editing = hasattr(self, 'current_editing_produto_codigo') and self.current_editing_produto_codigo is not None
        
        if is_editing:
            for i, produto in enumerate(self.produtos_data):
                if produto["codigo"] == self.current_editing_produto_codigo:
                    self.produtos_data[i] = {
                        "codigo": self.current_editing_produto_codigo,
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }
                    QMessageBox.information(self, "Produto Salvo", f"Produto {nome} atualizado com sucesso!")
                    break
        else:
            new_produto_codigo = f"P{len(self.produtos_data) + 1:03d}"
            new_produto = {
                "codigo": new_produto_codigo,
                "nome": nome,
                "preco": preco,
                "estoque": estoque
            }
            self.produtos_data.append(new_produto)
            QMessageBox.information(self, "Produto Salvo", f"Produto {nome} cadastrado com sucesso!")
        
        self.current_editing_produto_codigo = None
        
        self._populate_produtos_table(self.produtos_data)
        self._cancel_produto_form()

    def _cancel_produto_form(self):
        reply = QMessageBox.question(self, "Confirmar Cancelamento", 
                                     "Tem certeza que deseja cancelar esta operação? Todas as alterações não salvas serão perdidas.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.current_editing_produto_codigo = None
            self.produtos_stacked_widget.setCurrentIndex(0)
            self.nome_produto_input.clear()
            self.preco_input.clear()
            self.estoque_input.clear()