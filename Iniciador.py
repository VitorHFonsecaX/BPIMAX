# main.py (ou Inicializador.py na raiz do projeto)

from PySide6.QtWidgets import QApplication
from App.Nucleo.Ui_login import Ui_Login
from App.Nucleo.Janela_principal import JanelaPrincipal
import sys

class ApplicationInitializer:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = Ui_Login()
        self.main_window = JanelaPrincipal()

        # Conecta o sinal de sucesso do login para mostrar a janela principal
        self.login_window.login_successful.connect(self.show_main_window)

    def show_main_window(self):
        # Esconde a janela de login e mostra a principal
        self.login_window.hide()
        self.main_window.show()

    def run(self):
        # Inicia mostrando a janela de login
        self.login_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    # Certifique-se de que a estrutura de pastas está correta antes de executar
    # Para testar os ícones, certifique-se de ter a pasta 'Recursos/icones'
    # com os arquivos .png correspondentes (produtos.png, estoque.png, etc.)
    initializer = ApplicationInitializer()
    initializer.run()