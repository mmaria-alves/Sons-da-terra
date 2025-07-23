import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtCore import Qt, QTimer
from autenticadores import Autenticadores

class TelaLogin(QWidget):
    def __init__(self, autenticadores):
        super().__init__()
        self.autenticador = autenticadores
        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 200, 500, 500)
        
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        self.texto1 = "SONS DA TERRA SONS DA TERRA "
        self.posicao1 = 0
        self.texto2 = "SONS DA TERRA SONS DA TERRA "
        self.posicao2 = 0

        self.init_ui()
        
        self.setStyleSheet('background-color: #fcd967')
    
    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)

        else:
            return QFont("Arial", 20)

    def animar_textos(self):
        # Letreiro 1 - anda pra direita
        self.posicao1 = (self.posicao1 + 1) % len(self.texto1)
        texto_1_animado = self.texto1[self.posicao1:] + self.texto1[:self.posicao1]
        self.label_animada1.setText(texto_1_animado)

        # Letreiro 2 - anda pra esquerda
        self.posicao2 = (self.posicao2 - 1) % len(self.texto2)
        texto_2_animado = self.texto2[self.posicao2:] + self.texto2[:self.posicao2]
        self.label_animada2.setText(texto_2_animado)
    
    # inicializa a interface  
    def init_ui(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)

        botao_login = QPushButton("Entrar")
        botao_login.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_login.clicked.connect(self.fazer_login)

        botao_cadastro = QPushButton("Não possui uma conta? Cadastre-se agora!")
        botao_cadastro.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_cadastro.clicked.connect(self.abrir_cadastro)

        label = QLabel("Bem-vindo!")
        label.setFont(self.fonte_titulo)
        label.setStyleSheet("color: #fffffd; font-size: 70px; font-weight: bold;")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.label_animada1 = QLabel(self.texto1)
        self.label_animada1.setFont(self.fonte_titulo)
        self.label_animada1.setStyleSheet('''
                                          background-color: #fffffd;
                                          color: #fbcf41;
                                          border-radius: 25px;
                                          font-size: 25px; 
                                          ''')
        self.label_animada1.setAlignment(Qt.AlignCenter)
        
        self.label_animada2 = QLabel(self.texto2)
        self.label_animada2.setFont(self.fonte_titulo)
        self.label_animada2.setStyleSheet('''
                                          background-color: #fffffd;
                                          color: #fbcf41;
                                          border-radius: 25px;
                                          font-size: 25px; 
                                          ''')
        self.label_animada2.setAlignment(Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animar_textos)
        self.timer.start(750)

        # MUDAR AS FONTES, E O JEITO QUE FICA NA TELA
        label_login = QLabel('Login: ')
        label_login.setFont(self.fonte_subtitulo)
        label_login.setStyleSheet("color: #fffffd; font-size: 40px")
        label_login.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        layout.addWidget(label)
        layout.addWidget(self.label_animada1)
        layout.addWidget(self.label_animada2)
        layout.addWidget(label_login)
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(botao_login)
        layout.addWidget(botao_cadastro)

        self.setLayout(layout)

    def fazer_login(self):
        email = self.email_input.text()
        senha = self.senha_input.text()
        
        sucesso, usuario = self.autenticador.login(email, senha)
        if sucesso:
            QMessageBox.information(self, "Login", f"Bem-vindo, {usuario.nome}!")
            self.abrir_menu_principal(usuario)
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha inválidos.")

    def abrir_cadastro(self):
        self.hide()
        self.cadastro = TelaCadastro(self.autenticador)
        self.cadastro.show()


class TelaCadastro(QWidget):
    def __init__(self, autenticador):
        super().__init__()
        self.autenticador = autenticador
        self.setWindowTitle("Cadastro")
        self.setGeometry(100, 100, 300, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha (6 dígitos)")
        self.senha_input.setEchoMode(QLineEdit.Password)

        self.confirmar_senha_input = QLineEdit()
        self.confirmar_senha_input.setPlaceholderText("Confirmar senha")
        self.confirmar_senha_input.setEchoMode(QLineEdit.Password)

        botao_cadastrar = QPushButton("Cadastrar")
        botao_cadastrar.clicked.connect(self.realizar_cadastro)

        botao_voltar = QPushButton("Voltar")
        botao_voltar.clicked.connect(self.voltar)

        layout.addWidget(QLabel("Cadastro de Usuário"))
        layout.addWidget(self.nome_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(self.confirmar_senha_input)
        layout.addWidget(botao_cadastrar)
        layout.addWidget(botao_voltar)

        self.setLayout(layout)

    def realizar_cadastro(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        senha = self.senha_input.text()
        confirmar = self.confirmar_senha_input.text()

        sucesso, mensagem = self.autenticador.cadastrar_usuario(nome, email, senha, confirmar)
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.voltar()
        else:
            QMessageBox.warning(self, "Erro", mensagem)

    def voltar(self):
        self.hide()
        self.login = TelaLogin(self.autenticador)
        self.login.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    autenticador = Autenticadores()
    janela_login = TelaLogin(autenticador)
    janela_login.show()
    sys.exit(app.exec())