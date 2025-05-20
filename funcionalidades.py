# projeto-PISI
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
            mostrar_ouvindo()
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
    {"nome": "Mundhana", "artista": "Mun-há"},
    {"nome": "Megalomania", "artista": "Uana"},
    {"nome": "Tanto pra dizer", "artista": "Mirela Hazin"},
    {"nome": "Coisas naturais", "artista": "Marina Sena"},
    {"nome": "Gambiarra chic", "artista": "Irmãs de pau"}
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

def mostrar_ouvindo():
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
    sugestao = input("\nNome do álbum que você quer: ")
    artista = input("\nNome do artista/banda: ")

    shout = {"album": sugestao, "artista": artista}
    shouts.append(shout)
    print(" Sugestão registrada! Obrigado por contribuir\n")


def novidades():
    print("\nAlbuns lançados recentemente:")

    if not avaliacoes:
        sugestoes = random.sample(albuns_disponiveis, k=min(3, len(albuns_disponiveis)))
        for album in sugestoes:
            print(f"- {album['nome']} by {album['artista']}")
    else:
        escolhas = random.sample(avaliacoes, k=min(3, len(avaliacoes)))
        for item in escolhas:
            print(f"- {item['album']} by {item['artista']} ({item['nota']}/5): \"{item['comentario']}\"")

menu()
