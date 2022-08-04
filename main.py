#FÁBRICA DE SOFTWARE
#TRABALHO DO GRUPO 2 - TIME COLOSSUS
#INTEGRANTES DO GRUPO:ERICK JACQUES REGERT, LUCAS ROBERTO HAETINGER E MATHEUS HENRIQUE SEHN

import time #conta o tempo para executar algo na sequência (ex: time.sleep(segundos))
import random #no nosso código, utilizamos dessa lib para escolher aleatoriamente uma das 4 cores

#puxa os arquivos e suas funcionalidades
from lista_encadeada import ListaEncadeada
from registro_ranking import RegistroRanking


#define a lista do bot(gabarito) e lista do player(inseridas)
lista_player = ListaEncadeada()
lista_bot = ListaEncadeada()

ranking_list = [] #Lista para armazenar o ranking, trabalha com o arquivo .txt

cores = ["Vermelho", "Verde", "Amarelo", "Azul"] # Lista de cores
cores_formatadas = ["\033[31mVermelho\033[m" # Lista das cores formatadas
                    , "\033[32mVerde\033[m"
                    , "\033[33mAmarelo\033[m"
                    , "\033[34mAzul\033[m"]

# Método para gerar a string GENIUS colorida, cada letra com uma cor => estético
def GENIUS_colorido():
    return '\033[31m' + 'G' + \
           '\033[32m' + 'E' + \
           '\033[33m' + 'N' + \
           '\033[34m' + 'I' + \
           '\033[35m' + 'U' + \
           '\033[36m' + 'S' + '\033[m'

# Método para "limpar" terminal
def limpa_terminal():
    print('\n' * 50)


# Método para gerenciar o menu principal
def menu_principal():
    print(GENIUS_colorido())
    print('Selecione uma opção: ')
    print('[0] Sair\n[1] Jogar\n[2] Tutorial\n[3] Ranking')

    # Le a opção escolhida pelo usuário
    escolha_menu = input()
    limpa_terminal()

    # Verificar a opção digitada pelo usuário
    if escolha_menu == '0':
        exit()
    elif escolha_menu == '1':
        jogar()
    elif escolha_menu == '2':
        tutorial()
    elif escolha_menu == '3':
        ranking()
    else:
        print('Entrada inválida')

# Método responsável pela lógica do jogo
def jogar():
    continuar = True
    while continuar:
        # Mostrar contagem regresiva na primeira rodada 
        if lista_bot.tamanho() == 0:
            for i in range(3, 0, -1):
                limpa_terminal()
                print('Iniciando em {}'.format(i))
                time.sleep(1)

        # Gerar uma nova cor aleatória
        adiciona_cor()
        
        # Exibir as cores uma após a outra
        aux = lista_bot.primeiro
        while aux is not None:
            cor_index = aux.valor
            limpa_terminal()
            time.sleep(0.5)
            print(get_cor_formatada(cor_index))
            time.sleep(1)
            aux = aux.proximo

        limpa_terminal()
        print('[1] Vermelho | [2] Verde | [3] Amarelo | [4] Azul')

        # Limpa a lista de jogadas do usuário
        lista_player.limpar_lista()

        # Percorer a lista das cores geradas
        i = 1
        aux = lista_bot.primeiro
        while aux is not None:
            # Aguardar o usuário informar uma cor válida
            cor_informada = aguarda_entrada_valida(' - Digite a {}ª cor da sequência: '.format(i)
                                                   , ['vermelho', 'verde', 'amarelo', 'azul', '1', '2', '3', '4']
                                                   , 'Cor informada é inválida'
                                                   , ingore_case=True)

            # Transforma a entrada do usuário no indice que representa a cor informada
            cor_informada_index = get_cor_index_informada(cor_informada)
            lista_player.inserir_fim(cor_informada_index)

            # Verifica se a cor informada é diferente da correta
            cor_index = aux.valor
            if cor_informada_index != cor_index:
                # Determina a pontuação
                score = lista_bot.tamanho() - 1
                print('Você errou!')
                print('Score:', score)

                print('Sequência correta:   ', end='')
                exibir_sequencia(lista_bot)
                print('Sequência informada: ', end='')
                exibir_sequencia(lista_player)

                # Limpa a lista das cores para uma próxima rodada
                lista_bot.limpar_lista()

                if score > 0:
                    # Pede para informar um nome para o ranking
                    nome = input('Informe seu nome para o ranking: ')
                    while len(nome) < 4 or ';' in nome:
                        print("Nome inválido. O nome deve possuir pelo menos 4 caracteres e não pode conter ';'")
                        nome = input('Informe seu nome para o ranking:')
                    # inclui a entrada no ranking
                    adicionar_ao_ranking(nome, score)

                # Exibir o ranking
                ranking()

                # Pergunta se deseja cotinuar jogando
                jogar_novamente = aguarda_entrada_valida('Você deseja continuar jogando? [s/n]: '
                                                         , ['s', 'n']
                                                         , "Entrada inválida. Digite apenas 's' ou 'n'"
                                                         , True)
                                                        
                continuar = jogar_novamente != 'n'
                break
            
            # Avançar para o próximo elemento da lista
            aux = aux.proximo
            i += 1

#adiciona novas cores à lista correta (aKa bot)
def adiciona_cor():
    cor_index = random.randint(0, len(cores) - 1)
    lista_bot.inserir_fim(cor_index)

#recebe o que foi inserido pelo usuário e compara à lista gabarito
def get_cor_index_informada(entrada: str) -> int:
    i = 0
    for cor in cores:
        # Verifica a string da cor ou pelo indice
        if cor.lower() == entrada or str(i + 1) == entrada:
            return i
        i += 1
    return -1

# Método para validar a entrada e retornar a string de entrada valida
def aguarda_entrada_valida(mensagem: str, entradas_validas: list, mensagem_erro: str, ingore_case: bool):
    entrada = input(mensagem)
    if ingore_case:
        entrada = entrada.lower()

    # Aguarda uma entrada válida
    while entrada not in entradas_validas:
        print(mensagem_erro)
        entrada = input(mensagem)
        if ingore_case:
            entrada = entrada.lower()

    return entrada

#exibe a sequencia da lista encadeada
def exibir_sequencia(sequencia: ListaEncadeada):
    aux = sequencia.primeiro
    while aux is not None:
        # Exibir a cor formatada
        print(get_cor_formatada(aux.valor), end=' ')
        aux = aux.proximo
    print('')

#apenas uma sequencia de prints que explicam como funciona o jogo
def tutorial():
    print('-----------------------------------------------------------------')
    print('O jogo funciona da seguinte maneira:\n'
          'Será exibido ao jogador uma palavra referente à cor atribuida à uma sequência. '
          'Em seguida, a palavra(cor) será removida da tela e o programa esperará que o usuário insira um código '
          'referente à cor que foi mostrada anteriormente. '
          'Por exemplo:\n'
          'Se o programa mostrou a palavra Azul, o usuário deverá inserir a palavra Azul, ou A ou 4. '
          'Caso contrário, o jogo será encerrado pois essa regra não foi obedecida.\n'
          'No caso de derrota, o usuário ainda poderá escolher se quiser jogar novamente ou voltar ao menu principal, '
          'podendo acessar o ranking, jogar novamente ou sair para encerrar o programa.')
    print('-----------------------------------------------------------------')
    input('Pressione ENTER para continuar...')
    limpa_terminal()

#mostra os players com suas respectivas pontuações, da maior para menor(decrescente)
def ranking():
    print('Ranking:')
    carregar_ranking()
    print('Nome - Pontuação')
    for registro in ranking_list:
        print(registro.nome, '-', registro.score)
    input('Pressione ENTER para continuar...')
    limpa_terminal()

#abre e lê os dados do bloco de notas, que contêm o rankingg
def carregar_ranking():
    ranking_list.clear()
    try:
        # Abrir aquivo de ranking para leitura
        file = open('ranking.txt', 'r')
        # Ler as linhas do arquivo
        linhas = file.readlines()
        i = 0
        # Percorer as linhas
        for linha in linhas:
            if i >= 5:
                break
            # Adicionar o registro na lista do ranking
            registro = RegistroRanking()
            registro.from_string(linha)
            ranking_list.append(registro)
            i += 1
    # Lidar com a exceção de arquivo não encontrado
    except FileNotFoundError:
        ranking_list.clear()

#salva conteudo do ranking (txt)
def salvar_ranking():
    # Escrever os registro do ranking no arquivo
    file = open('ranking.txt', 'w')
    for registro in ranking_list:
        file.write(registro.to_string() + '\n')

#registra um nome uma pontuação por vez, após um jogo no bloco de notas, que contêm o ranking
def adicionar_ao_ranking(nome: str, score: int):
    carregar_ranking()
    i = 0
    adicionado = False

    # Percorer a lista do ranking para ver em qual indice deve ser adicionado o regristro atual
    for registro in ranking_list:
        if score > registro.score:
            novo_registro = RegistroRanking()
            novo_registro.nome = nome
            novo_registro.score = score
            ranking_list.insert(i, novo_registro)
            adicionado = True

            # Caso a lista tenha ficado com mais de 5 elementos, remover o último
            if len(ranking_list) > 5:
                ranking_list.pop()

            # Salvar arquivo
            salvar_ranking()
            break
        i += 1
    
    # Caso o regristro atual não tenha um score maior do que os registro da lista
    # e a lista possuir menos de 5 elementos, adiocionar o registro no final
    if adicionado == False and len(ranking_list) < 5:
        novo_registro = RegistroRanking()
        novo_registro.nome = nome
        novo_registro.score = score
        ranking_list.append(novo_registro)
        salvar_ranking()


# Método para retornar a string da cor formatada baseado no indice
def get_cor_formatada(index):
    return cores_formatadas[index]


#execução do código como um todo a partir do menu principal, que chama as funcionalidades necessárias
while True:
    menu_principal()
