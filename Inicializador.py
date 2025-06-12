from PySide6.QtWidgets import QApplication
import sys
from App.janela_principal import JanelaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())
