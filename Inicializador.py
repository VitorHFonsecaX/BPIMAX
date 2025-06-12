import sys
from PySide6.QtWidgets import QApplication
from app.autenticacao.ui_login import TelaLogin  # você vai criar isso já

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaLogin()
    janela.show()
    sys.exit(app.exec())
