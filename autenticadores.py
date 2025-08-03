import os
import json
import random
import smtplib
import spotipy
from urllib.request import urlopen
from spotipy.oauth2 import SpotifyClientCredentials
from PySide6.QtGui import QPixmap
from datetime import datetime, timedelta, date
from pathlib import Path
from email.message import EmailMessage
from sistemas import Avaliacao, sistemaAvaliacao, sistemaOuvindo, Album, Shout

EMAIL_REMETENTE = 'noreply.sonsdaterra@gmail.com'
SENHA_REMETENTE = 'pppd jwml xftl uwxb'

ARQUIVO_ALBUNS = "dados/albuns.json"
CLIENTE_ID="245d8233453d4e1ca80e73e160fdb42b"
CLIENT_SECRET="f56d813be60b4416b0ba4b35830e74dd"

class Usuario:
    def __init__(self, nome, email, senha,):
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
    def from_dict(dados):
        return Usuario(dados['nome'], dados['email'], dados['senha'])
    
    def to_dict(self):
        return {'nome': self.nome, 'email': self.email, 'senha': self.senha, "tempo": "", "codigo": ""}


class Autenticadores:
    def __init__(self, caminho_arquivo="dados/usuarios.json"):
        self.caminho_arquivo = caminho_arquivo
        self.usuarios = self.carregar_usuarios()
        self.usuario_logado = None
        self.albuns_disponiveis = self.carregar_albuns()
    @staticmethod
    def carregar_usuarios():
        caminho_arquivo = 'dados/usuarios.json'
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        return {}
    @staticmethod
    def salvar_usuarios(usuarios):
        caminho_arquivo = 'dados/usuarios.json'
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    
    def carregar_usuario(self, email):
        if email in self.usuarios:
            return Usuario.from_dict(self.usuarios[email])
        return None
    
    def carregar_albuns(self, caminho="dados/albuns.json"):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        
        self.albuns_disponiveis = [Album.from_dict(album) for album in dados]
        return self.albuns_disponiveis

       
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

    
    def ouvindo_agora_terminal(self):
        sistema = sistemaOuvindo()
        sistema.ouvindo_agora()
        
    def destaque_da_semana(self, caminho='dados/destaque.json'):
        hoje = date.today()
        semana_atual = hoje.isocalendar()[1]
    
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                if dados.get('semana') == semana_atual:
                    return Album.from_dict(dados['album'])
                
        destaque = random.choice(self.albuns_disponiveis)
        
        resultado = {
            'semana': semana_atual,
            'album': destaque.__dict__
        }

        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(resultado, arquivo, ensure_ascii=False, indent=4)
        
        return destaque
    
    def carregar_capa(self):
        try:
            destaque_info = self.destaque_da_semana()
            album_destaque = destaque_info['album']

            caminho_imagem = album_destaque['capa'][0]

            if not os.path.exists(caminho_imagem):
                script_dir = Path(__file__).parent
                caminho_completo = script_dir / caminho_imagem

                if caminho_completo.exists():
                    caminho_imagem = str(caminho_completo)
                else:
                    raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")
            
            return caminho_imagem
        except (KeyError, IndexError, FileNotFoundError) as e:
            print(f"Erro ao carregar capa do álbum: {e}")
    
    @staticmethod
    def carregar_pixmap(url: str):
        try:
            with urlopen(url) as resposta:
                dados = resposta.read()
                pixmap = QPixmap()
                pixmap.loadFromData(dados)
                return pixmap
        except Exception as erro:
            print(f"Erro ao carregar imagem: {erro}")
            return QPixmap()
    
    def info_completa_album(self):
        try:
            destaque_info = self.destaque_da_semana()
            album = destaque_info['album']

            return {
                'semana': destaque_info['semana'],
                'nome': album['nome'],
                'artista': album['artista'],
                'capa': self.carregar_capa(),
                'album_completo': album
            }
        except Exception as e:
            print(f'Erro ao obter informações do destaque da semana: {e}')
            return None
            
    @staticmethod
    def enviar_codigo(destinatario, codigo):
        mensagem = EmailMessage()
        mensagem['Subject'] = 'Recuperação de Senha'
        mensagem['From'] = EMAIL_REMETENTE
        mensagem['To'] = destinatario
        mensagem.set_content(f'''
Olá!
Seu código de verificação é {codigo}

Este código é válido por 10 minutos
Se você não tentou fazer login, ignore este e-mail.

Atenciosamente,
Sons da Terra
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
    def solicitar_codigo(email):
        usuarios = Autenticadores.carregar_usuarios()
        for dados in usuarios.values():
            if dados["email"] == email:
                codigo = random.randint(100000, 999999)
                codigo = str(codigo)
                tempo = (datetime.now() + timedelta(minutes=10)).isoformat()

                dados['codigo'] = codigo
                dados['tempo'] = tempo
                Autenticadores.salvar_usuarios(usuarios)

                enviado = Autenticadores.enviar_codigo(email, codigo)
                return enviado
        return False
    
    @staticmethod
    def validar_codigo(email_usuario, codigo_digitado, nova_senha):
        usuarios = Autenticadores.carregar_usuarios()
        for dados in usuarios.values():
            if dados['email'] == email_usuario:
                if dados['codigo'] != codigo_digitado:
                    return 'Código inválido'
                if datetime.now() > datetime.fromisoformat(dados['tempo']):
                    return 'Código expirado'
                
                dados['senha'] = nova_senha
                dados['codigo'] = ''
                dados['tempo'] = ''
                Autenticadores.salvar_usuarios(usuarios)
                return "Senha redefinada com sucesso!"
        return "Email não encontrado."
    
    def carregar_avaliacoes(self, caminho="dados/avaliações.json"):
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='UTF-8') as arquivo:
                return json.load(arquivo)
            return {}
        
    def salvar_avaliacoes(self, avaliacoes,caminho="dados/avaliações.json"):
        with open(caminho, 'w', encoding='UTF-8') as arquivo:
            json.dump(avaliacoes, arquivo, indent=4, ensure_ascii=False)

    def salvar_avaliacao(self, email, nome_album, artista, nota, comentario):
        album = next((a for a in self.albuns_disponiveis
                      if a.nome == nome_album and a.artista == artista), None)
        
        if not album:
            raise ValueError("Álbum não encontrado")
        
        avaliacao = Avaliacao(email, album.nome, album.artista, nota, comentario)
        avaliacoes = self.carregar_avaliacoes()
        if email not in avaliacoes:
            avaliacoes[email] = []
        
        avaliacoes[email].append(avaliacao.to_dict())
        
        self.salvar_avaliacoes(avaliacoes)

    def carregar_shouts(self):
        caminho="dados/shoutbox.json"
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
            return {}
        
    def salvar_shouts(self, shouts):
        caminho="dados/shoutbox.json"
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            return json.dump(shouts, arquivo, indent=4, ensure_ascii=False)
        
    def adicionar_shout(self, email, nome_album, artista):
        shout = Shout(email, nome_album, artista)
        shouts = self.carregar_shouts()

        if email not in shouts:
            shouts[email] = []
        
        shouts[email].append(shout.to_dict())
        self.salvar_shouts(shouts)

    def obter_shouts_usuario(self, email):
        shouts = self.carregar_shouts()
        return shouts.get(email, [])
    
    def ouvindo_agora(self):
        caminho = "dados/avaliações.json"
        if not os.path.exists(caminho):
            return []

        with open(caminho, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        avaliacoes = []

        for lista_avaliacoes in dados.values():
            if isinstance(lista_avaliacoes, dict):
                lista_avaliacoes = [lista_avaliacoes]
            for a in lista_avaliacoes:
                avaliacoes.append(Avaliacao.from_dict(a))

        return random.sample(avaliacoes, k=min(2, len(avaliacoes)))


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

    def salvar_usuarios(self, caminho="dados/usuarios.json"):
        self.usuarios[self.usuario_logado.email] = self.usuario_logado.to_dict()
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(self.usuarios, arquivo, indent=4, ensure_ascii=False)

    def apagar_conta(self):
        if self.usuario_logado.email in self.usuarios:
            del self.usuarios[self.usuario_logado.email]
            self.salvar_usuarios()
            return True
        return False
    

class AtualizadorSpotify:
    '''Utilizado para atualizar o arquivo json com as informações dos nomes corretos, imagem da capa e link do álbum/EPs'''
    def __init__(self, caminho_arquivo: str, client_id: str, client_secret: str):
        self.caminho_arquivo = caminho_arquivo
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))
        self.albuns = []

    def carregar_arquivo(self):
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                self.albuns = json.load(f)
        except FileNotFoundError:
            print("Arquivo não encontrado.")
        except json.JSONDecodeError:
            print("Erro ao ler o JSON.")

    def buscar_dados_album(self, nome_album: str, artista: str):
        resultado = self.sp.search(q=f"album:{nome_album} artist:{artista}", type="album", limit=1)
        items = resultado.get("albums", {}).get("items", [])
        if items:
            info = items[0]
            return {
                "nome_spotify": info["name"],
                "artista_spotify": ", ".join([a["name"] for a in info["artists"]]),
                "link": info["external_urls"]["spotify"],
                "capa": info["images"][0]["url"] if info["images"] else None
            }
        else:
            return {"erro": "Álbum não encontrado"}

    def atualizar_albuns(self):
        for album in self.albuns:
            nome = album.get("nome")
            artista = album.get("artista")
            dados = self.buscar_dados_album(nome, artista)
            album.update(dados)

    def salvar_arquivo(self):
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(self.albuns, f, indent=4, ensure_ascii=False)
        print("Arquivo atualizado com sucesso.")

    def executar(self):
        self.carregar_arquivo()
        if self.albuns:
            self.atualizar_albuns()
            self.salvar_arquivo()

# Só executar este arquivo quando for necessário atualizar os álbuns
if __name__ == "__main__":
    atualizador = AtualizadorSpotify(
        caminho_arquivo="dados/albuns.json",
        client_id=CLIENTE_ID,
        client_secret=CLIENT_SECRET
    )
    atualizador.executar()