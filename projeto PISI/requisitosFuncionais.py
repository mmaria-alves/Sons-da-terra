import random
import os
ARQUIVO_TXT1 = 'shoutbox.txt'
ARQUIVO_TXT2 = "avaliacoes.txt"

# avaliações
def carregar_avaliacoes():
    avaliacoes = []
    if os.path.exists(ARQUIVO_TXT2):
        with open(ARQUIVO_TXT2, 'r') as arquivo:
            for linha in arquivo:
                album, artista, nota, comentário = linha.strip().split('|')
                avaliacoes.append({'álbum': album, 'artista': artista, 
                               'nota': nota,'comentário': comentário})
        return avaliacoes
    
def salvar_avaliacoes(avaliacoes):
    with open(ARQUIVO_TXT2, 'w') as arquivo:
        for avaliacao in avaliacoes:
            linha = f"{avaliacao['album']}|{avaliacao['artista']}|{avaliacao['nota']}|{avaliacao['comentario']}\n"
            arquivo.write(linha)

# shoutbox
def carregar_shouts():
   shouts = []
   if os.path.exists(ARQUIVO_TXT1):
    with open(ARQUIVO_TXT1, 'r') as arquivo:
       for linha in arquivo:
            album, artista = linha.strip().split('|')
            shouts.append({'álbum': album, 'artista': artista})
    return shouts

def salvar_shouts(shouts):
    with open(ARQUIVO_TXT1, 'w') as arquivo:
        for shout in shouts:
            linha = f"{shout['album']}|{shout['artista']}\n"
            arquivo.write(linha)
            
# menu: funcionalidades
def menu_funcionalidades():
    while True:
        print("\n🎵 Sons da terra 🎵")
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
            print("Tente novamente.")

# Lista de álbuns disponíveis
albuns_disponiveis = [
    {"nome": "Mundhana (2022)", "artista": "Mun-há", "sobre": "Artista independente pernambucana, travesti e dona de uma energia incrivel. MUn-ha é Conhecida como a “Não-binária” do brega, esse albúm reforça sua identidade e força na cena. "},
    {"nome": "Megalomania (2024)", "artista": "Uana", "sobre": "Artista pernambucana explora as variedades sonoras de seu território e se define como o “pop pernambucano”. Megalomania vai do brega-funk ao house em disco e tem participação de Rachel Reis e Mago de Tarso"},
    {"nome": "Tanto pra dizer (2024)", "artista": "Mirela Hazin", "sobre": "Artista recifense nesse albúm a cantora relata desilusões amorosas, sentimentos que surgiram na transição da adolescência para o começo da fase universitária. "},
    {"nome": "Coisas naturais (2025)", "artista": "Marina Sena", "sobre": "Artista mineira, participou de 2 bandas e com esse disco, composto de maneira autoral, se consolida como uma das grandes novas vozes da geração."},
    {"nome": "Âmago (2024)", "artista": "Zendo", "sobre": "Artista recifense chama atenção por sua identidade visual ousada, sensual e composições sensíveis."},
    {"nome": "Gambiarra chic pt.2 (2025)", "artista": "Irmãs de pau", "sobre": "Dupla de funkeiras que ousam e subvertem padrões em seus próprios termos. Esse albúm é a continuaçao de um projeto que descreve vivência periférica, autonomia e estética com som iconico das artistas, mesclam funk ao drill."},
    {"nome": "Grimestar (2024)", "artista": "Tremsete, Zoebeats", "sobre": "Trem7 e Zoe sentiram uma grande conexão musical assim criaram esse EP, eles ja haviam colaborado em outro projeto do Zoebeats “Destalado”."},
    {"nome": "Jogo de Cintura (2024)", "artista": "Bell Puã", "sobre": "Poetisa usa os seus versos rasgados para escancarar a realidade das minorias sociais e bradar a resistência das mulheres negras, dos negros, dos periféricos. "},
    {"nome": "Casa Coração (2025)", "artista": "Joyce Alane", "sobre": "Joyce Alane é uma cantora e compositora pernambucana da nova cena musical. Joyce vem expandindo o seu público, levando o Nordeste consigo e ocupando seu espaço em âmbito nacional."},
    {"nome": "Bacuri (2024)", "artista": "Boogarins", "sobre": "Banda goiana composta por 4 integrantes possui uma discografia inovadora e ciclica nas inventivas. “BACURI” é o projeto que marca um retorno às raízes criativas por ser gravado inteiramente em casa."},
    {"nome": "Abaixo de zero: Hello Hell (2019)", "artista": "Black alien", "sobre": " Rapper brasileiro conhecido pelo trabalho provocador com o músico Speed Freaks (1972-2010) e a banda Planet Hemp. Apresenta estilo único, com rima rápida em inglês e português. "},
    {"nome": "KM2 (2025)", "artista": "Ebony", "sobre": "Um dos maiores nomes femininos do cenário urbano. O albúm soa muito mais pessoal e amadurecido, até mesmo como uma conversa casual."},
    {"nome": "Letrux como Mulher Girafa (2023)", "artista": "Letrux", "sobre": "Cantora, compositora, poeta e atriz carioca. Tem três álbuns lançados. "},
    {"nome": "SIM SIM SIM (2022)", "artista": "Bala Desejo", "sobre": "Quarteto formado por Dora Morelenbaum, Julia Mestre, Lucas Nunes e Zé Ibarra. União de quatro forças que já aconteciam e colaboraram na criação desse albúm"},
    {"nome": "Me Chama de Gato Que Eu Sou Sua (2023)", "artista": "Ana Frango Elétrico", "sobre": "Cantora, compositora, multiinstrumentista, produtora, poetisa e artista visual brasileira. "},
    {"nome": "o fim é um começo (2024)", "artista": "a terra vai se tornar um planeta inabitável", "sobre": "Projeto músical de música experimental e brasileira. Esse albúm assim como os outros retrata por meio de musicas melancolicas temas como fim do mundo, relacionamento e despedidas. "},
    {"nome": "MAU (2023)", "artista": "Jaloo", "sobre": "A artista paraense e trans é um dos nomes mais relevantes do pop brasileiro. Esse album foi inteiramente produzido e composta somente por ela, onde é nitido sua identidade musical. "},
    {"nome": "Antiasfixiante (2024)", "artista": "Kinoa", "sobre": "Banda de São Lourenço da Mata. O “Antiasfixiante” mistura sonoridades enérgicas e rebeldes do punk até momentos íntimos e emocionais que puxam pro indie rock, tudo isso unido a um carisma enorme e uma presença lírica muito destacável. "},
    {"nome": "Quebra Asa, vol.1 (2023)", "artista": "Fernando motta", "sobre": "Movimento algum representa a força e o sentimento que uma música tem por si só. São letras que não se localizam num espaço/tempo específicos, mas que encontram correspondência no que nos emociona e nos instiga. "},
    {"nome": "Muganga (2023)", "artista": "IDLIBRA", "sobre": "Artista pernambucana Libra Lima, a Idlibra, apresenta um repertório de cinco faixas que abraça a estranheza e utiliza da inusitada combinação de elementos como estímulo para brincar com a interpretação do ouvinte. "}
    
]

def avaliar_album():
    avaliacoes = carregar_avaliacoes()
    print("\nÁlbuns:")
    for i, album in enumerate(albuns_disponiveis):
        print(f"{i + 1}. {album['nome']} - {album['artista']}")
    
    try:
        escolha = int(input('Escolha o número do álbum que deseja avaliar (digite "sair" caso deseje retornar): '))- 1
        if escolha < 0 or escolha >= len(albuns_disponiveis):
            print("Número inválido. Tente novamente.")
            return
        
        nota = float(input('Dê uma nota de 0 a 5 (digite "sair" caso deseje retornar): ')) 
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
        salvar_avaliacoes(avaliacoes)
        print("Avaliação registrada com sucesso!\n")

    except ValueError:
        print("Tente novamente. Use números válidos.")

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


def shout_box():
    shouts = carregar_shouts()
    print("\nQual álbum você gostaria de avaliar mas não está disponível?")
    sugestao = input("\nNome do álbum que você quer ver na plataforma: ")
    artista = input("\nNome do artista/banda: ")

    shout = {"album": sugestao, "artista": artista}
    shouts.append(shout)
    salvar_shouts(shouts)
    print("Sugestão registrada! Obrigado por contribuir\n")


def novidades():
    print("\nÁlbuns lançados recentemente:")

news = [
    {"nome": "Movimento algum (NOVO)", "artista": "Fernando motta"},
    {"nome": "Imagina (single)", "artista": "Barbarize feat. Oreia"},
    {"nome": "Tropical do brasil (single)", "artista": "Uana feat. Leoa"},
    {"nome": "Casa Coração (2025)", "artista": "Joyce Alane"},
    {"nome": "Coisas naturais (2025)", "artista": "Marina Sena"},
    {"nome": "Gambiarra chic pt.2 (2025)", "artista": "Irmãs de pau"},
    {"nome": "Dvd (single)", "artista": "Mirela Hazin"},
    {"nome": "KM2 (2025)", "artista": "Ebony"} 

]

def avaliar_novidades():
    avaliacoes = carregar_avaliacoes()
    print("\nÁlbuns:")
    for i, album in enumerate(news):
        print(f"{i + 1}. {album['nome']} - {album['artista']}")

    try:
        escolhabb = int(input('Escolha o número do álbum que deseja avaliar: (digite "sair" caso deseje retornar)'))- 1
        if escolhabb < 0 or escolhabb >= len(news):
            print("Número inválido. Tente novamente.")
            return
        
        nota1 = float(input('Dê uma nota de 0 a 5: (digite "sair" caso deseje retornar) ')) 
        if nota1 < 0 or nota1 > 5:
            print("Tente novamente.")
            return

        
        comentario1 = input("Deixe um comentário sobre o álbum: ")
       
        avaliacaobb = {
            "album": news[escolhabb]["nome"],
            "artista": news[escolhabb]["artista"],
            "nota": nota1,
            "comentario": comentario1
        }

        avaliacoes.append(avaliacaobb)
        salvar_avaliacoes(avaliacoes)
        print("Avaliação registrada com sucesso!\n")

    except ValueError:
        print("Tente novamente. Use números válidos.")
