import os
import random
import json
ARQUIVO_USUARIOS = "dados/usuarios.json"
ARQUIVO_SHOUTBOXD = "dados/shoutbox.json"
ARQUIVO_AVALIACOES = "dados/avaliações.json"
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

class Utils:
    def limpar_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

class Aunteticadores:
    def __init__(self, caminho_arquivo='dados/usuarios.json'):
        self.caminho_arquivo = caminho_arquivo
        self.usuarios = self.carregar_usuarios()
    
    def carregar_usuarios(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, 'r', encoding='UTF-8') as arquivo:
                return json.load(arquivo)
        return {}
        
    def salvar_usuarios(self):
        with open(self.caminho_arquivo, 'w', encoding='UTF-8') as arquivo:
            return json.dump(self.usuarios, arquivo, indent=4, ensure_ascii=False)

    def carregar_usuario(self, email):
        if email in self.usuarios:
            return Usuario.from_dict(self.usuarios[email])
        return None
    
    def login(self, email, senha):
        usuario = self.carregar_usuario(email)
        if usuario and usuario.senha == senha:
            return usuario
        return None
        

class Album:
    def __init__(self, album, artista):
        self.album = album
        self.artista = artista

    @staticmethod
    def from_dict(dados):
        return Album(dados['album'], dados['artista'])
        
    def to_dict(self):
        return {'album': self.album, 'artista': self.artista}
        
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


class sistemaDados:
    def __init__(self):
        self.usuarios = self.carregar_usuarios()
        self.usuario_logado = None

    def carregar_usuarios(self):
        if os.path.exists(ARQUIVO_USUARIOS):
            with open(ARQUIVO_USUARIOS, 'r', encoding='UTF-8') as arquivo:
                return json.load(arquivo)
        return {}
    
    def carregar_usuario(self, email):
        if email in self.usuarios:
            return Usuario.from_dict(self.usuarios[email])
        return None
    
    def salvar_usuarios(self):
        with open('usuarios.json', 'w', encoding='UTF-8') as arquivo:
            json.dump(self.usuarios, arquivo, indent=4, ensure_ascii=False)
    
    def cadastrar_usuario(self):
        # nome
        while True:
            nome = input('Qual é o seu nome? ').title().strip()
            if all(n.isalpha() or n.isspace() for n in nome):
                break
            else:
                print('Nome inválido. Utilize apenas letras.')
        # email
        while True:
            email = input('Qual é o seu email? ')
            if email in self.usuarios:
                print('Esse email já está sendo utilizado. Tente novamente')
            elif " " in email:
                print('Email inválido. Contém espaços.')
            elif "@" not in email:
                print('Email inválido. Não contém @.')
            elif not(email.endswith("gmail.com") or email.endswith("ufrpe.br")):
                print('Email inválido. Domínio inválido, deve terminar com "gmail.com" ou "ufrpe.br".')
            else:
                break
            # senha
            while True:
                senha = input('Digite sua senha: ')
                if len(senha) == 6 and senha.isdigit():
                    break
                else: 
                    print('Senha inválida. Deve conter apenas seis números.')
            # confirmação de senha
            while True:
                confirmacao_senha = input('Confirme sua senha: ')
                if confirmacao_senha == senha:
                    break
                else:
                    print('Confirmação de senha falhou. Tente novamente.')

            novo_usuario = Usuario(nome = nome, email = email, senha = senha)
            dados_usuario = novo_usuario.to_dict()

            self.usuarios[email] = dados_usuario
            self.salvar_usuarios()
            print('Cadastro realizado com sucesso!\n')

    def login(self, email, senha):
        while True:
            usuario = self.carregar_usuario(email)

            if usuario and usuario.senha == senha:
                print(f'Olá {usuario.nome}!')
                self.usuario_logado = usuario
                break
            else:
                return False
    
    def ver_dados(self):
        if not self.usuario_logado:
            print('Nenhum usuário logado.')
            return
        
        usuario = self.usuario_logado
        while True:
            print('-' * 20)
            print(f'Aqui estão os dados de {usuario.email}')
            print(f'Nome: {usuario.nome}')
            print(f'Senha: {usuario.senha}')
            print('-' * 20)
            sair = input('Pressione qualquer tecla para sair.')
            if sair == '':
                break
            else:
                break

    def atualizar_dados(self):
        if not self.usuario_logado:
            print('Nenhum usuário logado.')
            return
        
        usuario = self.usuario_logado
        senha = input('Confirme sua senha: ')
        if senha == usuario.senha:

            while True:
                print(' ---------------------------------- ')
                print('| Qual dado você deseja atualizar: |')
                print('| [1] Nome                         |')
                print('| [2] Senha                        |')
                print(' ---------------------------------  ')
                opcao = input('Escolha uma opção: ')

                if opcao == '1':
                    novo_nome = input('Digite o novo nome: ').title().strip()
                    if all(n.isalpha() or n.isspace() for n in novo_nome):
                        print('Nome atualizado com sucesso!')
                        break
                    else:
                        print('Nome inválido. Utilize apenas letras.')
                
                elif opcao == '2':
                    nova_senha = input('Digite sua nova senha: ')
                    if len(nova_senha) == 6 and nova_senha.isdigit():
                        print('Senha atualizada com sucesso!')
                        break
                    else:
                        print('Senha inválida. Sua senha deve conter apenas seis números')
                else: 
                    print('Opção inválida. Tente novamente.')
    
                self.usuario[usuario.email] = usuario.to_dict()
                self.salvar_usuarios()
    
    def apagar_dados(self):
        if not self.usuario_logado:
            print('Nenhum usuário logado.')
            return
        
        usuario = self.usuario_logado
        while True:
            confirmacao = input('Tem certeza que deseja deletar sua conta (s/n)? ')
            if confirmacao == 's':
                senha = input('Confirme sua senha: ')
                if senha == usuario.senha:
                    del usuario
                    self.salvar_usuarios()
                    print('Dados deletados com sucesso!')
                    break
                else:
                    print('Senha incorreta. Tente novamente.')
            elif confirmacao == 'n':
                print('Ok! Voltando para o menu.')
            else:
                print('Opção inválida. Digite apenas "s" se sim e "n" se não.')

class Avaliacao:
    def __init__(self, email, album, nota, comentario):
        self.email = email
        self.album = album
        self.nota = nota
        self.comentario = comentario

    @staticmethod
    def from_dict(dados):
        return Avaliacao(dados['email'], dados['album'], dados['nota'], dados['comentario'])
    
    def to_dict(self):
        return {'email': self.email, 
                'album': self.album, 
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
        
    def salvar_avaliacoes(self):
        with open(ARQUIVO_AVALIACOES, 'w', encoding='UTF-8') as arquivo:
            json.dump(self.avaliacoes, arquivo, indent=4, ensure_ascii=False)

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

class Shoutboxd:
    def __init__(self, email, album, artista):
        self.email = email
        self.album = album
        self.artista = artista

    @staticmethod
    def from_dict(dados):
        return Shoutboxd(dados['email'], dados['album'], dados['artista'])
    
    def to_dict(self):
        return {'email': self.email,
                'album': self.album,
                'artista': self.artista
        }

class sistemaShoutboxd:
    def __init__(self, usuario_logado, albuns_disponiveis):
        self.shouts = self.carregar_shoutboxd()
        self.usuario_logado = usuario_logado
        self.albuns_disponiveis = albuns_disponiveis

    def carregar_shoutboxd(self):
        if os.path.exists(ARQUIVO_SHOUTBOXD):
            with open(ARQUIVO_SHOUTBOXD, 'r', encoding='UTF-8') as arquivo:
                json.load(arquivo)
            return {}
    
    def salvar_shouts(self):
        with open(ARQUIVO_SHOUTBOXD, 'w', encoding='UTF-8') as arquivo:
            json.dump(self.shouts, arquivo, indent=4, ensure_ascii=False)

    def adicionar_shouts(self):
        email = self.usuario_logado.email if hasattr(self.usuario_logado, 'email') else self.usuario_logado.get('email')
        while True:
            print('Qual álbum você gostaria de ver no Sons da Terra? ')
            album_novo = input('Nome do álbum: ').strip()
            artista_novo = input('Nome do artista: ').strip()

            for a in self.albuns_disponiveis:
                if album_novo.lower() == a['album'].lower() and artista_novo.lower() == a['artista']:
                    print('Esse álbum já está disponível aqui!')
                    return


            shout = Shoutboxd(email, album_novo, artista_novo) 
            self.shouts[email] = shout.to_dict()
            self.salvar_shouts()
            print('Shout registrado com sucesso!')
            break  

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