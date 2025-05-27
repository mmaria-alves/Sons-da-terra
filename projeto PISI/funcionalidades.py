import random
def menu():
    while True:
        print("\n🎵 Bem-vindo ao Sons da terra 🎵")
        print("1. avaliar")
        print("2. o que as pessoas estão ouvindo")
        print("3. shout-box")
        print("4. novidades")
        print("5. sair")

        opcao = input("Escolha uma opção (1-5): ")

        if opcao == '1':
            avaliar_album()
        elif opcao == '2':
            mostrar()
        elif opcao == '3':
            shout_box()
        elif opcao == '4':
            novidades()
        elif opcao == '5':
            print("Até a próxima!")
            break
        else:
            print(" Tente novamente.")

# Lista de álbuns disponíveis
albuns_disponiveis = [
    {"nome": "Mundhana (2022)", "artista": "Mun-há"},
    {"nome": "Megalomania (2024)", "artista": "Uana"},
    {"nome": "Tanto pra dizer (2024)", "artista": "Mirela Hazin"},
    {"nome": "Coisas naturais (2025)", "artista": "Marina Sena"},
    {"nome": "Gambiarra chic pt.2 (2025)", "artista": "Irmãs de pau"},
    {"nome": "Grimestar (2024)", "artista": "Tremsete"},
    {"nome": "Jogo de Cintura (2024)", "artista": "Bell Puã"},
    {"nome": "Bacuri (2024)", "artista": "Boogarins"},
    {"nome": "Abaixo de zero: Hello Hell (2019)", "artista": "Black alien"},
    {"nome": "KM2 (2025)", "artista": "Ebony"},
    {"nome": "SIM SIM SIM (2022)", "artista": "Bala Desejo"},
    {"nome": "Me Chama de Gato Que Eu Sou Sua (2023)", "artista": "Ana Frango Elétrico"},
    {"nome": "Muganga (2023)", "artista": "IDLIBRA"}
]

avaliacoes = []
shouts = []

def avaliar_album():
    print("\n Álbuns:")
    for i, album in enumerate(albuns_disponiveis):
        print(f"{i + 1}. {album['nome']} - {album['artista']}")

    try:
        escolha = int(input("Escolha o número do álbum que deseja avaliar: ")) - 1
        if escolha < 0 or escolha >= len(albuns_disponiveis):
            print("Número inválido. Tente novamente.")
            return

        nota = float(input("Dê uma nota de 0 a 5: ")) 
        if nota < 0 or nota > 5:
            print("Tente novamente.")
            return
        
        comentario = input("Deixe um comentário sobre o álbum: ")

        avaliacao = {
            "album": albuns_disponiveis[escolha]["nome"],
            "artista": albuns_disponiveis[escolha]["artista"],
            "nota": nota,
            "comentario": comentario
        }

        avaliacoes.append(avaliacao)
        print(" Avaliação registrada com sucesso!\n")

    except ValueError:
        print(" Tente novamente. Use números válidos.")

def mostrar():
    print("\n O que estão ouvindo agora:")

    if not avaliacoes:
        sugestoes = random.sample(albuns_disponiveis, k=min(3, len(albuns_disponiveis)))
        for album in sugestoes:
            print(f"- {album['nome']} by {album['artista']}")
    else:
        escolhas = random.sample(avaliacoes, k=min(3, len(avaliacoes)))
        for item in escolhas:
            print(f"- {item['album']} by {item['artista']} ({item['nota']}/5): \"{item['comentario']}\"")


def shout_box():
    print("\nQual álbum você gostaria de avaliar mas não está disponível?")
    sugestao = input("\nNome do álbum que você quer ver na plataforma: ")
    artista = input("\nNome do artista/banda: ")

    shout = {"album": sugestao, "artista": artista}
    shouts.append(shout)
    print(" Sugestão registrada! Obrigado por contribuir\n")


def novidades():
    print("\nAlbuns lançados recentemente:")

news = [
    {"nome": "Imagina (single)", "artista": "Barbarize feat. Oreia"},
    {"nome": "Tropical do brasil (single)", "artista": "Uana feat. Leoa"},
    {"nome": "Casa Coração (2024)", "artista": "Joyce Alane"},
    {"nome": "Coisas naturais (2025)", "artista": "Marina Sena"},
    {"nome": "Gambiarra chic pt.2 (2025)", "artista": "Irmãs de pau"},
    {"nome": "Dvd (single)", "artista": "Mirela Hazin"},
    {"nome": "KM2 (2025)", "artista": "Ebony"} 

]

avaliacoes = []
shouts = []

def novidades():
    print("\n Álbuns:")
    for i, album in enumerate(news):
        print(f"{i + 1}. {album['nome']} - {album['artista']}")

    try:
        escolha1 = int(input("Escolha o número do álbum que deseja avaliar: ")) - 1
        if escolha1 < 0 or escolha1 >= len(news):
            print("Número inválido. Tente novamente.")
            return

        nota1 = float(input("Dê uma nota de 0 a 5: ")) 
        if nota1 < 0 or nota1 > 5:
            print("Tente novamente.")
            return
        
        comentario1 = input("Deixe um comentário sobre o álbum: ")

        avaliacaobb = {
            "album": news[escolha1]["nome"],
            "artista": news[escolha1]["artista"],
            "nota": nota1,
            "comentario": comentario1
        }

        avaliacoes.append(avaliacaobb)
        print(" Avaliação registrada com sucesso!\n")

    except ValueError:
        print(" Tente novamente. Use números válidos.")

menu()
