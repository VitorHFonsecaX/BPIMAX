# App/Modulos/Ui_vendas.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QDateEdit,
    QStackedWidget, QGroupBox, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon

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
        # Este estilo afeta a maioria dos widgets de texto por padrão, a menos que sobreposto
        self.setStyleSheet("QLabel, QLineEdit, QComboBox, QTableWidget { color: black; }")
        
        # QStackedWidget para alternar entre a lista de vendas e o formulário de nova venda/detalhes
        self.sales_stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.sales_stacked_widget)

        # --- Página 1: Listagem de Vendas ---
        self.list_sales_page = QWidget()
        self.sales_stacked_widget.addWidget(self.list_sales_page)
        self._setup_list_sales_page()

        # --- Página 2: Formulário de Nova Venda/Detalhes ---
        self.new_sale_page = QWidget()
        self.sales_stacked_widget.addWidget(self.new_sale_page)
        self._setup_new_sale_page()

        self.sales_stacked_widget.setCurrentIndex(0)

    def _setup_list_sales_page(self):
        layout = QVBoxLayout(self.list_sales_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Título da seção (já tinha cor #2c3e50 que é um cinza escuro, quase preto)
        title_label = QLabel("Gestão de Vendas")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        # title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;") # Mantido ou pode ser ajustado
        layout.addWidget(title_label)

        # Barra de Ferramentas / Filtros
        toolbar_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar Venda (ID, Cliente...)")
        self.search_input.setFixedHeight(30)
        self.search_input.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;") # Adicionado color: black
        toolbar_layout.addWidget(self.search_input)
        
        self.filter_status_combo = QComboBox()
        self.filter_status_combo.addItems(["Todos", "Concluída", "Pendente", "Cancelada"])
        self.filter_status_combo.setFixedHeight(30)
        self.filter_status_combo.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;") # Adicionado color: black
        toolbar_layout.addWidget(self.filter_status_combo)

        self.filter_date_start = QDateEdit(QDate.currentDate().addYears(-1))
        self.filter_date_start.setCalendarPopup(True)
        self.filter_date_start.setFixedHeight(30)
        self.filter_date_start.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;") # Adicionado color: black
        toolbar_layout.addWidget(self.filter_date_start)

        self.filter_date_end = QDateEdit(QDate.currentDate())
        self.filter_date_end.setCalendarPopup(True)
        self.filter_date_end.setFixedHeight(30)
        self.filter_date_end.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;") # Adicionado color: black
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
             color: black; /* Garante texto das células preto */
            }
          QHeaderView::section {
             color: black; /* Garante texto do cabeçalho preto */
            }
            """)

        layout.addWidget(self.sales_table)

        self.btn_apply_filters.clicked.connect(self._apply_filters)
        self.search_input.textChanged.connect(self._apply_filters)
        self.filter_status_combo.currentIndexChanged.connect(self._apply_filters)
        self.filter_date_start.dateChanged.connect(self._apply_filters)
        self.filter_date_end.dateChanged.connect(self._apply_filters)

    def _setup_new_sale_page(self):
        layout = QVBoxLayout(self.new_sale_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.new_sale_title_label = QLabel("Nova Venda")
        self.new_sale_title_label.setFont(QFont("Arial", 18, QFont.Bold))
        # self.new_sale_title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;") # Já é um cinza escuro
        layout.addWidget(self.new_sale_title_label)

        # Formulário de Venda (Campos de Cliente, Data)
        customer_date_groupbox = QGroupBox("Informações da Venda")
        customer_date_groupbox.setStyleSheet("QGroupBox { color: black; }") # Se quiser garantir a cor do título do QGroupBox
        customer_date_layout = QVBoxLayout(customer_date_groupbox)

        customer_layout = QHBoxLayout()
        customer_layout.addWidget(QLabel("Cliente:"))
        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Nome do Cliente ou ID")
        self.customer_input.setFixedHeight(30)
        customer_input_style = "border: 1px solid #bdc3c7; border-radius: 5px; padding: 5px; color: black;"
        self.customer_input.setStyleSheet(customer_input_style)
        customer_layout.addWidget(self.customer_input)
        customer_date_layout.addLayout(customer_layout)

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Data da Venda:"))
        self.sale_date_edit = QDateEdit(QDate.currentDate())
        self.sale_date_edit.setCalendarPopup(True)
        self.sale_date_edit.setFixedHeight(30)
        self.sale_date_edit.setStyleSheet(customer_input_style) # Reusa o estilo
        date_layout.addWidget(self.sale_date_edit)
        customer_date_layout.addLayout(date_layout)

        layout.addWidget(customer_date_groupbox)

        # Tabela de Itens da Venda
        items_groupbox = QGroupBox("Itens da Venda")
        items_groupbox.setStyleSheet("QGroupBox { color: black; }") # Se quiser garantir a cor do título do QGroupBox
        items_layout = QVBoxLayout(items_groupbox)

        self.sale_items_table = QTableWidget()
        self.sale_items_table.setColumnCount(5)
        self.sale_items_table.setHorizontalHeaderLabels(["Produto", "Quantidade", "Preço Unit.", "Subtotal", "Ação"])
        self.sale_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sale_items_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sale_items_table.setStyleSheet("QTableWidget { color: black; }") # Garante texto da tabela de itens preto
        items_layout.addWidget(self.sale_items_table)
        self.sale_items_table.setStyleSheet("""
          QTableWidget {
             color: black; /* Garante texto das células preto */
            }
          QHeaderView::section {
             color: black; /* Garante texto do cabeçalho preto */
            }
            """)
        
        # Controles para adicionar item
        add_item_layout = QHBoxLayout()
        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Nome do Produto")
        self.product_input.setFixedHeight(30)
        self.product_input.setStyleSheet(customer_input_style) # Reusa o estilo
        add_item_layout.addWidget(self.product_input)

        self.quantity_input = QLineEdit("1")
        self.quantity_input.setPlaceholderText("Qtd")
        self.quantity_input.setFixedWidth(60)
        self.quantity_input.setFixedHeight(30)
        self.quantity_input.setStyleSheet(customer_input_style) # Reusa o estilo
        add_item_layout.addWidget(self.quantity_input)
        
        self.price_input = QLineEdit("0.00")
        self.price_input.setPlaceholderText("Preço")
        self.price_input.setFixedWidth(80)
        self.price_input.setFixedHeight(30)
        self.price_input.setStyleSheet(customer_input_style) # Reusa o estilo
        add_item_layout.addWidget(self.price_input)

        self.btn_add_item = QPushButton("Adicionar Item")
        self.btn_add_item.setFixedHeight(30)
        self.btn_add_item.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; border: none; border-radius: 5px; padding: 5px 10px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.btn_add_item.clicked.connect(self._add_item_to_sale)
        add_item_layout.addWidget(self.btn_add_item)

        items_layout.addLayout(add_item_layout)
        layout.addWidget(items_groupbox)

        # Seção de Total e Pagamento
        total_payment_layout = QHBoxLayout()
        total_payment_layout.addStretch(1)

        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("Total da Venda:"))
        self.total_value_label = QLabel("R$ 0.00")
        self.total_value_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_value_label.setStyleSheet("color: #e74c3c;") # Mantido o vermelho para o total
        total_layout.addWidget(self.total_value_label)
        total_payment_layout.addLayout(total_layout)

        total_payment_layout.addSpacing(30)

        payment_layout = QHBoxLayout()
        payment_layout.addWidget(QLabel("Forma de Pagamento:"))
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems(["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"])
        self.payment_method_combo.setFixedHeight(30)
        self.payment_method_combo.setStyleSheet(customer_input_style) # Reusa o estilo (também com color: black)
        payment_layout.addWidget(self.payment_method_combo)
        total_payment_layout.addLayout(payment_layout)

        layout.addLayout(total_payment_layout)

        # Botões de Ação (Salvar, Cancelar)
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addStretch(1)

        self.btn_cancel_sale = QPushButton("Cancelar")
        self.btn_cancel_sale.setFixedHeight(35)
        self.btn_cancel_sale.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.btn_cancel_sale.clicked.connect(self._cancel_sale_form)
        action_buttons_layout.addWidget(self.btn_cancel_sale)

        self.btn_save_sale = QPushButton("Salvar Venda")
        self.btn_save_sale.setFixedHeight(35)
        self.btn_save_sale.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_save_sale.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; color: white; border: none; border-radius: 5px; padding: 5px 15px;
            }
            QPushButton:hover { background-color: #27ae60; }
        """)
        self.btn_save_sale.clicked.connect(self._save_sale)
        action_buttons_layout.addWidget(self.btn_save_sale)

        layout.addLayout(action_buttons_layout)

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
            # Certifica que o texto dentro das células da tabela é preto
            for col in range(self.sales_table.columnCount()):
                item = self.sales_table.item(row_idx, col)
                if item:
                    item.setForeground(Qt.black) # Define a cor do texto do item para preto

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
        self.new_sale_title_label.setText("Nova Venda")
        self.customer_input.clear()
        self.sale_date_edit.setDate(QDate.currentDate())
        self.sale_items_table.setRowCount(0)
        self.current_sale_items = []
        self._update_total_value()
        self.product_input.clear()
        self.quantity_input.setText("1")
        self.price_input.setText("0.00")
        self.sales_stacked_widget.setCurrentIndex(1)

    def _edit_sale(self, item):
        sale_id = self.sales_table.item(item.row(), 0).text()
        selected_sale = next((s for s in self.sales_data if s["id"] == sale_id), None)

        if selected_sale:
            QMessageBox.information(self, "Editar Venda", f"Funcionalidade de edição para Venda ID: {sale_id} (simulado).")
        else:
            QMessageBox.warning(self, "Erro", "Venda não encontrada para edição.")


    def _add_item_to_sale(self):
        product_name = self.product_input.text().strip()
        quantity_str = self.quantity_input.text().strip()
        price_str = self.price_input.text().strip().replace(',', '.')

        if not product_name:
            QMessageBox.warning(self, "Erro de Item", "Nome do produto não pode ser vazio.")
            return
        
        try:
            quantity = int(quantity_str)
            price = float(price_str)
            if quantity <= 0 or price < 0:
                raise ValueError("Quantidade deve ser positiva e preço não negativo.")
        except ValueError:
            QMessageBox.warning(self, "Erro de Item", "Quantidade e Preço devem ser números válidos.")
            return

        subtotal = quantity * price
        
        self.current_sale_items.append({
            "product": product_name,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal
        })

        row_idx = self.sale_items_table.rowCount()
        self.sale_items_table.insertRow(row_idx)
        self.sale_items_table.setItem(row_idx, 0, QTableWidgetItem(product_name))
        self.sale_items_table.setItem(row_idx, 1, QTableWidgetItem(str(quantity)))
        self.sale_items_table.setItem(row_idx, 2, QTableWidgetItem(f"{price:.2f}"))
        self.sale_items_table.setItem(row_idx, 3, QTableWidgetItem(f"{subtotal:.2f}"))
        
        # Garante que as células da tabela de itens tenham texto preto
        for col in range(self.sale_items_table.columnCount() - 1): # Exclui a coluna do botão
            item = self.sale_items_table.item(row_idx, col)
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
        self.sale_items_table.setCellWidget(row_idx, 4, btn_remove)

        self.product_input.clear()
        self.quantity_input.setText("1")
        self.price_input.setText("0.00")
        self._update_total_value()
        self.product_input.setFocus()

    def _remove_item_from_sale(self, row_idx_to_remove):
        reply = QMessageBox.question(self, "Confirmar Remoção", "Tem certeza que deseja remover este item?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.current_sale_items[row_idx_to_remove]
            
            self.sale_items_table.setRowCount(0)
            for r_idx, item in enumerate(self.current_sale_items):
                self.sale_items_table.insertRow(r_idx)
                self.sale_items_table.setItem(r_idx, 0, QTableWidgetItem(item["product"]))
                self.sale_items_table.setItem(r_idx, 1, QTableWidgetItem(str(item["quantity"])))
                self.sale_items_table.setItem(r_idx, 2, QTableWidgetItem(f"{item['price']:.2f}"))
                self.sale_items_table.setItem(r_idx, 3, QTableWidgetItem(f"{item['subtotal']:.2f}"))

                # Garante que as células da tabela de itens tenham texto preto ao recarregar
                for col in range(self.sale_items_table.columnCount() - 1):
                    cell_item = self.sale_items_table.item(r_idx, col)
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
                self.sale_items_table.setCellWidget(new_r, 4, btn_remove)

            self._update_total_value()


    def _update_total_value(self):
        total = sum(item["subtotal"] for item in self.current_sale_items)
        self.total_value_label.setText(f"R$ {total:.2f}")

    def _save_sale(self):
        customer = self.customer_input.text().strip()
        sale_date = self.sale_date_edit.date().toString("yyyy-MM-dd")
        total_value = sum(item["subtotal"] for item in self.current_sale_items)
        payment_method = self.payment_method_combo.currentText()

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
            "status": "Concluída",
            "items": self.current_sale_items
        }
        self.sales_data.append(new_sale)
        
        QMessageBox.information(self, "Venda Salva", f"Venda {new_sale_id} salva com sucesso!\nTotal: R$ {total_value:.2f}")
        
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
            self.product_input.clear()
            self.quantity_input.setText("1")
            self.price_input.setText("0.00")