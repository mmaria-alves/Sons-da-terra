import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QInputDialog
)
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtCore import Qt, QTimer
from autenticadores import Autenticadores, configuracoesUsuario
from sistemas import sistemaAvaliacao, sistemaOuvindo, sistemaShoutboxd


class telaLogin(QWidget):
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

    def abrir_menu_principal(self, usuario):
        self.menu = menuPrincipal(self.autenticador)
        self.menu.show()
        self.close()

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
        self.cadastro = telaCadastro(self.autenticador)
        self.cadastro.show()


class telaCadastro(QWidget):
    def __init__(self, autenticador):
        super().__init__()
        self.autenticador = autenticador
        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 200, 500, 500)
        
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")

        self.init_ui()

        self.setStyleSheet('background-color: #fcd967')
    
    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)

        else:
            return QFont("Arial", 20)

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
        botao_cadastrar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_cadastrar.clicked.connect(self.realizar_cadastro)

        botao_voltar = QPushButton("Voltar")
        botao_voltar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_voltar.clicked.connect(self.voltar)

        label_cadastro = QLabel("Cadastro")
        label_cadastro.setFont(self.fonte_subtitulo)
        label_cadastro.setStyleSheet("color: #fffffd; font-size: 70px; font-weight: bold;")
        label_cadastro.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        layout.addWidget(label_cadastro)
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
        self.login = telaLogin(self.autenticador)
        self.login.show()

class menuPrincipal(QWidget):
    def __init__(self, autenticador):
        super().__init__()
        self.autenticador = autenticador
        self.usuario = autenticador.usuario_logado


        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 200, 500, 500)
        
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        self.init_ui()

        self.setStyleSheet('background-color: #fcd967')
    
    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)

        else:
            return QFont("Arial", 20)
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        destaque = self.autenticador.destaque_da_semana()

        destaque = self.autenticador.destaque_da_semana()
        texto_destaque = f"Destaque da Semana: {destaque['nome']} - {destaque['artista']}" if isinstance(destaque, dict) else f"Destaque da Semana: {destaque}"
        self.label_destaque = QLabel(texto_destaque)

        self.label_destaque.setFont(self.fonte_titulo)
        self.label_destaque.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.label_destaque.setStyleSheet("""
            background-color: #5966b1;
            color: #fffffd;
            font-size: 20px;
        """)
        self.label_destaque.setAlignment(Qt.AlignCenter)


        botao_avaliar = QPushButton("Avaliar Álbuns")
        botao_avaliar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_avaliar.clicked.connect(self.avaliar_albuns)
        

        botao_shoutboxd = QPushButton("Shoutboxd")
        botao_shoutboxd.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_shoutboxd.clicked.connect(self.adicionar_shout)


        botao_ouvindo_agora = QPushButton("Ouvindo Agora")
        botao_ouvindo_agora.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_ouvindo_agora.clicked.connect(self.ouvindo_agora)

        botao_config = QPushButton("Configurações")
        botao_config.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: light;")
        botao_config.clicked.connect(self.abrir_configuracoes)
        
        
        layout.addWidget(self.label_destaque)
        layout.addWidget(botao_avaliar)
        layout.addWidget(botao_shoutboxd)
        layout.addWidget(botao_ouvindo_agora)
        layout.addWidget(botao_config)
        
        self.setLayout(layout)

    def avaliar_albuns(self):
        if not hasattr(self.autenticador, 'albuns_disponiveis'):
            self.autenticador.albuns_disponiveis = self.autenticador.carregar_albuns()

        self.avaliacao_window = sistemaAvaliacao(
            usuario_logado=self.autenticador.usuario_logado,
            albuns_disponiveis=self.autenticador.albuns_disponiveis
        )
        self.avaliacao_window.show()
    
    def adicionar_shout(self):
        try:
            if not self.autenticador.usuario_logado:
                print("Erro: Nenhum usuário logado")
                return
                
            if not hasattr(self.autenticador, 'albuns_disponiveis'):
                self.autenticador.albuns_disponiveis = self.autenticador.carregar_albuns()
                
            sistema = sistemaShoutboxd(self.autenticador.usuario_logado,
                                     self.autenticador.albuns_disponiveis)
            sistema.adicionar_shouts()
        except Exception as e:
            print(f"Erro ao adicionar shout: {e}")
    
    def ouvindo_agora(self):
        try:
            sistema = sistemaOuvindo()
            sistema.ouvindo_agora()
        except Exception as e:
            print(f"Erro ao abrir 'ouvindo agora': {e}")
    
    def abrir_configuracoes(self):
        self.tela_config = TelaConfiguracoes(self.usuario_logado, self.usuarios, self.voltar_ao_login)
        self.tela_config.show()
        self.close()

    

class TelaConfiguracoes(QWidget):
    def __init__(self, usuario_logado, usuarios, voltar_callback):
        super().__init__()
        self.setWindowTitle("Configurações da Conta")
        self.configuracoes = configuracoesUsuario(usuario_logado, usuarios)
        self.voltar_callback = voltar_callback
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        btn_ver_dados = QPushButton("Ver meus dados")
        btn_atualizar_nome = QPushButton("Atualizar Nome")
        btn_atualizar_senha = QPushButton("Atualizar Senha")
        btn_apagar_conta = QPushButton("Apagar minha conta")
        btn_voltar = QPushButton("Voltar")

        btn_ver_dados.clicked.connect(self.exibir_dados)
        btn_atualizar_nome.clicked.connect(self.atualizar_nome)
        btn_atualizar_senha.clicked.connect(self.atualizar_senha)
        btn_apagar_conta.clicked.connect(self.apagar_conta)
        btn_voltar.clicked.connect(self.voltar_callback)

        layout.addWidget(btn_ver_dados)
        layout.addWidget(btn_atualizar_nome)
        layout.addWidget(btn_atualizar_senha)
        layout.addWidget(btn_apagar_conta)
        layout.addWidget(btn_voltar)
        self.setLayout(layout)

    def exibir_dados(self):
        dados = self.configuracoes.ver_dados()
        QMessageBox.information(self, "Seus Dados",
            f"Email: {dados['email']}\nNome: {dados['nome']}\nSenha: {dados['senha']}")

    def atualizar_nome(self):
        novo_nome, ok = QInputDialog.getText(self, "Atualizar Nome", "Novo nome:")
        if ok and novo_nome:
            sucesso, msg = self.configuracoes.atualizar_nome(novo_nome.strip().title())
            if sucesso:
                self.configuracoes.salvar_usuarios()
            QMessageBox.information(self, "Atualização", msg)

    def atualizar_senha(self):
        nova_senha, ok = QInputDialog.getText(self, "Atualizar Senha", "Nova senha (6 números):")
        if ok and nova_senha:
            sucesso, msg = self.configuracoes.atualizar_senha(nova_senha.strip())
            if sucesso:
                self.configuracoes.salvar_usuarios()
            QMessageBox.information(self, "Atualização", msg)

    def apagar_conta(self):
        confirmacao = QMessageBox.question(self, "Apagar Conta",
            "Tem certeza que deseja apagar sua conta?", QMessageBox.Yes | QMessageBox.No)
        if confirmacao == QMessageBox.Yes:
            sucesso = self.configuracoes.apagar_conta()
            if sucesso:
                QMessageBox.information(self, "Sucesso", "Conta apagada.")
                self.close()
                self.voltar_callback()  # Voltar ao login



if __name__ == "__main__":
    app = QApplication(sys.argv)
    autenticador = Autenticadores()
    janela_login = telaLogin(autenticador)
    janela_login.show()
    sys.exit(app.exec())