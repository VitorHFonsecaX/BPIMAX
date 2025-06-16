# App/Nucleo/Clientes/Ui_clientes.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget, QGroupBox,
    QMessageBox, QSpacerItem, QSizePolicy, QFormLayout # Adicionado QFormLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon, QDoubleValidator # <--- CORRIGIDO AQUI: QDoubleValidator de QtGui

class Ui_Clientes(QWidget):
    def __init__(self):
        super().__init__()
        self.clientes_data = [] # Lista para armazenar os dados dos clientes
        self.setupUi()
        self._load_sample_clientes_data() # Carrega alguns dados de exemplo

    def setupUi(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        self.setStyleSheet("QLabel, QLineEdit, QComboBox, QTableWidget { color: black; }")

        self.clientes_stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.clientes_stacked_widget)

        # --- Página 1: Listagem de Clientes ---
        self.list_clientes_page = QWidget()
        self.clientes_stacked_widget.addWidget(self.list_clientes_page)
        self._setup_list_clientes_page()

        # --- Página 2: Formulário de Cadastro/Edição de Cliente ---
        self.new_cliente_page = QWidget()
        self.clientes_stacked_widget.addWidget(self.new_cliente_page)
        self._setup_new_cliente_page()

        self.clientes_stacked_widget.setCurrentIndex(0) # Inicia na página de listagem

    def _setup_list_clientes_page(self):
        layout = QVBoxLayout(self.list_clientes_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        title_label = QLabel("Gestão de Clientes")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title_label)

        # Barra de Ferramentas / Filtros
        toolbar_layout = QHBoxLayout()
        
        self.search_cliente_input = QLineEdit()
        self.search_cliente_input.setPlaceholderText("Buscar Cliente (Nome, CPF/CNPJ...)")
        self.search_cliente_input.setFixedHeight(30)
        self.search_cliente_input.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.search_cliente_input)
        
        toolbar_layout.addStretch(1)

        self.btn_new_cliente = QPushButton("Novo Cliente")
        self.btn_new_cliente.setFixedHeight(35)
        self.btn_new_cliente.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_new_cliente.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_new_cliente.setIcon(QIcon("Recursos/icones/add.png"))
        self.btn_new_cliente.clicked.connect(self._show_new_cliente_form)
        toolbar_layout.addWidget(self.btn_new_cliente)

        layout.addLayout(toolbar_layout)

        # Tabela de Clientes
        self.clientes_table = QTableWidget()
        self.clientes_table.setColumnCount(6) # ID, Nome, CPF/CNPJ, Telefone, Email, Endereço
        self.clientes_table.setHorizontalHeaderLabels(["ID Cliente", "Nome", "CPF/CNPJ", "Telefone", "Email", "Endereço"])
        self.clientes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clientes_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.clientes_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.clientes_table.itemDoubleClicked.connect(self._edit_cliente)
        self.clientes_table.setStyleSheet("""
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
        layout.addWidget(self.clientes_table)

        self.search_cliente_input.textChanged.connect(self._apply_cliente_filters)

    def _setup_new_cliente_page(self):
        layout = QVBoxLayout(self.new_cliente_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.new_cliente_title_label = QLabel("Cadastrar Novo Cliente")
        self.new_cliente_title_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(self.new_cliente_title_label)

        # Formulário de Cliente
        form_groupbox = QGroupBox("Dados do Cliente")
        form_groupbox.setStyleSheet("QGroupBox { color: black; }")
        form_layout = QFormLayout(form_groupbox)
        form_layout.setContentsMargins(10, 20, 10, 10) # Margens internas do formulário
        form_layout.setSpacing(10) # Espaçamento entre os widgets

        # Estilo para os QLineEdits do formulário
        input_style = "border: 1px solid #bdc3c7; border-radius: 5px; padding: 8px; color: black;"

        self.cliente_id_label = QLabel("ID do Cliente: (Novo)")
        self.cliente_id_label.setStyleSheet("font-weight: bold; color: #34495e;")
        form_layout.addRow(self.cliente_id_label)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome Completo ou Razão Social")
        self.nome_input.setStyleSheet(input_style)
        form_layout.addRow("Nome:", self.nome_input)

        self.cpf_cnpj_input = QLineEdit()
        self.cpf_cnpj_input.setPlaceholderText("CPF ou CNPJ")
        self.cpf_cnpj_input.setStyleSheet(input_style)
        form_layout.addRow("CPF/CNPJ:", self.cpf_cnpj_input)
        
        self.endereco_input = QLineEdit()
        self.endereco_input.setPlaceholderText("Rua, Número, Bairro, Cidade, Estado")
        self.endereco_input.setStyleSheet(input_style)
        form_layout.addRow("Endereço:", self.endereco_input)

        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("(XX) XXXX-XXXX ou (XX) 9XXXX-XXXX")
        self.telefone_input.setStyleSheet(input_style)
        form_layout.addRow("Telefone:", self.telefone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemplo@email.com")
        self.email_input.setStyleSheet(input_style)
        form_layout.addRow("Email:", self.email_input)

        layout.addWidget(form_groupbox)
        layout.addStretch(1) # Empurra os botões para baixo

        # Botões de Ação
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addStretch(1)

        self.btn_cancel_cliente = QPushButton("Cancelar")
        self.btn_cancel_cliente.setFixedHeight(35)
        self.btn_cancel_cliente.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.btn_cancel_cliente.clicked.connect(self._cancel_cliente_form)
        action_buttons_layout.addWidget(self.btn_cancel_cliente)

        self.btn_save_cliente = QPushButton("Salvar Cliente")
        self.btn_save_cliente.setFixedHeight(35)
        self.btn_save_cliente.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_save_cliente.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btn_save_cliente.clicked.connect(self._save_cliente)
        action_buttons_layout.addWidget(self.btn_save_cliente)

        layout.addLayout(action_buttons_layout)

    def _load_sample_clientes_data(self):
        self.clientes_data = [
            {"id": "C001", "nome": "Empresa Alpha Ltda", "cpf_cnpj": "12.345.678/0001-90", "telefone": "(31) 3212-3456", "email": "contato@alpha.com", "endereco": "Rua A, 100, Centro, Contagem - MG"},
            {"id": "C002", "nome": "Maria Joana", "cpf_cnpj": "123.456.789-01", "telefone": "(31) 98765-4321", "email": "maria@email.com", "endereco": "Av. Brasil, 500, Bairro X, Belo Horizonte - MG"},
            {"id": "C003", "nome": "João Carlos", "cpf_cnpj": "987.654.321-02", "telefone": "(11) 99876-5432", "email": "joao@email.com", "endereco": "Rua Z, 30, Vila Y, São Paulo - SP"},
        ]
        self._populate_clientes_table(self.clientes_data)

    def _populate_clientes_table(self, data):
        self.clientes_table.setRowCount(0)
        for row_idx, cliente in enumerate(data):
            self.clientes_table.insertRow(row_idx)
            self.clientes_table.setItem(row_idx, 0, QTableWidgetItem(cliente["id"]))
            self.clientes_table.setItem(row_idx, 1, QTableWidgetItem(cliente["nome"]))
            self.clientes_table.setItem(row_idx, 2, QTableWidgetItem(cliente["cpf_cnpj"]))
            self.clientes_table.setItem(row_idx, 3, QTableWidgetItem(cliente["telefone"]))
            self.clientes_table.setItem(row_idx, 4, QTableWidgetItem(cliente["email"]))
            self.clientes_table.setItem(row_idx, 5, QTableWidgetItem(cliente["endereco"]))
            
            for col in range(self.clientes_table.columnCount()):
                item = self.clientes_table.item(row_idx, col)
                if item:
                    item.setForeground(Qt.black)

    def _apply_cliente_filters(self):
        search_text = self.search_cliente_input.text().lower()
        
        filtered_data = []
        for cliente in self.clientes_data:
            match_search = (search_text in cliente["nome"].lower() or 
                            search_text in cliente["cpf_cnpj"].lower() or
                            search_text in cliente["telefone"].lower() or
                            search_text in cliente["email"].lower())
            
            if match_search:
                filtered_data.append(cliente)
        
        self._populate_clientes_table(filtered_data)

    def _show_new_cliente_form(self):
        self.new_cliente_title_label.setText("Cadastrar Novo Cliente")
        self.cliente_id_label.setText("ID do Cliente: (Novo)")
        self.nome_input.clear()
        self.cpf_cnpj_input.clear()
        self.endereco_input.clear()
        self.telefone_input.clear()
        self.email_input.clear()
        self.clientes_stacked_widget.setCurrentIndex(1)
        self.nome_input.setFocus()

    def _edit_cliente(self, item):
        cliente_id = self.clientes_table.item(item.row(), 0).text()
        self.current_editing_cliente_id = cliente_id
        
        selected_cliente = next((c for c in self.clientes_data if c["id"] == cliente_id), None)

        if selected_cliente:
            self.new_cliente_title_label.setText(f"Editar Cliente: {selected_cliente['nome']}")
            self.cliente_id_label.setText(f"ID do Cliente: {selected_cliente['id']}")
            self.nome_input.setText(selected_cliente["nome"])
            self.cpf_cnpj_input.setText(selected_cliente["cpf_cnpj"])
            self.endereco_input.setText(selected_cliente["endereco"])
            self.telefone_input.setText(selected_cliente["telefone"])
            self.email_input.setText(selected_cliente["email"])
            self.clientes_stacked_widget.setCurrentIndex(1)
            self.nome_input.setFocus()
        else:
            QMessageBox.warning(self, "Erro", "Cliente não encontrado para edição.")

    def _save_cliente(self):
        nome = self.nome_input.text().strip()
        cpf_cnpj = self.cpf_cnpj_input.text().strip()
        endereco = self.endereco_input.text().strip()
        telefone = self.telefone_input.text().strip()
        email = self.email_input.text().strip()

        if not nome or not cpf_cnpj:
            QMessageBox.warning(self, "Erro ao Salvar", "Nome e CPF/CNPJ são campos obrigatórios.")
            return

        is_editing = hasattr(self, 'current_editing_cliente_id') and self.current_editing_cliente_id is not None
        
        if is_editing:
            for i, cliente in enumerate(self.clientes_data):
                if cliente["id"] == self.current_editing_cliente_id:
                    self.clientes_data[i] = {
                        "id": self.current_editing_cliente_id,
                        "nome": nome,
                        "cpf_cnpj": cpf_cnpj,
                        "endereco": endereco,
                        "telefone": telefone,
                        "email": email
                    }
                    QMessageBox.information(self, "Cliente Salvo", f"Cliente {nome} atualizado com sucesso!")
                    break
        else:
            new_cliente_id = f"C{len(self.clientes_data) + 1:03d}"
            new_cliente = {
                "id": new_cliente_id,
                "nome": nome,
                "cpf_cnpj": cpf_cnpj,
                "endereco": endereco,
                "telefone": telefone,
                "email": email
            }
            self.clientes_data.append(new_cliente)
            QMessageBox.information(self, "Cliente Salvo", f"Cliente {nome} cadastrado com sucesso!")
        
        self.current_editing_cliente_id = None 
        
        self._populate_clientes_table(self.clientes_data)
        self._cancel_cliente_form()

    def _cancel_cliente_form(self):
        reply = QMessageBox.question(self, "Confirmar Cancelamento", 
                                     "Tem certeza que deseja cancelar esta operação? Todas as alterações não salvas serão perdidas.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.current_editing_cliente_id = None
            self.clientes_stacked_widget.setCurrentIndex(0)
            self.nome_input.clear()
            self.cpf_cnpj_input.clear()
            self.endereco_input.clear()
            self.telefone_input.clear()
            self.email_input.clear()