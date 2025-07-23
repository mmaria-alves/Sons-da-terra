from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class MenuPrincipal(QWidget):
    def __init__(self, usuario_logado):
        super().__init__()
        self.usuario = usuario_logado
        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        label_boasvindas = QLabel(f"Bem-vindo, {self.usuario['nome']}!!!")
        label_boasvindas.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_boasvindas)

        label_info = QLabel("tela do menu principal.")
        label_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_info)

        self.setLayout(layout)
