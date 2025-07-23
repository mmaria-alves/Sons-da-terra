import sys
import json
import os
import random
from Main import *
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase, QFont, QIcon

ARQUIVO_USUARIOS = "dados/usuarios.json"
ARQUIVO_AVALIACOES = "dados/avaliacoes.json"
ARQUIVO_SHOUTBOX = "dados/shoutbox.json"
ARQUIVO_ALBUNS = "dados/albuns.json"


novidades = [
    {"nome": "Movimento algum (NOVO)", "artista": "Fernando Motta"},
    {"nome": "Imagina (single)", "artista": "Barbarize feat. Oreia"},
    {"nome": "Tropical do Brasil (single)", "artista": "Uana feat. Leoa"},
    {"nome": "Casa Coração (2025)", "artista": "Joyce Alane"},
    {"nome": "Coisas naturais (2025)", "artista": "Marina Sena"},
    {"nome": "Gambiarra chic pt.2 (2025)", "artista": "Irmãs de Pau"},
    {"nome": "Dvd (single)", "artista": "Mirela Hazin"},
    {"nome": "KM2 (2025)", "artista": "Ebony"}
]

def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_json(caminho, dados):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

class MenuPrincipal(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"Sons da Terra")
        self.setGeometry(200, 200, 500, 500)
        self.setWindowIcon(QIcon("imagens/Logo.png"))
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        self.setStyleSheet("background-color: #fcd967") 

        layout = QVBoxLayout()

        btn_avaliar = QPushButton("Avaliar álbum")
        btn_ouvindo = QPushButton("O que as pessoas estão ouvindo?")
        btn_shout = QPushButton("Shout-boxd")
        btn_novidades = QPushButton("Novidades")
        btn_sair = QPushButton("Sair")

        for btn in [btn_avaliar, btn_ouvindo, btn_shout, btn_novidades, btn_sair]:
            btn.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold;")
            
        btn_avaliar.clicked.connect(self.avaliar_album)
        btn_ouvindo.clicked.connect(self.ver_ouvindo)
        btn_shout.clicked.connect(self.adicionar_shout)
        btn_novidades.clicked.connect(self.ver_novidades)
        btn_sair.clicked.connect(self.fechar)

        layout.addWidget(btn_avaliar)
        layout.addWidget(btn_ouvindo)
        layout.addWidget(btn_shout)
        layout.addWidget(btn_novidades)
        layout.addWidget(btn_sair)

        self.setLayout(layout)

    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)
        else:
            return QFont("Arial", 20)

    def avaliar_album(self):
        avaliacoes = carregar_json(ARQUIVO_AVALIACOES)
        email = self.usuario.get('email')

        lista = "\n".join(f"{i+1}. {alb['nome']} - {alb['artista']}" for i, alb in enumerate(albuns_disponiveis))

        numero, ok = QInputDialog.getText(self, "Avaliação", f"Escolha o número do álbum para avaliar:\n\n{lista}")
        if not ok or not numero.isdigit() or not (1 <= int(numero) <= len(albuns_disponiveis)):
            return

        nota, ok = QInputDialog.getText(self, "Nota", "Dê uma nota de 0 a 5:")
        if not ok:
            return
        try:
            nota_float = float(nota)
            if nota_float < 0 or nota_float > 5:
                QMessageBox.warning(self, "Erro", "nota deve ser entre 0 e 5.")
                return
        except ValueError:
            QMessageBox.warning(self, "Erro", "Nota inválida.")
            return

        comentario, ok = QInputDialog.getText(self, "Comentário", "Deixe um comentário (máx 300 caracteres):")
        if not ok:
            return
        if len(comentario) > 300:
            QMessageBox.warning(self, "Erro", "Comentário muito longo.")
            return

        album = albuns_disponiveis[int(numero) - 1]
        avaliacoes[email] = {
            "album": album["nome"],
            "artista": album["artista"],
            "nota": nota_float,
            "comentario": comentario
        }
        salvar_json(ARQUIVO_AVALIACOES, avaliacoes)
        QMessageBox.information(self, "Avaliação registrada com sucesso!")

    def ver_ouvindo(self):
        avaliacoes = carregar_json(ARQUIVO_AVALIACOES)
        if not avaliacoes:
            sugestoes = random.sample(albuns_disponiveis, k=min(3, len(albuns_disponiveis)))
            texto = "\n".join(f"- {alb['nome']} ({alb['artista']})" for alb in sugestoes)
        else:
            escolhas = random.sample(list(avaliacoes.values()), k=min(3, len(avaliacoes)))
            texto = "\n".join(f"- {a['album']} by {a['artista']} ({a['nota']}/5): \"{a['comentario']}\"" for a in escolhas)

        QMessageBox.information(self, "O que estão ouvindo", texto)

    def adicionar_shout(self):
        email = self.usuario.get('email')
        shouts = carregar_json(ARQUIVO_SHOUTBOX)

        album, ok1 = QInputDialog.getText(self, "Shout", "Qual álbum você quer sugerir?")
        if not ok1 or not album.strip():
            QMessageBox.warning(self, "Erro", "Você deve informar o álbum.")
            return

        artista, ok2 = QInputDialog.getText(self, "Shout", "Nome do artista?")
        if not ok2 or not artista.strip():
            QMessageBox.warning(self, "Erro", "Você deve informar o artista.")
            return

        shouts[email] = {"album": album.strip(), "artista": artista.strip()}
        salvar_json(ARQUIVO_SHOUTBOX, shouts)
        QMessageBox.information(self, "Sucesso", "Shout adicionado!")

    def ver_novidades(self):
        texto = "\n".join(f"- {n['nome']} ({n['artista']})" for n in novidades)
        QMessageBox.information(self, "Novidades", texto)

    def fechar(self):
        self.close()


def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='UTF-8') as arquivo:
            return json.load(arquivo)
    return {}


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='UTF-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)




class telaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sons da Terra")
        self.setGeometry(200, 200, 500, 500)
        self.setWindowIcon(QIcon("imagens/Logo.png"))
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        self.setStyleSheet("background-color: #fcd967") 

        self.stack = QVBoxLayout()
        self.setLayout(self.stack)

        self.tela_login()

    def limpar_layout(self):
        while self.stack.count():
            widget = self.stack.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)
        else:
            return QFont("Arial", 20)
        

    def tela_login(self):
        sistema = sistemaDados
        self.limpar_layout()

        label = QLabel("Login:")
        label.setFont(self.fonte_subtitulo)
        label.setStyleSheet("color: #fffffd;")
        label.setAlignment(Qt.AlignBottom)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)

        botao_login = QPushButton("Entrar")
        botao_login.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold;")
        botao_login.clicked.connect(sistema.login()) 

        botao_ir_cadastro = QPushButton("Não tem conta? Cadastre-se agora!")
        botao_ir_cadastro.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold;")
        botao_ir_cadastro.clicked.connect(self.tela_cadastro)

        self.stack.addWidget(label)
        self.stack.addWidget(self.email_input)
        self.stack.addWidget(self.senha_input)
        self.stack.addWidget(botao_login)
        self.stack.addWidget(botao_ir_cadastro)

    def tela_cadastro(self):
        self.limpar_layout()

        label = QLabel("Cadastro:")
        label.setFont(self.fonte_subtitulo)
        label.setStyleSheet("color: #fffffd;")
        label.setAlignment(Qt.AlignBottom)
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")

        self.email_cadastro = QLineEdit()
        self.email_cadastro.setPlaceholderText("Email")

        self.senha_cadastro = QLineEdit()
        self.senha_cadastro.setPlaceholderText("Senha (6 números)")
        self.senha_cadastro.setEchoMode(QLineEdit.Password)

        self.confirmar_senha = QLineEdit()
        self.confirmar_senha.setPlaceholderText("Confirmar senha")
        self.confirmar_senha.setEchoMode(QLineEdit.Password)

        self.idade_input = QLineEdit()
        self.idade_input.setPlaceholderText("Idade")

        botao_cadastrar = QPushButton("Cadastrar")
        botao_cadastrar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold;")
        botao_cadastrar.clicked.connect(self.cadastrar)

        botao_voltar = QPushButton("Voltar")
        botao_voltar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold;")
        botao_voltar.clicked.connect(self.tela_login)

        self.stack.addWidget(label)
        self.stack.addWidget(self.nome_input)
        self.stack.addWidget(self.email_cadastro)
        self.stack.addWidget(self.senha_cadastro)
        self.stack.addWidget(self.confirmar_senha)
        self.stack.addWidget(self.idade_input)
        self.stack.addWidget(botao_cadastrar)
        self.stack.addWidget(botao_voltar)

    def login(self):
        sistema = sistemaDados
        email = self.email_input.text()
        senha = self.senha_input.text()
        sistema.login(email, senha)
        QMessageBox.information(self, "Login", f"Olá")
    
    def login(self):
        email = self.email_input.text()
        senha = self.senha_input.text()
        usuarios = carregar_usuarios()

        if email in usuarios and usuarios[email]['senha'] == senha:
            QMessageBox.information(self, "Login", f"Bem-vindo, {usuarios[email]['nome']}!")
            self.menu = MenuPrincipal(usuarios[email])
            self.menu.show()
            self.close()  
        else:
            QMessageBox.warning(self,  "Erro", "Email ou senha inválidos.")

    def cadastrar(self):
        nome = self.nome_input.text().title().strip()
        email = self.email_cadastro.text().strip()
        senha = self.senha_cadastro.text()
        confirmar = self.confirmar_senha.text()
        idade = self.idade_input.text().strip()

        usuarios = carregar_usuarios()

        if not nome.replace(" ", "").isalpha():
            QMessageBox.warning(self, "erro","Nome inválido. Use apenas letras.")
            return
        if email in usuarios or " " in email or "@" not in email or not (email.endswith("gmail.com") or email.endswith("ufrpe.com")):
            QMessageBox.warning(self, "erro","Email inválido ou já cadastrado.")
            return
        if len(senha) != 6 or not senha.isdigit():
            QMessageBox.warning(self, "erro." "Senha inválida. Use 6 números.")
            return
        if senha != confirmar:
            QMessageBox.warning(self, "erro",". Senhas não coincidem.")
            return
        if not idade.isdigit():
            QMessageBox.warning(self, "erro."," Idade deve ser numérica.")
            return

        usuarios[email] = {
            "nome": nome,
            "senha": senha,
            "idade": idade
        }

        salvar_usuarios(usuarios)
        QMessageBox.information(self, "Sucesso", "Cadastro realizado!")
        self.tela_login()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = telaInicial()
    janela.show()
    sys.exit(app.exec())
