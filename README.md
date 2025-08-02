# Sons da Terra
<img width="250" height="250" alt="Logo" src="https://github.com/user-attachments/assets/93c1324b-00fb-41c2-b0d2-bfc1f2673580" />

## 🎯 Sobre o projeto
A valorização da diversidade cultural e a promoção de espaços mais inclusivos no cenário artístico são demandas crescentes na sociedade contemporânea. Nesse contexto, a plataforma **Sons da Terra** surge com o propósito de fomentar a pluralidade cultural entre seus usuários e pôr artistas independentes em evidência.

## 🛠️ Tecnologias utilizadas

- **Linguagem**: Python
- **Bibliotecas**:
  - `random` — recomendações aleatórias e geração de códigos
  - `os` — manipulação de arquivos e diretórios
  - `json` — armazenamento de dados
  - `PySide6` — interface gráfica (GUI)
  - `smtplib` — envio de emails aos usuários por meio do protocolo SMTP.
    
## ✨ Release 1.0

- **RF001 - CRUD completo**  
  Criação, leitura, atualização e exclusão de contas de usuários.
  
- **RF002 - Avaliação de álbuns**  
  Usuários podem dar nota e deixar um comentário sobre os álbuns e EPs.
  
- **RF003 - Shout-boxd**  
  Área para a sugestão de álbuns e EPs que ainda não estão na plataforma.
  
## 🎧 Release 2.0
### Novas funcionalidades
- **RF004 - Recomendação de álbuns**  
  Recomendação aleatória de álbuns e EPs.
  
- **RF005 - Destaque da semana**  
  Toda semana um álbum diferente é escolhido como destaque.
  
- **RF006 - Interface gráfica com PySide6**  
  Experiência visual amigável e intuitiva.
### Melhorias
- **ENH01 - Substituição do banco de dados**  
  Os bancos de dados dos usuários agora estão em um arquivo `json`.
  
- **ENH02 - Refatorização e modularização do código**  
  Código inteiramente reorganizado/modularizado e atualizado para POO.
  
## ⏳ Release 3.0
### Novas funcionalidades
- **RF007 - Recuperação de senha**  
  Geração e envio de código por email.
- **RF008 - Ligação direta com o Spotify**  
  Agora o usuário pode ser redirecionado para um álbum específico no spotify sempre que desejar.
- **RF009 - Meus Shouts**  
  O usuário, sempre que desejar, pode verificar quais shous (sugestões) ele já deixou na plataforma.
- **RF010 - Criação de novas telas para organizar a interface gráfica**  
  As telas de recuperação, avaliação e shoutboxd foram adicionadas para uma melhor estruturação do código
### Melhorias
- **ENH02 - Interface gráfica**  
  Correção de bugs e refatoração completa de todas as telas.
- **ENH03 - Destaque da semana**  
  Agora a função destaque da semana exibe a capa do álbum e uma pequena descrição do artista.
- **ENH04 - Álbuns disponíveis**  
  Novos álbuns e EPs foram adicionados à plataforma.
- **ENH05 - Estruturação dos dados**  
  Todos os dados estão devidamente modularizados em arquvos `json`, não apenas os dados dos usuários.
- **ENH06 - Correção de bugs no armazenamento de avaliações e shouts**  
  Agora, os usuários podem deixar mais de uma avaliação/shout, o que antes não era possível devido a um erro ao salvar os dados.
- **ENH07 - Automatização no processo de atualização de dados dos álbuns/EPS**  
  Utilizamos a API do spotify para automatizar o processo que envolvia pegar o link e a capa do álbum, agora basta adicionar o nome e o artista responsável pelo álbum no arquivo `albuns.json` que, automaticamente, ele se atualiza com os novos dados.
## 📷 Imagens do Sons da Terra
- Tela inicial/tela de login:  
  <img width="521" height="562" alt="telaInicial_ST" src="https://github.com/user-attachments/assets/45ae748e-3c4a-4164-867f-5b02fc021e2d" />
- Menu principal:  
  <img width="986" height="539" alt="menuPrincipal_ST" src="https://github.com/user-attachments/assets/448ac8f1-088c-41f6-a8ff-7fe1696f6f5c" />
- Tela de avaliações dos álbuns:  
  <img width="959" height="617" alt="avaliacao_ST" src="https://github.com/user-attachments/assets/0a6a76ea-7d84-49a3-865c-140671477051" />
- Configurações:  
  <img width="519" height="499" alt="configuracoes_ST" src="https://github.com/user-attachments/assets/3bca8fce-3d54-4436-ba22-a5a6f8941b8f" />


## 👀 Conceitos:
### Funções de tratamento de strings
- Métodos usados para manipular textos:  
  `upper()`- Retorna a string com todas as suas letras maiúsculas;  
  `lower()`- Retorna a string com todas as suas letras minúsculas;  
  `strip()`- Remove espaçoes em branco na frente e ao final da string;  
  `title()`- Retorna a string com a primeira letra de cada palavra maiúscula;  
  `len()`- Retorna um valor inteiro com o número de caracteres de uma string.

### Estruturas de decisão e repetição
- Decisão: permitem executar diferentes blocos de código com base em condições.  
  `if` = se  
  `elif` = se não, se  
  `else` = se não

- Repetição: usados para repetir ações.  
  `while`: itera sobre um bloco de código enquanto uma determiada condição for verdadeira;  
  `for`: um valor x é variável e que recebe o valor do item dentro da sequência a cada nova iteração, até a sequência chegar ao fim. 

### Funções
- Definição: blocos de código reutilizáveis definidos por `def`, que podem receber parâmetros e retornar valores;

### Listas e dicionários
- Listas: coleções ordenadas de itens ([]), acessadas por índice.  
- Dicionários: coleções de pares chave-valor ({}), acessadas por chave.

### Conceitos de Programação Orientada a Objetos -POO-
- Definição: a Programação Orientada a Objetos (POO) é um paradigma que organiza o código em torno de objetos, que são instâncias das classes. Cada classe define atributos, que representam as características dos objetos, e métodos, que representam as ações que esses objetos podem realizar. Esse modelo permite maior organização, reutilização e manutenção do código. Também são usados conceitos como encapsulamento, que protege os dados internos dos objetos, herança, que permite que uma classe herde características de outra e polimorfismo, que permite que métodos com o mesmo nome se comportem de maneiras diferentes dependendo do contexto.

## 🧪 Como executar o projeto

1. Instale a biblioteca PySide6:
   ```bash
    pip install PySide6
2. Instale a biblioteca Spotipy:
   ```bash
   pip instal spotipy
4. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/sons-da-terra.git
5. Navegue até o diretório do projeto:
   ```bash
   cd sons-da-terra
6. Execute o arquivo:
   ```bash
   python main.py

## 📎 Documentação complementar

- [📄 Artigo Sons da Terra (PDF)](https://github.com/user-attachments/files/21420999/SonsdaTerra.pdf)
- [📌 Fluxograma do CRUD](https://drive.google.com/file/d/1LdmUFJJ50fUBIOtOuPOlCgfKJaNrkG8p/view?usp=drivesdk)
- [📌 Fluxograma das funcionalidades](https://drive.google.com/file/d/12JIuusqXzoGaLwlM3jDaPeVWD9sl-XUf/view?usp=sharing)

## 👩‍💻 Desenvolvedores

- Luiz Filipe F. Q. da Silva  
  [Github de Filipe](https://github.com/nilipe)
- Maria Eduarda A. dos Santos  
  [Github de Maria](https://github.com/mmaria-alves)
