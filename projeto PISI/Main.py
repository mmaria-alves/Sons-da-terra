# CRUD
import os
from validadores import *
ARQUIVO_TXT = "usuarios.txt"
ARQUIVO_TXT1 = "shoutbox.txt"
ARQUIVO_TXT2 = "avaliações.txt"
from requisitosFuncionais import menu_funcionalidades

def limpar_terminal():
    if os.name == 'nt':
       os.system('cls')
    else:
       os.system('clear')

# lê e carrega os dados no usuarios.txt
def carregar_usuarios():
    usuarios = []

    if os.path.exists(ARQUIVO_TXT):
        with open(ARQUIVO_TXT, 'r') as arquivo:
            for linha in arquivo:
                nome, email, senha = linha.strip().split('|')
                usuarios.append({"nome": nome, "email": email, "senha": senha})
    return usuarios

# salva os dados no .txt
def salvar_usuarios(usuarios):
    with open(ARQUIVO_TXT, 'a') as arquivo:
        for usuario in usuarios:
            linha = f"{usuario['nome']}|{usuario['email']}|{usuario['senha']}\n"
            arquivo.write(linha)

# cadastrar usuário
def cadastrar_usuario(nome, email, senha, confirm_senha):
    usuarios = carregar_usuarios()

    if any(usuario["email"] == email for usuario in usuarios):
        return False, 'Este email já está cadastrado.'  
    
    if not nome_valido(nome):
        return False, 'Nome inválido. Por favor, insira outro nome.'
    
    if not email_valido(email):
        return False, 'Email inválido. Por favor, tente novamente.'
    
    if not senha_valida(senha): 
        return False, 'Senha inválida. Por favor, insira uma nova senha.'
    
    if senha != confirm_senha:
        return False, 'As senhas não coincidem. Tente novamente.'


    usuarios.append({
        "nome": nome.strip(), 
        "email": email.strip(), 
        "senha": senha.strip()
    })
    
    salvar_usuarios(usuarios)
    return True, 'Cadastro realizado com sucesso!'

# ver usuários 
def ver_dados(email):
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['email'] == email:
            return usuario
    return False, 'Email não encontrado. Por favor, tente novamente.'


# atualizar dados
def atualizar_usuario(email, novo_nome, nova_senha):
    usuarios = carregar_usuarios()

    for usuario in usuarios:
        if usuario['email'] == email:
            if novo_nome.strip():
                if not nome_valido(novo_nome):
                    return False, 'Nome inválido. Por favor, insira um novo nome.'
            usuario['nome'] = novo_nome.strip()

            if nova_senha.strip():
                if not senha_valida(nova_senha):
                    return False, 'Senha inválida. Por favor, insira uma nova senha.'
            usuario['senha'] = nova_senha.strip()
            
            salvar_usuarios(usuarios)
            return True, 'Dados atualizados com sucesso.'
    return False, 'Email não encontrado. Por favor, tente novamente.'

# deletar dados
def deletar_dados(email):
    usuarios = carregar_usuarios()
    if any(u['email'] == email for u in usuarios): 
            usuarios = [u for u in usuarios if u['email'] != email] # exclui dados
            salvar_usuarios(usuarios)
            return True, 'Dados deletados com sucesso!'
    return False, 'Email não encontrado. Por favor, tente novamente.'


# menu de dados pessoais
def menu_dados():
    usuarios = carregar_usuarios()
    while True:
        print("\n --------- MENU --------- ")
        print("|1. Cadastrar usuário    |")
        print("|2. Visualizar dados     |")
        print("|3. Atualizar dados      |")
        print("|4. Deletar dados        |")
        print("|5. Sair                 |")
        print(" ------------------------ ")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha (apenas números): ")
            confirm_senha = input('Confirme sua senha: ')
            sucesso, mensagem = cadastrar_usuario(nome, email, senha, confirm_senha)
            print(mensagem if sucesso else mensagem)
            
        elif opcao == "2":
            email = input("Digite seu email: ")
            usuario = ver_dados(email)
            if usuario in usuarios:
                print("\nSeus dados:")
                print(f'Nome: {usuario['nome']}')
                print(f"Email: {usuario['email']}")
                print(f'Senha: {usuario['senha']}')
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            email = input("Digite seu email: ")
            novo_nome = input("Novo nome: ")
            nova_senha = input("Nova senha: ")
            sucesso, mensagem = atualizar_usuario(email, novo_nome, nova_senha)
            print(mensagem if sucesso else mensagem)

        elif opcao == "4":
            email = input('\nDigite seu email: ').strip()
            print('Tem certeza que deseja deletar sua conta? ')
            print('1. Sim')
            print('2. Não')

            escolha = input('Escolha uma opção: ')

            if escolha == "1":
                sucesso, mensagem = deletar_dados(email)
                print(mensagem if sucesso else mensagem)
                
                
            elif escolha == "2": 
                return menu_dados()

            else: 
                print('Opção inválida. Por favor, tente novamente.')
                return menu_dados()

        elif opcao == "5":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

def pag_inicial(): 
    while True: 
        print('\nBem vindo ao Sons da Terra. O que deseja fazer? ')
        print('1. Dados pessoais')
        print('2. Menu principal')
        print('3. Sair')

        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            menu_dados()
        elif opcao == '2':
            menu_funcionalidades()
        elif opcao == '3':
            print('\nAté a próxima!\n')
            limpar_terminal()
            break
        else:
            print('\nOpção inválida.')

if __name__ == "__main__":
    pag_inicial()