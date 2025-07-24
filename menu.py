from sistemas import sistemaDados, Utils
import time

class Menu():
    def __init__(self, sistema):
        self.sistema = sistema

    def exibir(self):
        raise NotImplementedError('Erro. As subclasses devem implementar esse método.')
    
class menuInicial(Menu):
    sistema = sistemaDados
    def exibir(self):
        print('Bem vindo(a) ao Sons da Terra!')
        while True:
            opcao = input('Você já tem uma conta? (s/n) ou digite "sair" para sair: ').lower()
            if opcao == 'n':
                self.sistema.cadastrar_usuario()
            elif opcao == 's':
                self.sistema.login()
                menuPrincipal.exibir()
            elif opcao == 'sair':
                print('Até a próxima. Saindo...')
                time.sleep(1.5)
                Utils.limpar_terminal()
            else:
                print('opção inválida. Digite apenas "s", "n" ou "sair".')

class menuConfiguracoes(Menu):
    sistema = sistemaDados
    def exibir(self):
        while True:
            print("\n ------------ Configurações ----------- ")
            print("| 1. Visualizar dados                  |")
            print("| 2. Atualizar dados                   |")
            print("| 3. Deletar dados                     |")
            print("| Pressione Enter para voltar          |")
            print(" -------------------------------------- ")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.sistema.ver_dados()
            elif opcao == '2':
                self.sistema.atualizar_dados()
            elif opcao == '3':
                self.sistema.apagar_dados()
            elif opcao == '':
                break
            else:
                print('Opção inválida. Tente Novamente.')
            
class menuPrincipal(Menu):
    def exibir(self):
        while True:
            print(' ----------------- MENU ------------------ ')
            print('| 1. Avaliar                               |')
            print('| 2. Shout-Box                             |')
            print('| 3. O que as pessoas estão ouvindo?       |')
            print('| 4. Novidades                             |')
            print('| 5. Configurações                         |')
            print('| Pressione ENTER para sair                |')
            print(' ------------------------------------------ ')
            opcao = input('O que deseja fazer? ')

            if opcao == '1':
                pass
            elif opcao == '2':
                pass
            elif opcao == '3':
                pass
            elif opcao == '4':
                pass
            elif opcao == '5':
                menuConfiguracoes.exibir()
            elif opcao == '':
                print('Foi bom te ver por aqui!')

                break
            else:
                print('opção inválida. Digite apenas números de 1-5 ou pressione ENTER.')

if __name__ == '__main__':
    menu = menuInicial(Menu)
    menu.exibir()