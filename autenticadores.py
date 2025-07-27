import os
import json
from datetime import datetime, timedelta
import random
import smtplib
from email.message import EmailMessage
from sistemas import sistemaAvaliacao, sistemaOuvindo, sistemaShoutboxd

EMAIL_REMETENTE = 'noreply.sonsdaterra@gmail.com'
SENHA_REMETENTE = 'pppd jwml xftl uwxb'

class Usuario:
    def __init__(self, nome, email, senha,):
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
    def from_dict(dados):
        return Usuario(dados['nome'], dados['email'], dados['senha'])
    
    def to_dict(self):
        return {'nome': self.nome, 'email': self.email, 'senha': self.senha}


class Autenticadores:
    def __init__(self, caminho_arquivo="dados/usuarios.json"):
        self.caminho_arquivo = caminho_arquivo
        self.usuarios = self.carregar_usuarios()
        self.usuario_logado = None
        self.albuns_disponiveis = self.carregar_albuns()

    def carregar_usuarios(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        return {}

    def salvar_usuarios(self):
        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(self.usuarios, arquivo, indent=4, ensure_ascii=False)

    def carregar_usuario(self, email):
        if email in self.usuarios:
            return Usuario.from_dict(self.usuarios[email])
        return None
    
    def carregar_albuns(self, caminho="dados/albuns.json"):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

       
    def cadastrar_usuario(self, nome, email, senha, confirmar_senha):
        if not all(n.isalpha() or n.isspace() for n in nome):
            return False, "Nome inválido. Utilize apenas letras."
        
        elif email in self.usuarios:
            return False, "Email já cadastrado."
        
        elif " " in email:
            return False, "Email inválido. Contém espaços."
        
        elif not(email.endswith("gmail.com") or email.endswith("ufrpe.br")):
            return False, "Email inválido. Domínio inválido."
        
        elif "@" not in email:
            return False, "Email inválido. Não contém @"
        
        elif len(senha) != 6 and not senha.isdigit():
            return False, "Senha inválida. Deve conter apenas seis números"
        
        elif senha != confirmar_senha:
            return False, "As senhas não coincidem."
        
        
        novo_usuario = Usuario(nome, email, senha)
        self.usuarios[email] = novo_usuario.to_dict()
        self.salvar_usuarios()
        return True, "Usuário cadastrado com sucesso!"


    def login(self, email, senha):
        usuario = self.carregar_usuario(email)
        if usuario and usuario.senha == senha:
            self.usuario_logado = usuario
            return True, usuario
        else:
            return False, None
        
    def avaliar_album_terminal(self):
        try:
            # Verifica se os álbuns estão carregados
            if not hasattr(self, 'albuns_disponiveis') or not self.albuns_disponiveis:
                self.albuns_disponiveis = self.carregar_albuns()

            # Verifica se há usuário logado
            if not self.usuario_logado:
                raise ValueError("Nenhum usuário logado")

            sistema = sistemaAvaliacao(self.usuario_logado, self.albuns_disponiveis)
            sistema.avaliar_album()

        except Exception as e:
            print(f"Erro ao avaliar álbum: {e}")
            return False
        return True
    
    def adicionar_shouts_terminal(self):
        sistema = sistemaShoutboxd(self.usuario_logado, self.albuns_disponiveis)
        sistema.adicionar_shouts()
    
    def ouvindo_agora_terminal(self):
        sistema = sistemaOuvindo()
        sistema.ouvindo_agora()
        
    def destaque_da_semana(self, caminho='dados/destaque.json'):
        hoje = datetime.date.today()
        semana_atual = hoje.isocalendar()[1]

        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                if dados.get('semana') == semana_atual:
                    return dados.get('album')

        destaque = random.choice(list(self.albuns_disponiveis.values()))  # Ajuste conforme estrutura
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump({'semana': semana_atual, 'album': destaque}, arquivo)
        return destaque
    
    @staticmethod
    def enviar_codigo(destinatario, codigo):
        mensagem = EmailMessage()
        mensagem['Subject'] = 'Recuperação de Senha'
        mensagem['From'] = EMAIL_REMETENTE
        mensagem['To'] = destinatario
        mensagem.set_content(f'''
                             Seu código de verificação é {codigo}
                             Válido por 10 minutos
                            ''')
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_REMETENTE)
                smtp.send_message(mensagem)
                return True
        
        except Exception as e:
            print(f'Erro ao enviar e-mail: {e}')
            return False
    
    @staticmethod
    def solicitar_codigo(email_usuario):
        usuarios = Autenticadores.carregar_usuarios()
        for usuario, dados in usuarios.items():
            if dados['email'] == email_usuario:
                codigo = random.randomint(100000, 999999)
                tempo = (datetime.now() + timedelta(minutes=10)).isoformat()

                dados['codigo'] = codigo
                dados['tempo'] = tempo
                Autenticadores.salvar_usuarios()

                enviado = Autenticadores.enviar_codigo(email_usuario, codigo)
                return enviado
        return False
    
    @staticmethod
    def validar_codigo(email_usuario, codigo_digitado, nova_senha):
        usuarios = Autenticadores.carregar_usuarios()
        for usuario, dados in usuario.items():
            if dados['email'] == email_usuario:
                if dados['codigo'] != codigo_digitado:
                    return 'Código inválido'
                if datetime.now() > datetime.fromisoformat(dados['tempo']):
                    return 'Código expirado'
                
                dados['senha'] == nova_senha
                dados['codigo'] == ''
                dados['tempo'] == ''
                Autenticadores.salvar_usuarios()
                return "Senha redefinada com sucesso!"
        return "Email não encontrado."

class configuracoesUsuario:
    def __init__(self, usuario_logado, usuarios):
        self.usuario_logado = usuario_logado
        self.usuarios = usuarios 

    def ver_dados(self):
        return {
            'email': self.usuario_logado.email,
            'nome': self.usuario_logado.nome,
            'senha': self.usuario_logado.senha
        }

    def atualizar_nome(self, novo_nome):
        if all(n.isalpha() or n.isspace() for n in novo_nome):
            self.usuario_logado.nome = novo_nome
            return True, "Nome atualizado com sucesso."
        return False, "Nome inválido. Use apenas letras."

    def atualizar_senha(self, nova_senha):
        if len(nova_senha) == 6 and nova_senha.isdigit():
            self.usuario_logado.senha = nova_senha
            return True, "Senha atualizada com sucesso."
        return False, "Senha inválida. Use exatamente 6 números."

    def salvar_usuarios(self, caminho="usuarios.json"):
        self.usuarios[self.usuario_logado.email] = self.usuario_logado.to_dict()
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump({'usuarios': self.usuarios}, arquivo, indent=4, ensure_ascii=False)

    def apagar_conta(self):
        if self.usuario_logado.email in self.usuarios:
            del self.usuarios[self.usuario_logado.email]
            self.salvar_usuarios()
            return True
        return False
    