def email_valido(email):
    email = email.strip()
    if '@' in email and email.endswith('gmail.com') and " " not in email:
     return True
    else: 
       return False, 'Email inválido. Por favor, tente novamente.'

def senha_valida(senha):
    senha.strip()
    if " " not in senha and len(senha) == 6:
     return True
    else: 
       return False, 'Senha inválida. Por favor, insira uma nova senha'

def nome_valido(nome):
    nome.strip()
    if len(nome) <=25 and '  ' not in nome:
        return True
    else: 
       return False, 'Nome inválido. Por favor, insira outro nome'