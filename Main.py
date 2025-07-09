import os
from requisitosFuncionais import menu_funcionalidades
import json
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_SHOUTBOX = "shoutbox.json"
ARQUIVO_AVALIACOES = "avaliações.json"

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='UTF-8') as arquivo:
            return json.load(arquivo)
    return {}

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='UTF-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

def carregar_dados_usuario(email):
    dados = carregar_usuarios()
    return dados.get('usuarios', {}).get(email)

usuario_logado = None

def cadastrar_usuarios(): ### 
    usuarios = carregar_usuarios()
    while True:
        nome = input('Qual é o seu nome? ').title().strip()
        if all(n.isalpha() or n.isspace() for n in nome):
            break
        else:
            print('Nome inválido. Utilize apenas letras')
    # email
    while True: 
        email = input('Digite seu email: ')
        if email in usuarios:
            print('Esse email já está sendo utilizado. Tente novamente.')
        elif " " in email:
            print('Email inválido. Contém espaços.')
        elif "@" not in email:
            print('Email inválido. Não contém @.')
        elif not (email.endswith('gmail.com') or email.endswith('ufrpe.com')):
            print('Email inválido. Domínio inválido, deve terminar "gmail.com" ou "ufrpe.br".')
        else:
            break
    # senha
    while True:
        senha = input('Digite sua senha: ')
        if len(senha) == 6 and senha.isdigit():
            break
        else:
            print('Senha inválida. Sua senha deve conter apenas seis números.')
    while True:
        tentativas = 3
        confirmacao_senha = input('Confirme sua senha: ')
        if confirmacao_senha == senha:
            break
        else:
            print('Confirmação de senha falhou. Tente novamente.')
    # idade
    while True:
        idade = input('Qual é a sua idade? ')
        if idade.isdigit():
            break
        else:
            print('Idade inválida. Utilize apenas números')

    usuarios[email] = {
        'nome': nome,
        'senha': senha,
        'idade': idade
    }

    salvar_usuarios(usuarios)
    print('Cadastro realizado com sucesso!')

def login(): ###
    global usuario_logado
    usuarios = carregar_usuarios()
    print('Bom te ver de novo!')
    email = input('Insira seu email: ')
    senha = input('Insira sua senha: ')
    usuario = carregar_dados_usuario(email)

    if (email in usuarios and usuarios[email]['senha'] == senha):
        print(f'Olá {usuarios[email]['nome']}')
        usuario_logado = usuario
    else: 
        print('Email ou senha inválidos. Tente novamente')


def ver_dados():
    global usuario_logado
    email = usuario_logado.get('email')
    nome = usuario_logado.get('nome')
    idade = usuario_logado.get('idade')
    senha = usuario_logado.get('senha')

    while True:
        print(f'Aqui estão os dados vinculado à {email}')
        print(f'Nome: {nome}')
        print(f'Idade: {idade}')
        print(f'Senha: {senha}')
        sair = input('Pressione qualquer tecla para sair')
        if sair == '':
            break
        else:
            break


def atualizar_dados(): ###
    global usuario_logado
    email = usuario_logado.get('email')
    senha = input('Confirme sua senha: ')
    if usuario_logado[email]['senha'] == senha:
    
        while True:
            print(' ---------------------------------- ')
            print('| Qual dado você deseja atualizar: |')
            print('| [1] Nome                         |')
            print('| [2] Senha                        |')
            print('| [3] Idade                        |')
            print(' ---------------------------------  ')
            opcao = input('Escolha uma opção (1/2): ')

            if opcao == '1':
                novo_nome = input('Novo nome: ').title().strip()
                if all(n.isalpha() or n.isspace() for n in novo_nome) and len(novo_nome) <= 25:
                    usuario_logado[email]['nome'] = novo_nome
                    salvar_usuarios()
                    print('Dados atualizados com sucesso.')
                    break
                else:
                    print('Nome inválido. Utilize apenas letras')
            
            elif opcao == '2':
                nova_senha = input('Nova senha: ')
                if len(nova_senha) == 6 and nova_senha.isdigit():
                    usuario_logado[email]['senha'] = nova_senha
                    salvar_usuarios()
                    print('Dados atualizados com sucesso!')
                    break
                else:
                    print('Senha incorreta. A senha deve ter seis números')
            
            elif opcao == '3':
                nova_idade = input('Nova idade: ')
                if nova_idade.isdigit():
                    usuario_logado[email]['idade']
                    salvar_usuarios()
                    break
                else:
                    print('Idade inválida. Digite apenas números.')
            else:
                print('Opção inválida. Tente Novamente')
    else:
        print('Senha incorreta. Tente novamente.')

def deletar_conta(): ###
    global usuario_logado
    while True:
        confirmacao = input('Tem certeza que deseja deletar sua conta (s/n)? ')
        if confirmacao == 's':
            senha = input('Confirme sua senha: ')
            if senha == usuario_logado.get('senha'):
                del usuario_logado
                salvar_usuarios()
                print('Dados deletados com sucesso!')
                break
        elif confirmacao == 'n':
            print('Ok! Voltando...')
            break
        else:
            print('Opção inválida. Digite apenas "s" ou "n".')


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
            cadastrar_usuarios()
            
        elif opcao == "2":
            ver_dados()

        elif opcao == "3":
            atualizar_dados()

        elif opcao == "4":
            email = input('\nDigite seu email: ').strip()
            print('Tem certeza que deseja deletar sua conta? ')
            print('1. Sim')
            print('2. Não')

            escolha = input('Escolha uma opção: ')

            if escolha == "1":
                sucesso, mensagem = deletar_conta(email)
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