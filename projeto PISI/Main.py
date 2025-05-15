import os
from validadores import (email_valido, nome_valido, senha_valida)
ARQUIVO_TXT = "usuarios.txt"


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
    with open(ARQUIVO_TXT, 'w') as arquivo:
        for usuario in usuarios:
            linha = f"{usuario['nome']}|{usuario['email']}|{usuario['senha']}\n"
            arquivo.write(linha)

def cadastrar_usuario(nome, email, senha, confirm_senha):
    usuarios = carregar_usuarios()

    if any(u['email'] == email for u in usuarios):
        return False, 'Este email já está cadastrado'  
    
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

def buscar_usuario(email):
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['email'] == email:
            return usuario
    return None

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
    return False, 'Email não encontrado.'

def deletar_usuario(email):
    usuarios = carregar_usuarios()
    usuarios = [u for u in usuarios if u['email'] != email]
    salvar_usuarios(usuarios)
    return len(usuarios) != len(carregar_usuarios())


def menu():
    while True:
        print("\n---- MENU ----")
        print("1. Cadastrar usuário")
        print("2. Visualizar dados")
        print("3. Atualizar dados")
        print("4. Deletar dados")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            confirm_senha = input('Confirme sua senha: ')
            sucesso, mensagem = cadastrar_usuario(nome, email, senha, confirm_senha)
            print(mensagem if sucesso else mensagem)
            
        elif opcao == "2":
            email = input("Digite o email: ")
            usuario = buscar_usuario(email)
            if usuario:
                print("\nDados do usuário:")
                print(f"Nome: {usuario['nome']}")
                print(f"Email: {usuario['email']}")
            else:
                print("Usuário não encontrado!")

        elif opcao == "3":
            email = input("Digite seu email: ")
            novo_nome = input("Novo nome (pressione Enter para manter): ")
            nova_senha = input("Nova senha (pressione Enter para manter): ")
            sucesso, mensagem = atualizar_usuario(email, novo_nome, nova_senha)
            print(mensagem if sucesso else mensagem)

        elif opcao == "4":
            email = input("Digite seu email: ")
            if deletar_usuario(email):
                print("Usuário removido com sucesso!")
            else:
                print("Falha ao remover: usuário não encontrado!")

        elif opcao == "5":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()