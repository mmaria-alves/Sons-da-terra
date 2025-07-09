import random
import os
import json
ARQUIVO_SHOUTBOX = "shoutbox.json"
ARQUIVO_AVALIACOES = "avaliacoes.json"
ARQUIVO_NOVIDADES = "novidades.json"

albuns_disponiveis = [
    {"nome": "Mundhana (2022)", "artista": "Mun-há"},
    {"nome": "Megalomania (2024)", "artista": "Uana"},
    {"nome": "Tanto pra dizer (2024)", "artista": "Mirela Hazin"},
    {"nome": "Coisas naturais (2025)", "artista": "Marina Sena"},
    {"nome": "Âmago (2024)", "artista": "Zendo"},
    {"nome": "Gambiarra chic pt.2 (2025)", "artista": "Irmãs de pau"},
    {"nome": "Grimestar (2024)", "artista": "Tremsete"},
    {"nome": "Jogo de Cintura (2024)", "artista": "Bell Puã"},
    {"nome": "Casa Coração (2025)", "artista": "Joyce Alane"},
    {"nome": "Bacuri (2024)", "artista": "Boogarins"},
    {"nome": "Abaixo de zero: Hello Hell (2019)", "artista": "Black alien"},
    {"nome": "KM2 (2025)", "artista": "Ebony"},
    {"nome": "Letrux como Mulher Girafa (2023)", "artista": "Letrux"},
    {"nome": "SIM SIM SIM (2022)", "artista": "Bala Desejo"},
    {"nome": "Me Chama de Gato Que Eu Sou Sua (2023)", "artista": "Ana Frango Elétrico"},
    {"nome": "o fim é um começo (2024)", "artista": "a terra vai se tornar um planeta inabitável"},
    {"nome": "MAU (2023)", "artista": "Jaloo"},
    {"nome": "Antiasfixiante (2024)", "artista": "Kinoa"},
    {"nome": "Quebra Asa, vol.1 (2023)", "artista": "Fernando motta"},
    {"nome": "Muganga (2023)", "artista": "IDLIBRA"}
]

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

def carregar_avaliacoes():
    if os.path.exists(ARQUIVO_AVALIACOES):
        with open(ARQUIVO_AVALIACOES, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return {}

def salvar_avaliacoes(avaliacoes):
    with open(ARQUIVO_AVALIACOES, 'w', encoding='utf-8') as arquivo:
        json.dump(avaliacoes, arquivo, indent=4, ensure_ascii=False)

def carregar_shoutbox(): ###
    if os.path.exists(ARQUIVO_SHOUTBOX):
        with open(ARQUIVO_SHOUTBOX, 'r', encoding='UTF-8') as arquivo:
            json.load(arquivo)
    return {}

def salvar_shouts(shouts): ###
    with open(ARQUIVO_SHOUTBOX, 'w', encoding='UTF-8') as arquivo:
        json.dump(shouts, arquivo, indent=4, ensure_ascii=False)

def avaliar_album(): ###
    global usuario_logado
    email = usuario_logado.get('email')

    avaliacoes = carregar_avaliacoes()
    print('Álbuns disponíveis: ')
    for i, album in enumerate(albuns_disponiveis):
       print(f'{i + 1}. {album['nome']} - {album['artista']}')
    opcao = input('Digite o número do álbum que você deseja avaliar (pressione "s" para sair): ').lower()
    
    while True:    
        if opcao == 's':
            break

        elif opcao.isdigit() and (1 <= int(opcao) <= len(albuns_disponiveis)):
            nota = input('Dê uma nota para esse álbum: ')
            if nota.isdigit():
                nota = float(nota)
                if nota < 0 or nota > 5:
                    print('Erro. Digite apenas números no intervalo de 0 até 5.')
                else: 
                    comentario = input('Deixe um comentário sobre o álbum: ')
                    if len(comentario) < 300:
                        break
                    else:
                        print('Ops, você atingiu o limite de 300 caracteres. Tente Novamente.')
            else: 
                print('Erro. Digite apenas números.')
        else:
            print('Número inválido. Tente novamente.')
    avaliacoes[email] = {
        'album': album,
        'nota': nota,
        'comentario': comentario
    }
    salvar_avaliacoes(avaliacoes)
    print('Avaliação registrada com sucesso!')

def mostrar():
    avaliacoes = carregar_avaliacoes()
    print("\nO que estão ouvindo agora:")

    if not avaliacoes:
        sugestoes = random.sample(albuns_disponiveis, k=min(3, len(albuns_disponiveis)))
        for album in sugestoes:
            print(f"- {album['nome']} by {album['artista']}")
    else:
        escolhas = random.sample(avaliacoes, k=min(3, len(avaliacoes)))
        for item in escolhas:
            print(f"- {item['album']} by {item['artista']} ({item['nota']}/5): \"{item['comentario']}\"")

def adicionar_shout():
    global usuario_logado
    email = usuario_logado.get('email')
    shouts = carregar_shoutbox()

    print('Qual álbum você gostaria de ver no Sons da Terra?')
    album = input('Nome do álbum: ')
    artista = input('Nome do artista: ')

    shouts[email] = {
        'album': album,
        'artista': artista
    }
    salvar_shouts(shouts)
    print('Sugestão adicionada!')
    