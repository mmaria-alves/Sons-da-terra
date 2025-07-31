import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QInputDialog, QHBoxLayout
from PySide6.QtGui import QFontDatabase, QFont, QIcon, QPixmap, QTransform
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property
from autenticadores import Autenticadores, configuracoesUsuario
from sistemas import sistemaAvaliacao, sistemaOuvindo, sistemaShoutboxd


class telaLogin(QWidget):
    def __init__(self, autenticadores):
        super().__init__()
        self.autenticador = autenticadores
        # Definindo configurações da página
        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 100, 500, 500)
        self.setStyleSheet('background-color: #fcd967')
        
        # Definindo as fontes que serão utilizadas
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        # Definindo as configurações da animação da imagem
        self.original_pixmap = None
        self._angle = 0
        self.animacao = None
        self.label_imagem = None

        # Definindo as configurações da animação do texto
        self.texto = "BEM VINDO AO SONS DA TERRA "
        self.posicao = 0
        
        # Inicializando a tela inicial
        self.init_ui()
        
    @Property(float)
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, valor):
        self._angle = valor
        self.atualizar_rotacao()
    
    def atualizar_rotacao(self):
        if self.original_pixmap and self.label_imagem:
            transform = QTransform()
            transform.rotate(self._angle)
            rotated_pixmap = self.original_pixmap.transformed(transform, Qt.SmoothTransformation)
            self.label_imagem.setPixmap(rotated_pixmap)
    
    def animacao_logo(self):
        self.animacao = QPropertyAnimation(self, b"angle")
        self.animacao.setDuration(3000)
        self.animacao.setStartValue(0)
        self.animacao.setEndValue(360)
        self.animacao.setLoopCount(-1)
        self.animacao.setEasingCurve(QEasingCurve.Linear)
    
    def iniciar_animacao(self):
        if self.animacao:
            self.animacao.start()

    def parar_animacao(self):
        if self.animacao:
            self.animacao.stop()

    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)

        else:
            return QFont("Arial", 20)

    def animar_textos(self):
        # Letreiro 2 - anda pra esquerda
        self.posicao = (self.posicao - 1) % len(self.texto)
        texto_animado = self.texto[self.posicao:] + self.texto[:self.posicao]
        self.label_animada.setText(texto_animado)
      
    def init_ui(self):
        '''Inicializa a interface'''
        main_layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedSize(500, 23)
        self.email_input.setStyleSheet("color: #001f54; font-size: 13px")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setFixedSize(500, 23)
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.senha_input.setStyleSheet("color: #001f54; font-size: 13px")

        botao_login = QPushButton("Entrar")
        botao_login.setFixedSize(500, 25)
        botao_login.setFont(self.fonte_texto)
        botao_login.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_login.clicked.connect(self.fazer_login)

        botao_esqueci_senha = QPushButton('Esqueceu sua senha?')
        botao_esqueci_senha.setFixedSize(500, 25)
        botao_esqueci_senha.setFont(self.fonte_texto)
        botao_esqueci_senha.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_esqueci_senha.clicked.connect(self.abrir_recuperacao)

        botao_cadastro = QPushButton("Não possui uma conta? Cadastre-se agora!")
        botao_cadastro.setFont(self.fonte_texto)
        botao_cadastro.setFixedSize(500, 25)
        botao_cadastro.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_cadastro.clicked.connect(self.abrir_cadastro)

        label = QLabel("Sons da Terra")
        label.setFont(self.fonte_titulo)
        label.setStyleSheet("color: #fffffd; font-size: 70px; font-weight: bold;")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        self.label_animada = QLabel(self.texto) #color: fbcf41 #background-color: #fffffd
        self.label_animada.setFont(self.fonte_titulo)
        self.label_animada.setStyleSheet('''
                                          background-color: #5966b1;
                                          color: #fffffd; 
                                          border-radius: 100px;
                                          font-size: 25px; 
                                          ''')
        self.label_animada.setAlignment(Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animar_textos)
        self.timer.start(500)

        label_login = QLabel('Login: ')
        label_login.setFont(self.fonte_subtitulo)
        label_login.setStyleSheet("color: #fffffd; font-size: 40px; font-weight: bold;")
        label_login.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        imagem = QPixmap('imagens/Logo.png')
        self.original_pixmap = imagem.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(500, 200)
        self.label_imagem.setAlignment(Qt.AlignCenter)
        self.label_imagem.setPixmap(self.original_pixmap)
        
        self.animacao_logo()
        self.iniciar_animacao()

        # Adiciona todos os elementos no layout
        main_layout.addWidget(label)
        main_layout.addWidget(self.label_animada)
        main_layout.addWidget(self.label_imagem)
        main_layout.addWidget(label_login)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(self.senha_input)
        main_layout.addWidget(botao_login)        
        main_layout.addWidget(botao_esqueci_senha)
        main_layout.addWidget(botao_cadastro)

        self.setLayout(main_layout)

    def abrir_menu_principal(self, usuario):
        '''Inicializa a tela do menu principal'''
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
        '''Inicializa a tela de cadastro'''
        self.hide()
        self.cadastro = telaCadastro(self.autenticador)
        self.cadastro.show()
    
    def abrir_recuperacao(self):
        '''Abre a tela de recuperação de senha'''
        self.hide()
        self.recuperacao = telaRecuperar1(autenticador)
        self.recuperacao.show()

class telaCadastro(QWidget):
    def __init__(self, autenticador):
        super().__init__()
        self.autenticador = autenticador
        # Configurações da página
        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 200, 500, 500)
        self.setStyleSheet('background-color: #fcd967')
        
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        # Configurações iniciais da animação:
        self.original_pixmap = None
        self._angle = 0
        self.animacao = None
        self.label_imagem = None

        self.init_ui()


    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)
        else:
            return QFont("Arial", 20)

    @Property(float)
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, valor):
        self._angle = valor
        self.atualizar_rotacao()
    
    def atualizar_rotacao(self):
        if self.original_pixmap and self.label_imagem:
            transform = QTransform()
            transform.rotate(self._angle)
            rotated_pixmap = self.original_pixmap.transformed(transform, Qt.SmoothTransformation)
            self.label_imagem.setPixmap(rotated_pixmap)
    
    def animacao_logo(self):
        self.animacao = QPropertyAnimation(self, b"angle")
        self.animacao.setDuration(3000)
        self.animacao.setStartValue(0)
        self.animacao.setEndValue(360)
        self.animacao.setLoopCount(-1)
        self.animacao.setEasingCurve(QEasingCurve.Linear)
    
    def iniciar_animacao(self):
        '''Inicia a animação'''
        if self.animacao:
            self.animacao.start()

    def parar_animacao(self):
        '''Para a animação'''
        if self.animacao:
            self.animacao.stop()

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
        botao_cadastrar.setFont(self.fonte_texto)
        botao_cadastrar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_cadastrar.clicked.connect(self.realizar_cadastro)

        botao_voltar = QPushButton("Voltar")
        botao_voltar.setFont(self.fonte_texto)
        botao_voltar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_voltar.clicked.connect(self.voltar)

        label_cadastro = QLabel("Cadastro:")
        label_cadastro.setFont(self.fonte_subtitulo)
        label_cadastro.setStyleSheet("color: #fffffd; font-size: 70px; font-weight: bold;")
        label_cadastro.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        imagem = QPixmap('imagens/Logo.png')
        self.original_pixmap = imagem.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(500, 200)
        self.label_imagem.setAlignment(Qt.AlignCenter)
        self.label_imagem.setPixmap(self.original_pixmap)
        
        self.animacao_logo()
        self.iniciar_animacao()

        layout.addWidget(self.label_imagem)
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
        self.parar_animacao()
        self.hide()
        self.login = telaLogin(self.autenticador)
        self.login.show()

class telaRecuperar1(QWidget):
    def __init__(self, autenticador):
        super().__init__()
        self.autenticador = autenticador
        self.setWindowTitle('Recuperar Senha')
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 200, 400, 200)
        self.setStyleSheet('background-color: #fcd967')
        
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")

        self.init_ui()

    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)
        else:
            return QFont("Arial", 20)
        
    def enviar_codigo(self):
        email = self.email_input.text()
        if Autenticadores.solicitar_codigo(email):
            QMessageBox.information(self, "Sucesso", "Código enviado por email")
        else: 
            QMessageBox.warning(self, "Erro", "E-mail não encontrado ou falha no envio")
    
    def validar_codigo(self):
        email = self.email_input.text()
        codigo = self.codigo_input.text()
        nova_senha = self.nova_senha_input.text()

        resultado = Autenticadores.validar_codigo(email, codigo, nova_senha)
        if resultado == "Senha redefinada com sucesso!":
            QMessageBox.information(self, 'Ok', resultado)
            self.close()
        else:
            QMessageBox.warning(self, 'Erro', resultado)

    def voltar(self):
        self.hide()
        self.login = telaLogin(self.autenticador)
        self.login.show()

    def init_ui(self):
        layout = QVBoxLayout()
        label_recuperacao = QLabel(
        '''
Recuperação 
De senha: ''')
        
        label_recuperacao.setFont(self.fonte_subtitulo)
        label_recuperacao.setStyleSheet("color: #fffffd; font-size: 40px; font-weight: bold;")
        label_recuperacao.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        self.email_input = QLineEdit()
        self.email_input.setFixedSize(400, 23)
        self.email_input.setPlaceholderText('Email')
        self.email_input.setStyleSheet("color: #001f54; font-size: 13px")
        
        self.botao_enviar_codigo = QPushButton('Enviar código')
        self.botao_enviar_codigo.setFixedSize(400, 25)
        self.botao_enviar_codigo.setFont(self.fonte_texto)
        self.botao_enviar_codigo.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px;")
        self.botao_enviar_codigo.clicked.connect(self.enviar_codigo)
        self.botao_enviar_codigo.clicked.connect(self.abrir_recuperacao2)
        
        self.botao_voltar = QPushButton('Voltar')
        self.botao_voltar.setFixedSize(400, 25)
        self.botao_voltar.setFont(self.fonte_texto)
        self.botao_voltar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px;")
        self.botao_voltar.clicked.connect(self.voltar)
        
        layout.addWidget(label_recuperacao)
        layout.addWidget(self.email_input)
        layout.addWidget(self.botao_enviar_codigo)
        layout.addWidget(self.botao_voltar)

        self.setLayout(layout)

    def abrir_recuperacao2(self):
        email = self.email_input.text()
        self.hide()
        self.recuperacao = telaRecuperar2(email)
        self.recuperacao.show()

class telaRecuperar2(QWidget):
        def __init__(self, email_usuario):
            super().__init__()
            self.email_usuario = email_usuario
            self.setWindowTitle("Recuperar senha")
            self.setWindowIcon(QIcon('imagens/Logo.png'))
            self.setGeometry(200, 200, 400, 300)
            self.setStyleSheet('background-color: #fcd967')
            
            self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
            self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
            self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")

            self.init_ui()
        
        def carregar_fonte(self, caminho_fonte: str):
            id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
            familias = QFontDatabase.applicationFontFamilies(id_fonte)

            if familias:
                return QFont(familias[0], 50)

            else:
                return QFont("Arial", 20)
        
        def validar_codigo(self):
            email = self.email_usuario
            codigo = self.codigo_input.text()
            nova_senha = self.nova_senha_input.text()

            resultado = Autenticadores.validar_codigo(email, codigo, nova_senha)
            if resultado == "Senha redefinada com sucesso!":
                QMessageBox.information(self, 'Ok', resultado)
                self.close()
            else:
                QMessageBox.warning(self, 'Erro', resultado)
        
        def abrir_login(self):
            self.hide()
            self.login = telaLogin()
            self.login.show()

        
        def init_ui(self):
            layout = QVBoxLayout()
            label_recuperacao = QLabel('Código: ')
            label_recuperacao.setFont(self.fonte_subtitulo)
            label_recuperacao.setStyleSheet("color: #fffffd; font-size: 40px; font-weight: bold;")
            label_recuperacao.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

            self.codigo_input = QLineEdit()
            self.codigo_input.setFixedSize(400, 23) 
            self.codigo_input.setStyleSheet("color: #001f54; font-size: 13px")
            self.codigo_input.setPlaceholderText('Digite o código')
            
            label_nova_senha = QLabel('Nova senha: ')
            label_nova_senha.setFont(self.fonte_subtitulo)
            label_nova_senha.setStyleSheet("color: #fffffd; font-size: 40px; font-weight: bold")
            label_nova_senha.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

            self.nova_senha_input = QLineEdit()
            self.nova_senha_input.setFixedSize(400, 23)
            self.nova_senha_input.setStyleSheet("color: #001f54; font-size: 13px")
            self.nova_senha_input.setPlaceholderText('Nova senha')
            self.nova_senha_input.setEchoMode(QLineEdit.Password)

            self.botao_confirmar = QPushButton('Confirmar nova senha')
            self.botao_confirmar.setFont(self.fonte_texto)
            self.botao_confirmar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-size: 14px; font-weight: bold")
            self.botao_confirmar.clicked.connect(self.validar_codigo)
                
                # Adicionar o método que volta para o login
            layout.addWidget(label_recuperacao)
            layout.addWidget(self.codigo_input)
            layout.addWidget(label_nova_senha)
            layout.addWidget(self.nova_senha_input)
            layout.addWidget(self.botao_confirmar)

            self.setLayout(layout)

class menuPrincipal(QWidget):
    def __init__(self, autenticador):
        super().__init__()
        self.autenticador = autenticador
        self.usuario = autenticador.usuario_logado
        self.usuarios = autenticador.carregar_usuarios()

        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 100, 960, 540)
        self.setStyleSheet('background-color: #fcd967')
        
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        self.original_pixmap = None
        self._angle = 0
        self.animacao = None
        self.label_imagem = None

        self.init_ui()

    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)

        else:
            return QFont("Arial", 20)
    
    @Property(float)
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, valor):
        self._angle = valor
        self.atualizar_rotacao()
    
    def atualizar_rotacao(self):
        if self.original_pixmap and self.label_imagem:
            transform = QTransform()
            transform.rotate(self._angle)
            rotated_pixmap = self.original_pixmap.transformed(transform, Qt.SmoothTransformation)
            self.label_imagem.setPixmap(rotated_pixmap)
    
    def animacao_logo(self):
        self.animacao = QPropertyAnimation(self, b"angle")
        self.animacao.setDuration(3000)
        self.animacao.setStartValue(0)
        self.animacao.setEndValue(360)
        self.animacao.setLoopCount(-1)
        self.animacao.setEasingCurve(QEasingCurve.Linear)
    
    def iniciar_animacao(self):
        if self.animacao:
            self.animacao.start()

    def parar_animacao(self):
        if self.animacao:
            self.animacao.stop()

    def init_ui(self):
        main_layout = QHBoxLayout()
        layout_esquerda = QVBoxLayout()
        layout_direita = QVBoxLayout()

        # layout da parte esquerda da janela
        botao_avaliar = QPushButton("Avaliar Álbuns")
        botao_avaliar.setFixedSize(480, 25)
        botao_avaliar.setFont(self.fonte_texto)
        botao_avaliar.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_avaliar.clicked.connect(self.avaliar_albuns)
        
        botao_shoutboxd = QPushButton("Shoutboxd")
        botao_shoutboxd.setFixedSize(480, 25)
        botao_shoutboxd.setFont(self.fonte_texto)
        botao_shoutboxd.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_shoutboxd.clicked.connect(self.adicionar_shout)

        botao_ouvindo_agora = QPushButton("O que as pessoas estão ouvindo?")
        botao_ouvindo_agora.setFixedSize(480, 25)
        botao_ouvindo_agora.setFont(self.fonte_texto)
        botao_ouvindo_agora.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px;")
        botao_ouvindo_agora.clicked.connect(self.ouvindo_agora)

        botao_config = QPushButton("Configurações")
        botao_config.setFixedSize(480, 25)
        botao_config.setFont(self.fonte_texto)
        botao_config.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_config.clicked.connect(self.abrir_configuracoes)

        botao_recomendacao = QPushButton("Sem ideia do que ouvir? Clica aqui!")
        botao_recomendacao.setFixedSize(480, 25)
        botao_recomendacao.setFont(self.fonte_texto)
        botao_recomendacao.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")

        imagem_logo = QPixmap('imagens/Logo.png')
        self.original_pixmap = imagem_logo.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(480, 200)
        self.label_imagem.setAlignment(Qt.AlignCenter)
        self.label_imagem.setPixmap(self.original_pixmap)

        self.animacao_logo()
        self.iniciar_animacao()

        layout_esquerda.addWidget(self.label_imagem)
        layout_esquerda.addWidget(botao_recomendacao)
        layout_esquerda.addWidget(botao_avaliar)
        layout_esquerda.addWidget(botao_shoutboxd)
        layout_esquerda.addWidget(botao_ouvindo_agora)
        layout_esquerda.addWidget(botao_config)
        
        # layout da parte direita da janela
        label_destaque = QLabel("Destaque da Semana")
        label_destaque.setFont(self.fonte_titulo)
        label_destaque.setStyleSheet("color: #fffffd; font-weight: bold; font-size: 40px")
        label_destaque.setAlignment(Qt.AlignHCenter| Qt.AlignTop)
        
        destaque = self.autenticador.destaque_da_semana()

        album = destaque['album']
        texto_destaque = (f'''{album['nome']}
por {album['artista']}''')
        
        capa = QPixmap(album['capa'])
        self.pixmap_capa = capa.scaled(230, 230, Qt.KeepAspectRatio, Qt.SmoothTransformation) 

        self.label_album_destaque = QLabel(texto_destaque)
        self.label_album_destaque.setFixedSize(480, 70)
        self.label_album_destaque.setFont(self.fonte_titulo)
        self.label_album_destaque.setStyleSheet("background-color: #5966b1; color: #fffffd; font-size: 20px; border-radius: 5px;")
        self.label_album_destaque.setAlignment(Qt.AlignCenter)
    
        
        self.label_capa = QLabel(self)
        self.label_capa.setFixedSize(480, 240)
        self.label_capa.setStyleSheet("background-color: #fcd967; border-radius: 15px")
        self.label_capa.setPixmap(self.pixmap_capa)
        self.label_capa.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        layout_direita.addWidget(label_destaque)
        layout_direita.addWidget(self.label_capa)
        layout_direita.addWidget(self.label_album_destaque)
        layout_direita.addStretch()

        main_layout.addLayout(layout_esquerda)
        main_layout.addLayout(layout_direita)

        self.setLayout(main_layout)

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
        self.parar_animacao()
        self.tela_config = TelaConfiguracoes(self.usuario, self.usuarios)
        self.tela_config.show()
        self.close()
    
class TelaConfiguracoes(QWidget):
    def __init__(self, usuario_logado, usuarios):
        super().__init__()
        self.configuracoes = configuracoesUsuario(usuario_logado, usuarios)
        # Definindo configurações da página
        self.setWindowTitle("Sons da Terra")
        self.setWindowIcon(QIcon('imagens/Logo.png'))
        self.setGeometry(200, 100, 500, 500)
        self.setStyleSheet('background-color: #fcd967')
        
        # Definindo as fontes que serão utilizadas
        self.fonte_subtitulo = self.carregar_fonte("fontes/Coco-Sharp-Bold-trial.ttf")
        self.fonte_titulo = self.carregar_fonte("fontes/Coco-Sharp-Regular-trial.ttf")
        self.fonte_texto = self.carregar_fonte("fontes/Coco-Sharp-Light-trial.ttf")
        
        # Configurações iniciais da animação:
        self.original_pixmap = None
        self._angle = 0
        self.animacao = None
        self.label_imagem = None
        # Inicializando a tela
        self.init_ui()

    def carregar_fonte(self, caminho_fonte: str):
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        familias = QFontDatabase.applicationFontFamilies(id_fonte)

        if familias:
            return QFont(familias[0], 50)
        else:
            return QFont("Arial", 20)
    
    @Property(float)
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, valor):
        self._angle = valor
        self.atualizar_rotacao()
    
    def atualizar_rotacao(self):
        if self.original_pixmap and self.label_imagem:
            transform = QTransform()
            transform.rotate(self._angle)
            rotated_pixmap = self.original_pixmap.transformed(transform, Qt.SmoothTransformation)
            self.label_imagem.setPixmap(rotated_pixmap)
    
    def animacao_logo(self):
        self.animacao = QPropertyAnimation(self, b"angle")
        self.animacao.setDuration(3000)
        self.animacao.setStartValue(0)
        self.animacao.setEndValue(360)
        self.animacao.setLoopCount(-1)
        self.animacao.setEasingCurve(QEasingCurve.Linear)
    
    def iniciar_animacao(self):
        '''Inicia a animação'''
        if self.animacao:
            self.animacao.start()

    def parar_animacao(self):
        '''Para a animação'''
        if self.animacao:
            self.animacao.stop()
    
    def voltar_login(self):
        self.hide()
        self.login = telaLogin()
        self.login.show()
    
    def voltar_menu(self):
        self.hide()
        self.menu_principal = menuPrincipal(autenticador)
        self.menu_principal.show()
    
    def init_ui(self):
        layout = QVBoxLayout()

        label_configuracoes = QLabel("Configurações")
        label_configuracoes.setFont(self.fonte_titulo)
        label_configuracoes.setStyleSheet("color: #fffffd; font-weight: bold; font-size: 60px")
        label_configuracoes.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        botao_ver_dados = QPushButton("Ver meus dados")
        botao_ver_dados.setFixedSize(500, 25)
        botao_ver_dados.setFont(self.fonte_texto)
        botao_ver_dados.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_ver_dados.clicked.connect(self.exibir_dados)

        botao_att_nome = QPushButton("Atualizar Nome")
        botao_att_nome.setFixedSize(500, 25)
        botao_att_nome.setFont(self.fonte_texto)
        botao_att_nome.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_att_nome.clicked.connect(self.atualizar_nome)

        botao_att_senha = QPushButton("Atualizar Senha")
        botao_att_senha.setFixedSize(500, 25)
        botao_att_senha.setFont(self.fonte_texto)
        botao_att_senha.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_att_senha.clicked.connect(self.atualizar_senha)
        
        botao_del_conta = QPushButton("Apagar minha conta")
        botao_del_conta.setFixedSize(500, 25)
        botao_del_conta.setFont(self.fonte_texto)
        botao_del_conta.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_del_conta.clicked.connect(self.apagar_conta)

        botao_voltar_menu = QPushButton("Voltar para o menu")
        botao_voltar_menu.setFixedSize(500, 25)
        botao_voltar_menu.setFont(self.fonte_texto)
        botao_voltar_menu.setStyleSheet("background-color: #5966b1; color: #fffffd; font-weight: bold; font-size: 14px")
        botao_voltar_menu.clicked.connect(self.voltar_menu)
        
        imagem = QPixmap('imagens/Logo.png')
        self.original_pixmap = imagem.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(500, 170)
        self.label_imagem.setPixmap(self.original_pixmap)
        self.label_imagem.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.animacao_logo()
        self.iniciar_animacao()

        layout.addWidget(label_configuracoes)        
        layout.addWidget(self.label_imagem)
        layout.addWidget(botao_ver_dados)
        layout.addWidget(botao_att_nome)
        layout.addWidget(botao_att_senha)
        layout.addWidget(botao_del_conta)
        layout.addWidget(botao_voltar_menu)
        
        self.setLayout(layout)

    def exibir_dados(self):
        dados = self.configuracoes.ver_dados()
        QMessageBox.information(self, "Seus Dados",
            f"Email: {dados['email']}\nNome: {dados['nome']}\nSenha: {dados['senha']}")

    def atualizar_nome(self):
        novo_nome, ok = QInputDialog.getText(self, "Atualizar Nome", "Novo nome:")
        if ok and novo_nome:
            sucesso, mensagem = self.configuracoes.atualizar_nome(novo_nome.strip().title())
            if sucesso:
                self.configuracoes.salvar_usuarios()
            QMessageBox.information(self, "Atualização", mensagem)

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
                self.voltar_login()
                
 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    autenticador = Autenticadores()
    janela_login = telaLogin(autenticador)
    janela_login.show()
    sys.exit(app.exec())