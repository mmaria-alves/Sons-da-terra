import os
import random
import json

ARQUIVO_USUARIOS = "dados/usuarios.json"
ARQUIVO_SHOUTBOXD = "dados/shoutbox.json"
ARQUIVO_AVALIACOES = "dados/avaliações.json"
ARQUIVO_ALBUNS = "dados/albuns.json"

        

class Album:
    def __init__(self, nome, artista, spotify_id="", capa_url="", spotify_url="", descricao=""):
        self.nome = nome                  # Nome do álbum
        self.artista = artista            # Nome do artista
        self.capa_url = capa_url          # URL da imagem da capa
        self.spotify_url = spotify_url    # Link para abrir o álbum no Spotify
        self.descricao = descricao        # Descrição do artista adicionada manualmente ao JSON
    
    @staticmethod
    def from_dict(dados):
        return Album(
            nome=dados.get("nome_spotify", dados.get("nome", "")),
            artista=dados.get("artista_spotify", dados.get("artista", "")),
            capa_url=dados.get("capa", dados.get("capa_url", "")),
            spotify_url=dados.get("link", dados.get("spotify_url", "")),
            descricao=dados.get("descricao", "")
        )

    def to_dict(self):
        return {
            "nome_spotify": self.nome,
            "artista_spotify": self.artista,
            "capa": self.capa_url,
            "link": self.spotify_url,
            "descricao": self.descricao
        }
    
class gerenciarAlbuns:
    def __init__(self):
        self.albuns = self.carregar_albuns()

    def carregar_albuns(self):
        if os.path.exists(ARQUIVO_ALBUNS):
            with open(ARQUIVO_ALBUNS, 'r', encoding='UTF-8') as arquivo:
                dados = json.load(arquivo)
                return [Album.from_dict(album) for album in dados]
        return []
        
    def listar_albuns(self):
        for i, album in enumerate(self.albuns, 1):
           print(f'{i}. {album.nome} - {album.artista}')

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    @staticmethod
    def from_dict(dados):
        return Usuario(dados['nome'], dados['email'], dados['senha'])
    
    def to_dict(self):
        return {'nome': self.nome, 'email': self.email, 'senha': self.senha}

class Avaliacao:
    def __init__(self, email, nome_album, artista, nota, comentario):
        self.email = email
        self.nome_album = nome_album
        self.artista = artista
        self.nota = nota
        self.comentario = comentario

    @staticmethod
    def from_dict(dados):
        return Avaliacao(
            email=dados['email'], 
            nome_album=dados['nome_album'], 
            artista=dados['artista'],
            nota=dados['nota'], 
            comentario=dados['comentario']
            )
    
    def to_dict(self):
        return {
            'email': self.email, 
            'nome_album': self.nome_album,
            'artista': self.artista, 
            'nota': self.nota, 
            'comentario': self.comentario
        }

class sistemaAvaliacao:
    def __init__(self, usuario_logado, albuns_disponiveis):
        self.avaliacoes = self.carregar_avaliacoes()
        self.usuario_logado = usuario_logado
        self.albuns_disponiveis = albuns_disponiveis

    def carregar_avaliacoes(self):
        if os.path.exists(ARQUIVO_AVALIACOES):
            with open(ARQUIVO_AVALIACOES, 'r', encoding='UTF-8') as arquivo:
                return json.load(arquivo)
            return {}
        
    def salvar_avaliacoes(self, avaliacoes):
        with open(ARQUIVO_AVALIACOES, 'w', encoding='UTF-8') as arquivo:
            json.dump(avaliacoes, arquivo, indent=4, ensure_ascii=False)

    def salvar_avaliacao(self, email, nome_album, artista, nota, comentario):
        album = next((a for a in self.albuns_disponiveis
                      if a.nome == nome_album and a.artista == artista), None)
        
        if not album:
            raise ValueError("Álbum não encontrado")
        
        avaliacao = Avaliacao(email, album, nota, comentario)

        avaliacoes = self.carregar_avaliacoes()
        avaliacoes[email] = avaliacao.to_dict()
        self.salvar_avaliacoes(avaliacoes)

    def avaliar_album(self):
        gerenciar = gerenciarAlbuns
        email = self.usuario_logado.email if hasattr(self.usuario_logado, 'email') else self.usuario_logado.get('email')

        print('Álbuns disponíveis: ')
        gerenciar.listar_albuns(self)
        while True:
            opcao = input('\nDigite o número do álbum que deseja avaliar (ou "s" para sair): ').lower()
            if opcao == 's':
                break
            elif opcao.isdigit() and (1 <= int(opcao) <= len(self.albuns_disponiveis)):
                album_escolhido = self.albuns_disponiveis [int(opcao) - 1]

                nota = input('Dê uma nota para esse álbum (0-5): ')
                if not nota.replace('.', '', 1).isdigit():
                    print('Nota inválida. Digite um número.')
                    continue

                nota = float(nota)
                if nota < 0 or nota > 5:
                    print('Nota fora do intervalo permitido. Digite um número no intervalo permitido.')
                    continue

                comentario = input('Deixe um comentário (até 250 caracteres): ')
                if len(comentario) > 250:
                    print('Comentário muito longo. Não exceda o limite de caracteres.')
                    continue

                avaliacao = Avaliacao(email, album_escolhido, nota, comentario)
                self.avaliacoes[email] = avaliacao.to_dict()
                self.salvar_avaliacoes()
                print('Avaliação registrada com sucesso!')
                break
            else: 
                print('Opção inválida. Tente novamente.')

class Shout:
    def __init__(self, email, nome_album, artista):
        self.email = email
        self.nome_album = nome_album
        self.artista = artista

    def to_dict(self):
        return {
            "email": self.email,
            "nome_album": self.nome_album,
            "artista": self.artista
        }
    

class sistemaOuvindo:
    def __init__(self, caminho_avaliacoes=ARQUIVO_AVALIACOES, caminho_albuns=ARQUIVO_ALBUNS):
        self.caminho_avaliacoes = caminho_avaliacoes
        self.caminho_albuns = caminho_albuns
        self.avaliacoes = self.carregar_avaliacoes()
        self.albuns_disponiveis = self.carregar_albuns()

    def carregar_avaliacoes(self):
        if os.path.exists(self.caminho_avaliacoes):
            with open(self.caminho_avaliacoes, 'r', encoding='utf-8') as arquivo:
                return list(json.load(arquivo).values())
        return []
    
    def carregar_albuns(self):
        if os.path.exists(self.caminho_albuns):
            with open (self.caminho_albuns, 'r', encoding='UTF-8') as arquivo:
                return json.load(arquivo)
            return []
    
    def ouvindo_agora(self):
        if not self.avaliacoes:
            sugestoes = random.sample(self.albuns_disponiveis, k=min(3, len(self.albuns_disponiveis)))
            for album in sugestoes:
                print(f'- {album['album']} by {album['artista']}')
        else:
            escolha = random.sample(self.avaliacoes, k=min(3, len(self.avaliacoes)))
            for item in escolha:
                album = item.get('album')
                artista = item.get('artista')
                nota = item.get('nota')
                comentario = item.get('comentario')
                print(f'- {album} by {artista} | ({nota}/5): \"{comentario}\"')
