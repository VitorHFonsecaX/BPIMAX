import sys
# import os # Não é necessário para este arquivo

from PySide6.QtWidgets import QApplication
from App.Janela_principal import JanelaPrincipal # Assumindo que Janela_principal.py está dentro de App/

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())