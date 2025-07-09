import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QListWidget
)
from PySide6.QtCore import Qt

class TelaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("songue")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("""
            background-color: #FFF176;
            color: black;
        """)

        layout = QVBoxLayout()

        titulo = QLabel("Bem-vindo ao Sons da terra")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")

        botao_entrar = QPushButton("Entrar")
        botao_entrar.setStyleSheet("""
            background-color: #2196F3; /* Azul */
            color: white;
            padding: 10px;
            font-size: 14px;
            border-radius: 8px;
        """)
        botao_entrar.clicked.connect(self.abrir_menu)

        layout.addWidget(titulo)
        layout.addWidget(botao_entrar)
        self.setLayout(layout)

    def abrir_menu(self):
        self.menu = TelaMenu()
        self.menu.show()
        self.close()

class TelaMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("requisitos funcionais")
        self.setGeometry(100, 100, 600, 600)

        self.setStyleSheet("""
            background-color: #FFF59D;
            color: black;
        """)

        layout = QVBoxLayout()

        label = QLabel("Menu")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")

        lista_menu = QListWidget()
        lista_menu.addItems([
            "avaliar",
            "o que as pessoas estão ouvindo",
            "shout-boxd",
            "novidades",
            "configurações",
            "sair"
        ])
        lista_menu.setStyleSheet("""
            background-color: #FFFDE7;
            border: none;
            padding: 5px;
        """)

        layout.addWidget(label)
        layout.addWidget(lista_menu)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaInicial()
    janela.show()
    sys.exit(app.exec())
