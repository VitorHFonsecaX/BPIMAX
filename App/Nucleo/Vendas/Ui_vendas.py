# App/Nucleo/Vendas/Ui_vendas.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QDateEdit,
    QStackedWidget, QGroupBox, QMessageBox, QSpacerItem, QSizePolicy,
    QGridLayout # <--- Garante que QGridLayout está aqui e é importado corretamente de QtWidgets
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon, QDoubleValidator 

class Ui_Vendas(QWidget):
    def __init__(self):
        super().__init__()
        self.sales_data = []
        self.current_sale_items = []
        self.setupUi()
        self._load_sample_sales_data()

    def setupUi(self):
        # Layout principal da tela de Vendas
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Aplicar estilo geral para cor da fonte preta em QWidgets filhos
        self.setStyleSheet("QLabel, QLineEdit, QComboBox, QTableWidget { color: black; }")
        
        # QStackedWidget para alternar entre a lista de vendas e o formulário de nova venda/detalhes
        self.sales_stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.sales_stacked_widget)

        # --- Página 1: Listagem de Vendas ---
        self.list_sales_page = QWidget()
        self.sales_stacked_widget.addWidget(self.list_sales_page)
        self._setup_list_sales_page()

        # --- Página 2: Formulário de Nova Venda/Detalhes (PDV) ---
        self.new_sale_page = QWidget()
        self.sales_stacked_widget.addWidget(self.new_sale_page)
        self._setup_new_sale_page() 

        self.sales_stacked_widget.setCurrentIndex(0)

    def _setup_list_sales_page(self):
        layout = QVBoxLayout(self.list_sales_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        title_label = QLabel("Gestão de Vendas")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title_label)

        # Barra de Ferramentas / Filtros
        toolbar_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar Venda (ID, Cliente...)")
        self.search_input.setFixedHeight(30)
        self.search_input.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.search_input)
        
        self.filter_status_combo = QComboBox()
        self.filter_status_combo.addItems(["Todos", "Concluída", "Pendente", "Cancelada"])
        self.filter_status_combo.setFixedHeight(30)
        self.filter_status_combo.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.filter_status_combo)

        self.filter_date_start = QDateEdit(QDate.currentDate().addYears(-1))
        self.filter_date_start.setCalendarPopup(True)
        self.filter_date_start.setFixedHeight(30)
        self.filter_date_start.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.filter_date_start)

        self.filter_date_end = QDateEdit(QDate.currentDate())
        self.filter_date_end.setCalendarPopup(True)
        self.filter_date_end.setFixedHeight(30)
        self.filter_date_end.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        toolbar_layout.addWidget(self.filter_date_end)

        self.btn_apply_filters = QPushButton("Aplicar Filtros")
        self.btn_apply_filters.setFixedHeight(30)
        self.btn_apply_filters.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border: none; border-radius: 5px; padding: 5px 10px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        toolbar_layout.addWidget(self.btn_apply_filters)

        toolbar_layout.addStretch(1)

        self.btn_new_sale = QPushButton("Nova Venda")
        self.btn_new_sale.setFixedHeight(35)
        self.btn_new_sale.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_new_sale.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_new_sale.setIcon(QIcon("Recursos/icones/add.png"))
        self.btn_new_sale.clicked.connect(self._show_new_sale_form)
        toolbar_layout.addWidget(self.btn_new_sale)

        layout.addLayout(toolbar_layout)

        # Tabela de Vendas
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels(["ID Venda", "Data", "Cliente", "Total", "Status"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sales_table.itemDoubleClicked.connect(self._edit_sale)
        self.sales_table.setStyleSheet("""
            QTableWidget {
                color: black;
            }
            QHeaderView::section {
                color: black;
            }
        """)
        layout.addWidget(self.sales_table)

        self.btn_apply_filters.clicked.connect(self._apply_filters)
        self.search_input.textChanged.connect(self._apply_filters)
        self.filter_status_combo.currentIndexChanged.connect(self._apply_filters)
        self.filter_date_start.dateChanged.connect(self._apply_filters)
        self.filter_date_end.dateChanged.connect(self._apply_filters)

    def _setup_new_sale_page(self):
        # Layout principal da página de Nova Venda (PDV)
        main_pdv_layout = QHBoxLayout(self.new_sale_page)
        main_pdv_layout.setContentsMargins(0, 0, 0, 0)
        main_pdv_layout.setSpacing(15)

        # --- Coluna Esquerda: Entrada de Produtos e Tabela de Itens ---
        left_column_layout = QVBoxLayout()
        left_column_layout.setSpacing(10)

        self.new_sale_title_label = QLabel("PDV - Nova Venda")
        self.new_sale_title_label.setFont(QFont("Arial", 20, QFont.Bold))
        left_column_layout.addWidget(self.new_sale_title_label)
        
        # Grupo para entrada de produto
        product_input_group = QGroupBox("Adicionar Produto")
        product_input_group.setStyleSheet("QGroupBox { color: black; }")
        product_layout = QVBoxLayout(product_input_group)
        
        # Campo de entrada de produto (foco principal)
        product_quantity_layout = QHBoxLayout()
        self.product_input_pdv = QLineEdit()
        self.product_input_pdv.setPlaceholderText("Código ou Nome do Produto")
        self.product_input_pdv.setFixedHeight(40)
        self.product_input_pdv.setFont(QFont("Arial", 12))
        self.product_input_pdv.setStyleSheet("border: 2px solid #3498db; border-radius: 8px; padding: 5px; color: black;")
        product_quantity_layout.addWidget(self.product_input_pdv, 3) 

        self.quantity_input_pdv = QLineEdit("1")
        self.quantity_input_pdv.setPlaceholderText("Qtd")
        self.quantity_input_pdv.setFixedWidth(80)
        self.quantity_input_pdv.setFixedHeight(40)
        self.quantity_input_pdv.setFont(QFont("Arial", 12))
        self.quantity_input_pdv.setStyleSheet("border: 2px solid #bdc3c7; border-radius: 8px; padding: 5px; color: black;")
        self.quantity_input_pdv.setValidator(QDoubleValidator(0.01, 99999.99, 2))
        product_quantity_layout.addWidget(self.quantity_input_pdv, 1)

        product_layout.addLayout(product_quantity_layout)

        # Botão Adicionar Item (melhor posicionado para fluxo de PDV)
        self.btn_add_item_pdv = QPushButton("Adicionar")
        self.btn_add_item_pdv.setFixedHeight(45)
        self.btn_add_item_pdv.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_add_item_pdv.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; border: none; border-radius: 8px; padding: 10px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_add_item_pdv.clicked.connect(self._add_item_to_sale)
        product_layout.addWidget(self.btn_add_item_pdv)

        left_column_layout.addWidget(product_input_group)

        # Tabela de Itens da Venda (PDV) - principal área
        self.sale_items_table_pdv = QTableWidget()
        self.sale_items_table_pdv.setColumnCount(5)
        self.sale_items_table_pdv.setHorizontalHeaderLabels(["Produto", "Quantidade", "Preço Unit.", "Subtotal", "Ação"])
        self.sale_items_table_pdv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sale_items_table_pdv.setSelectionBehavior(QTableWidget.SelectRows)
        self.sale_items_table_pdv.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sale_items_table_pdv.setStyleSheet("""
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
        left_column_layout.addWidget(self.sale_items_table_pdv)

        main_pdv_layout.addLayout(left_column_layout, 2)

        # --- Coluna Direita: Total, Pagamento, Troco e Ações ---
        right_column_layout = QVBoxLayout()
        right_column_layout.setSpacing(10)

        # Informações da Venda (Cliente e Data - compacto)
        info_group = QGroupBox("Info. da Venda")
        info_group.setStyleSheet("QGroupBox { color: black; }")
        info_layout = QGridLayout(info_group)
        info_layout.setSpacing(5)

        info_layout.addWidget(QLabel("Cliente:"), 0, 0)
        self.customer_input_pdv = QLineEdit()
        self.customer_input_pdv.setPlaceholderText("Nome ou ID")
        self.customer_input_pdv.setFixedHeight(30)
        self.customer_input_pdv.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        info_layout.addWidget(self.customer_input_pdv, 0, 1)

        info_layout.addWidget(QLabel("Data:"), 1, 0)
        self.sale_date_edit_pdv = QDateEdit(QDate.currentDate())
        self.sale_date_edit_pdv.setCalendarPopup(True)
        self.sale_date_edit_pdv.setFixedHeight(30)
        self.sale_date_edit_pdv.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        info_layout.addWidget(self.sale_date_edit_pdv, 1, 1)
        
        right_column_layout.addWidget(info_group)

        # Seção de Total
        total_group = QGroupBox("Total da Venda")
        total_group.setStyleSheet("QGroupBox { color: black; }")
        total_layout = QVBoxLayout(total_group)
        self.total_value_label_pdv = QLabel("R$ 0.00")
        self.total_value_label_pdv.setFont(QFont("Arial", 28, QFont.Bold))
        self.total_value_label_pdv.setStyleSheet("color: #e74c3c;")
        self.total_value_label_pdv.setAlignment(Qt.AlignCenter)
        total_layout.addWidget(self.total_value_label_pdv)
        right_column_layout.addWidget(total_group)

        # Seção de Pagamento e Troco
        payment_group = QGroupBox("Pagamento")
        payment_group.setStyleSheet("QGroupBox { color: black; }")
        payment_layout = QVBoxLayout(payment_group)

        # Forma de Pagamento
        payment_method_layout = QHBoxLayout()
        payment_method_layout.addWidget(QLabel("Forma:"))
        self.payment_method_combo_pdv = QComboBox()
        self.payment_method_combo_pdv.addItems(["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"])
        self.payment_method_combo_pdv.setFixedHeight(30)
        self.payment_method_combo_pdv.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;")
        payment_method_layout.addWidget(self.payment_method_combo_pdv)
        payment_layout.addLayout(payment_method_layout)

        # Valor Recebido
        received_layout = QHBoxLayout()
        received_label = QLabel("Valor Recebido:")
        received_label.setFont(QFont("Arial", 12))
        received_layout.addWidget(received_label)
        self.received_input_pdv = QLineEdit("0.00")
        self.received_input_pdv.setPlaceholderText("Valor Pago Pelo Cliente")
        self.received_input_pdv.setFixedHeight(35)
        self.received_input_pdv.setFont(QFont("Arial", 14, QFont.Bold))
        self.received_input_pdv.setStyleSheet("border: 2px solid #2980b9; border-radius: 5px; padding: 5px; color: black;")
        self.received_input_pdv.setAlignment(Qt.AlignRight)
        self.received_input_pdv.setValidator(QDoubleValidator(0.00, 999999.99, 2))
        self.received_input_pdv.textChanged.connect(self._calculate_change)
        received_layout.addWidget(self.received_input_pdv)
        payment_layout.addLayout(received_layout)

        # Troco
        change_layout = QHBoxLayout()
        change_label = QLabel("Troco:")
        change_label.setFont(QFont("Arial", 12))
        change_layout.addWidget(change_label)
        self.change_value_label_pdv = QLabel("R$ 0.00")
        self.change_value_label_pdv.setFont(QFont("Arial", 18, QFont.Bold))
        self.change_value_label_pdv.setStyleSheet("color: #27ae60;")
        self.change_value_label_pdv.setAlignment(Qt.AlignRight)
        change_layout.addWidget(self.change_value_label_pdv)
        payment_layout.addLayout(change_layout)

        right_column_layout.addWidget(payment_group)

        # Botões de Ação (PDV)
        pdv_action_buttons_layout = QVBoxLayout()
        
        self.btn_finalize_sale = QPushButton("Finalizar Venda (F1)")
        self.btn_finalize_sale.setFixedHeight(50)
        self.btn_finalize_sale.setFont(QFont("Arial", 14, QFont.Bold))
        self.btn_finalize_sale.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; border: none; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_finalize_sale.clicked.connect(self._save_sale)
        pdv_action_buttons_layout.addWidget(self.btn_finalize_sale)

        self.btn_cancel_sale_pdv = QPushButton("Cancelar Venda (F12)")
        self.btn_cancel_sale_pdv.setFixedHeight(40)
        self.btn_cancel_sale_pdv.setFont(QFont("Arial", 11))
        self.btn_cancel_sale_pdv.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; border: none; border-radius: 10px; padding: 8px;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        self.btn_cancel_sale_pdv.clicked.connect(self._cancel_sale_form)
        pdv_action_buttons_layout.addWidget(self.btn_cancel_sale_pdv)
        
        pdv_action_buttons_layout.addStretch(1)

        right_column_layout.addLayout(pdv_action_buttons_layout)

        main_pdv_layout.addLayout(right_column_layout, 1)

    def _load_sample_sales_data(self):
        self.sales_data = [
            {"id": "001", "date": "2024-05-10", "customer": "João Silva", "total": 150.50, "status": "Concluída"},
            {"id": "002", "date": "2024-05-12", "customer": "Maria Souza", "total": 230.00, "status": "Pendente"},
            {"id": "003", "date": "2024-05-15", "customer": "Pedro Santos", "total": 50.00, "status": "Concluída"},
            {"id": "004", "date": "2024-05-16", "customer": "Ana Oliveira", "total": 450.75, "status": "Concluída"},
            {"id": "005", "date": "2024-05-18", "customer": "Carlos Costa", "total": 80.20, "status": "Cancelada"},
        ]
        self._populate_sales_table(self.sales_data)

    def _populate_sales_table(self, data):
        self.sales_table.setRowCount(0)
        for row_idx, sale in enumerate(data):
            self.sales_table.insertRow(row_idx)
            self.sales_table.setItem(row_idx, 0, QTableWidgetItem(sale["id"]))
            self.sales_table.setItem(row_idx, 1, QTableWidgetItem(sale["date"]))
            self.sales_table.setItem(row_idx, 2, QTableWidgetItem(sale["customer"]))
            self.sales_table.setItem(row_idx, 3, QTableWidgetItem(f"R$ {sale['total']:.2f}"))
            self.sales_table.setItem(row_idx, 4, QTableWidgetItem(sale["status"]))
            for col in range(self.sales_table.columnCount()):
                item = self.sales_table.item(row_idx, col)
                if item:
                    item.setForeground(Qt.black)

    def _apply_filters(self):
        search_text = self.search_input.text().lower()
        status_filter = self.filter_status_combo.currentText()
        start_date = self.filter_date_start.date()
        end_date = self.filter_date_end.date()

        filtered_data = []
        for sale in self.sales_data:
            match_search = search_text in sale["id"].lower() or search_text in sale["customer"].lower()
            match_status = (status_filter == "Todos" or sale["status"] == status_filter)

            sale_date = QDate.fromString(sale["date"], "yyyy-MM-dd")
            match_date = (sale_date >= start_date and sale_date <= end_date)

            if match_search and match_status and match_date:
                filtered_data.append(sale)
        
        self._populate_sales_table(filtered_data)

    def _show_new_sale_form(self):
        self.new_sale_title_label.setText("PDV - Nova Venda")
        self.customer_input_pdv.clear()
        self.sale_date_edit_pdv.setDate(QDate.currentDate())
        self.sale_items_table_pdv.setRowCount(0)
        self.current_sale_items = []
        self._update_total_value()
        self.product_input_pdv.clear()
        self.quantity_input_pdv.setText("1")
        self.received_input_pdv.setText("0.00")
        self.change_value_label_pdv.setText("R$ 0.00")
        self.sales_stacked_widget.setCurrentIndex(1)
        self.product_input_pdv.setFocus()

    def _edit_sale(self, item):
        sale_id = self.sales_table.item(item.row(), 0).text()
        selected_sale = next((s for s in self.sales_data if s["id"] == sale_id), None)

        if selected_sale:
            QMessageBox.information(self, "Editar Venda", f"Funcionalidade de edição para Venda ID: {sale_id} (simulado).")
        else:
            QMessageBox.warning(self, "Erro", "Venda não encontrada para edição.")

    def _add_item_to_sale(self):
        product_name = self.product_input_pdv.text().strip()
        quantity_str = self.quantity_input_pdv.text().strip()
        
        simulated_price = 10.00 

        if not product_name:
            QMessageBox.warning(self, "Erro de Item", "Nome do produto não pode ser vazio.")
            return
        
        try:
            quantity = float(quantity_str)
            price_for_item = simulated_price

            if quantity <= 0:
                raise ValueError("Quantidade deve ser positiva.")
        except ValueError:
            QMessageBox.warning(self, "Erro de Item", "Quantidade deve ser um número válido.")
            return

        subtotal = quantity * price_for_item
        
        self.current_sale_items.append({
            "product": product_name,
            "quantity": quantity,
            "price": price_for_item,
            "subtotal": subtotal
        })

        row_idx = self.sale_items_table_pdv.rowCount()
        self.sale_items_table_pdv.insertRow(row_idx)
        self.sale_items_table_pdv.setItem(row_idx, 0, QTableWidgetItem(product_name))
        self.sale_items_table_pdv.setItem(row_idx, 1, QTableWidgetItem(str(quantity)))
        self.sale_items_table_pdv.setItem(row_idx, 2, QTableWidgetItem(f"{price_for_item:.2f}"))
        self.sale_items_table_pdv.setItem(row_idx, 3, QTableWidgetItem(f"{subtotal:.2f}"))
        
        for col in range(self.sale_items_table_pdv.columnCount() - 1):
            item = self.sale_items_table_pdv.item(row_idx, col)
            if item:
                item.setForeground(Qt.black)

        btn_remove = QPushButton("Remover")
        btn_remove.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; border: none; border-radius: 3px; padding: 3px 5px; font-size: 10px;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        btn_remove.clicked.connect(lambda checked, r=row_idx: self._remove_item_from_sale(r))
        self.sale_items_table_pdv.setCellWidget(row_idx, 4, btn_remove)

        self.product_input_pdv.clear()
        self.quantity_input_pdv.setText("1")
        self._update_total_value()
        self._calculate_change()
        self.product_input_pdv.setFocus()

    def _remove_item_from_sale(self, row_idx_to_remove):
        reply = QMessageBox.question(self, "Confirmar Remoção", "Tem certeza que deseja remover este item?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.current_sale_items[row_idx_to_remove]
            
            self.sale_items_table_pdv.setRowCount(0)
            for r_idx, item in enumerate(self.current_sale_items):
                self.sale_items_table_pdv.insertRow(r_idx)
                self.sale_items_table_pdv.setItem(r_idx, 0, QTableWidgetItem(item["product"]))
                self.sale_items_table_pdv.setItem(r_idx, 1, QTableWidgetItem(str(item["quantity"])))
                self.sale_items_table_pdv.setItem(r_idx, 2, QTableWidgetItem(f"{item['price']:.2f}"))
                self.sale_items_table_pdv.setItem(r_idx, 3, QTableWidgetItem(f"{item['subtotal']:.2f}"))

                for col in range(self.sale_items_table_pdv.columnCount() - 1):
                    cell_item = self.sale_items_table_pdv.item(r_idx, col)
                    if cell_item:
                        cell_item.setForeground(Qt.black)

                btn_remove = QPushButton("Remover")
                btn_remove.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c; color: white; border: none; border-radius: 3px; padding: 3px 5px; font-size: 10px;
                    }
                    QPushButton:hover { background-color: #c0392b; }
                """)
                btn_remove.clicked.connect(lambda checked, new_r=r_idx: self._remove_item_from_sale(new_r))
                self.sale_items_table_pdv.setCellWidget(new_r, 4, btn_remove)

            self._update_total_value()
            self._calculate_change()

    def _update_total_value(self):
        total = sum(item["subtotal"] for item in self.current_sale_items)
        self.total_value_label_pdv.setText(f"R$ {total:.2f}")

    def _calculate_change(self):
        try:
            total = sum(item["subtotal"] for item in self.current_sale_items)
            received_str = self.received_input_pdv.text().replace(',', '.')
            received_amount = float(received_str)
            
            change = received_amount - total
            self.change_value_label_pdv.setText(f"R$ {change:.2f}")
            if change < 0:
                self.change_value_label_pdv.setStyleSheet("color: #e74c3c;")
            else:
                self.change_value_label_pdv.setStyleSheet("color: #27ae60;")
        except ValueError:
            self.change_value_label_pdv.setText("R$ 0.00")
            self.change_value_label_pdv.setStyleSheet("color: #27ae60;")

    def _save_sale(self):
        customer = self.customer_input_pdv.text().strip()
        sale_date = self.sale_date_edit_pdv.date().toString("yyyy-MM-dd")
        total_value = sum(item["subtotal"] for item in self.current_sale_items)
        payment_method = self.payment_method_combo_pdv.currentText()
        received_amount = float(self.received_input_pdv.text().replace(',', '.'))
        
        if total_value > received_amount:
            QMessageBox.warning(self, "Erro ao Finalizar", "Valor recebido é menor que o total da venda. Verifique o pagamento.")
            return

        if not customer:
            QMessageBox.warning(self, "Erro ao Salvar", "O nome do cliente não pode ser vazio.")
            return
        if not self.current_sale_items:
            QMessageBox.warning(self, "Erro ao Salvar", "A venda deve ter pelo menos um item.")
            return

        new_sale_id = f"V{len(self.sales_data) + 1:03d}"
        new_sale = {
            "id": new_sale_id,
            "date": sale_date,
            "customer": customer,
            "total": total_value,
            "payment_method": payment_method,
            "received_amount": received_amount,
            "change": received_amount - total_value,
            "status": "Concluída",
            "items": self.current_sale_items
        }
        self.sales_data.append(new_sale)
        
        QMessageBox.information(self, "Venda Salva", f"Venda {new_sale_id} salva com sucesso!\nTotal: R$ {total_value:.2f}\nTroco: R$ {new_sale['change']:.2f}")
        
        self._populate_sales_table(self.sales_data)
        self._cancel_sale_form()

    def _cancel_sale_form(self):
        reply = QMessageBox.question(self, "Confirmar Cancelamento", 
                                     "Tem certeza que deseja cancelar esta operação? Todas as alterações serão perdidas.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sales_stacked_widget.setCurrentIndex(0)
            self.current_sale_items = []
            self._update_total_value()
            self.product_input_pdv.clear()
            self.quantity_input_pdv.setText("1")
            self.customer_input_pdv.clear()
            self.sale_date_edit_pdv.setDate(QDate.currentDate())
            self.sale_items_table_pdv.setRowCount(0)
            self.received_input_pdv.setText("0.00")
            self.change_value_label_pdv.setText("R$ 0.00")