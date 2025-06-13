# App/Inicializador.py

import sys
from PySide6.QtWidgets import QApplication
from App.Nucleo.Janela_principal import JanelaPrincipal # Caminho atualizado

if __name__ == "__main__":
    app = QApplication(sys.argv)

    janela_principal = JanelaPrincipal()
    janela_principal.show()

    sys.exit(app.exec())