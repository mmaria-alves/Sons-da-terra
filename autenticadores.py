import os
import json

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