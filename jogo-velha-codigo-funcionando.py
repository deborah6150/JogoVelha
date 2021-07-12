from math import inf as infinity
import math
from random import choice
import platform
import time
from os import system
from sys import exit

"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""


HUMANO = -1
COMP = +1
tabuleiro = []
N = 0
dificuldade = 1
estados_gerados_total = 0
posicoes = []

"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: Retorna um valor baseado na quantidade de peças do computador em cada linha coluna, diagonal principal e secundária usando função eval
 """


def avaliacao(estado):

    global N
    win_estado = possiveis_estados_vitoria(estado)

    evalVariablesHuman = [0 for z in range(N)]
    evalVariablesComputer = [0 for z in range(N)]

    for z in range(N):
        for w in win_estado:
            if(w.count(1) == z+1 and w.count(0) == (N - (z+1))):
                evalVariablesComputer[z] = evalVariablesComputer[z] + 1
            if(w.count(-1) == z+1 and w.count(0) == (N - (z+1))):
                evalVariablesHuman[z] = evalVariablesHuman[z] + 1
    resulthuman = 0
    resultcomputer = 0
    for z in range(N):
        resultcomputer = resultcomputer + (z+1)*(evalVariablesComputer[z])
        resulthuman = resulthuman + (z+1)*(evalVariablesHuman[z])

    return resultcomputer - resulthuman


""" fim avaliacao (estado)------------------------------------- """

"""
Funcao para gerar os possíveis estados de vitória no tabuleiro.
:parametro (estado): o estado atual do tabuleiro
:returna: lista de listas com as possiveis vitorias no estado atual
 """


def possiveis_estados_vitoria(estado):

    global N
    win_estado = []
    diagonal_principal = []
    diagonal_secundaria = []
    for line in range(N):
        winLine = []
        winColumn = []
        diagonal_principal.append(estado[line][line])
        diagonal_secundaria.append(estado[line][((N - 1) - line)])
        for column in range(N):
            winLine.append(estado[line][column])
            winColumn.append(estado[column][line])
        win_estado.append(winLine)
        win_estado.append(winColumn)
    win_estado.append(diagonal_principal)
    win_estado.append(diagonal_secundaria)

    return win_estado


""" fim possiveis_estados_vitoria (estado)------------------------------------- """

def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence.
    :param. (estado): o estado atual do tabuleiro
    :param. (jogador): um HUMANO ou um Computador
    :return: True se jogador vence
    """

    global tam_tabuleiro
    win_estado = possiveis_estados_vitoria(estado)

    # Se um, dentre todos os alinhamentos pertence um mesmo jogador,
    # então o jogador vence!
    if [jogador for z in range(N)] in win_estado:
        return True
    else:
        return False



""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""


def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)


""" ---------------------------------------------------------- """

"""
Verifica celular vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""


def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0:
                celulas.append([x, y])
    return celulas


def movimento_valido(x, y):
    """
    Um movimento é valido se a célula escolhida está vazia.
    :param x: coordenada X
    :param y: coordenada Y
    :return: True se o tabuleiro[x][y] está vazio
    """
    global tabuleiro, N
    return (0 <= x < N) and (0 <= y < N) and (tabuleiro[x][y] == 0)

  

def exec_movimento(x, y, jogador):
    """
    Executa o movimento no tabuleiro se as coordenadas são válidas
    :param (x): coordenadas X
    :param (y): coordenadas Y
    :param (jogador): o jogador da vez
    """
    global tabuleiro
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False


def minimax(estado, profundidade, jogador):
    """
    Função da IA que escolhe o melhor movimento
    :param (estado): estado atual do tabuleiro
    :param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
    mas nunca será nove neste caso (veja a função iavez())
    :param (jogador): um HUMANO ou um Computador
    :return: uma lista com [melhor linha, melhor coluna, melhor placar]
    """
    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar]
        

    for cell in celulas_vazias(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundidade - 1, -jogador)
        
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
    return melhor


def limpa_console():
    """
    Limpa o console para SO Windows
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    """
    Imprime o tabuleiro no console
    :param. (estado): estado atual do tabuleiro
    """
    global N
    for t in range(N):
        print('-----', end='')
    for row in estado:
        print('')
        for t in range(N):
            print('-----', end='')
        print('')
        for cell in row:
            if cell == +1:
                print('|', comp_escolha, '|', end='')
            elif cell == -1:
                print('|', humano_escolha, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('')
    for t in range(N):
        print('-----', end='')
    print('')


def IA_vez(comp_escolha, humano_escolha):
    """
    Chama a função minimax se a profundidade < 25,
    ou escolhe uma coordenada aleatória.
    :param (comp_escolha): Computador escolhe X ou O
    :param (humano_escolha): HUMANO escolhe X ou O
    :return:
    """
    global N, tabuleiro, posicoes
    # print(celulas_vazias(tabuleiro))
    #profundidade = int(math.log(len(celulas_vazias(tabuleiro)), 2))
    #profundidade = math.floor(math.log(len(celulas_vazias(tabuleiro))))
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    # if profundidade == (N ** 2):
    #     x = choice([z for z in range(N)])
    #     y = choice([z for z in range(N)])
    # else:
    #     move = minimax(tabuleiro, profundidade, COMP)

    if profundidade == (N ** 2):
        x = choice([z for z in range(N)])
        y = choice([z for z in range(N)])
        pos = (x,y)      
        posicoes.append(pos)  
    else:
        if(profundidade > 5):
            move = minimax(tabuleiro, profundidade, COMP)
            x, y = move[0], move[1]
            pos = (x,y)

            while pos in posicoes:
                x = choice([z for z in range(N)])
                y = choice([z for z in range(N)])   
                pos = (x,y)    
          
            posicoes.append(pos)                
        else:
            while True:
                x = choice([z for z in range(N)])
                y = choice([z for z in range(N)])   
                pos = (x,y)
                if pos not in posicoes:
                    posicoes.append(pos)
                    break
          
    exec_movimento(x, y, COMP)
    time.sleep(0.1)


""" ---------------------------------------------------------- """

def HUMANO_vez(comp_escolha, humano_escolha):

    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """

    global N, tabuleiro
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return
        
    limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    xx = -1
    yy = -1
    while xx < 1 or xx > N or yy < 1 or yy > N:
        try:
            xx = int(
                input('Entre com a coordenada horizontal (1..' + str(N) + '): '))
            yy = int(input('Entre com a coordenada vertical (1..' + str(N) + '): '))
            coord = (xx - 1, yy - 1)
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO) if coord not in posicoes else False
         
            if tenta_movimento == False:
                print('Movimento Inválido')
                xx = -1; yy = -1
            else: posicoes.append(coord)
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')


""" ---------------------------------------------------------- """

"""
Funcao Principal que chama todas funcoes
"""


def main():
    global tabuleiro, N, INC_PROFUNDIDADE
    limpa_console()
    humano_escolha = ''  # Pode ser X ou O
    comp_escolha = ''  # Pode ser X ou O
    primeiro = ''  # se HUMANO e o primeiro

    # HUMANO escolhe X ou O para jogar
    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    # Setting Computador's choice
    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    # HUMANO pode começar primeiro
    # Escolha do tamanho do tabuleiro
    N = -1
    while N < 3:
        try:
            print('')
            N = int(input('Escolha o tamanho do tabuleiro\n: '))
            if N < 3:
                print('Escolha Errada, entre com um valor a partir de 3.')
        except KeyboardInterrupt:
            print('Tchau!')
            exit()

    tabuleiro = [[0 for _ in range(N)] for _ in range(N)]
    limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    # Laço principal do jogo
    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(comp_escolha, humano_escolha)
        IA_vez(comp_escolha, humano_escolha)

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()
