#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-
"""
@author: Igor Neves
"""
"""
Este código se refere ao primeiro trabalho pratico da disciplina Inteligencia Artificial.
"""

#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system


HUMANO = -1
COMP = +1
conjunto_de_palitos = []

#definição de movimentos validos
def mov_validos(a, b, original):
    if (a == b) or ((a+b) != original):
        print("Movimento invalido os numeros sao iguais ou a soma deles é maior que o conjunto!")
        return False
    return True

"""
função para verificar se o numero pode ser dividido
"""
def num_div(original):
    if int(original) > 2 and original in conjunto_de_palitos:
        return True
    else:
        return False

#condição de vitoria 
#se tiver algum numero maior que 2 o jogo ainda nao terminou
def vitoria(conjunto_de_palitos, jogador):
    for i in conjunto_de_palitos:
        if i >2:
            return False
    return True


#Testa fim de jogo para ambos jogadores de acordo com estado atual
#return: será fim de jogo caso ocorra vitória de um dos jogadores.

def fim_jogo(conjunto_de_palitos):
    for i in conjunto_de_palitos:
        if i > 2:
            return False
    return True

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (x): coordenadas X
:param (y): coordenadas Y
:param (jogador): o jogador da vez
"""
def exec_movimento(a, b, original):
    if mov_validos(a, b, original) == True:
        conjunto_de_palitos.remove(original)
        conjunto_de_palitos.append(a)
        conjunto_de_palitos.append(b)   
        sorted(conjunto_de_palitos, reverse=True)     
        return True
    else:
        return False

"""
Verifica celular vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""
def numeros_disponiniveis(conjunto_de_palitos):
    numeros = []
    for x, cell in enumerate(conjunto_de_palitos):
        if cell>2: numeros.append([cell])
    print(len(numeros))
    return numeros


def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: +1 se o computador vence; -1 se o HUMANOo vence; 0 empate
 """
def avaliacao(conjunto_de_palitos):
    
    if vitoria(conjunto_de_palitos, COMP):
        placar = +1
    elif vitoria(conjunto_de_palitos, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""
def minimax(conjunto_de_palitos, profundidade, jogador):

    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(conjunto_de_palitos):
        placar = avaliacao(conjunto_de_palitos)
        return [-1, -1, placar]

    for numero in numeros_disponiniveis(conjunto_de_palitos):
        x, y = numero[0], numero[1]
        conjunto_de_palitos[x][y] = jogador
        placar = minimax(conjunto_de_palitos, profundidade - 1, -jogador)
        conjunto_de_palitos[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
    return melhor
""" ---------------------------------------------------------- """

"""
Função para a vez da IA:
"""
def IA_vez(IA):
    profundidade = len(numeros_disponiniveis(conjunto_de_palitos))
    if profundidade == 0 or fim_jogo(conjunto_de_palitos):
        return
    
    print("Vez do computador aguarde")


"""
Metodo para a vez do humano
"""
def HUMANO_vez(conjunto_de_palitos):
    original = int(input("Qual conjunto de palitos deseja dividir: "))
    while num_div(original) ==  False:
        print("A quantidade de palitos nao pode ser divida ou nao esta no conjunto.")            
        original = int(input("Qual conjunto de palitos deseja dividir: "))
        a = int(input("Qual o primeiro numero que voce gostaria de colocar: "))
        b = int(input("Qual o segundo numero que voce gostaria de colocar: "))
        #Laço para caso o jogador coloque numeros iguais ou a soma dos numeros seja maior que o numero original
        while mov_validos(a, b, original) == False:
            a = int(input("Qual o primeiro numero que voce gostaria de colocar: "))
            b = int(input("Qual o segundo numero que voce gostaria de colocar: "))           
        if mov_validos(a,b, original) == True:
            exec_movimento(a, b, original)
        
"""
Metodo Principal que chama todas funcoes
"""
def main():
    limpa_console()
    numero_de_palitos = int(input("Digite o numero de palitos parar o começar o jogo: "))
    conjunto_de_palitos.append(numero_de_palitos)
    print(conjunto_de_palitos)
    #Laço principal do jogo
    while fim_jogo(conjunto_de_palitos)== False:
        original = int(input("Qual conjunto de palitos deseja dividir: "))
        #laço para caso o jogador coloque um numero nao valido
        while num_div(original) ==  False:
            print("A quantidade de palitos nao pode ser divida ou nao esta no conjunto.")            
            original = int(input("Qual conjunto de palitos deseja dividir: "))
        a = int(input("Qual o primeiro numero que voce gostaria de colocar: "))
        b = int(input("Qual o segundo numero que voce gostaria de colocar: "))
        #Laço para caso o jogador coloque numeros iguais ou a soma dos numeros seja maior que o numero original
        while mov_validos(a, b, original) == False:
            a = int(input("Qual o primeiro numero que voce gostaria de colocar: "))
            b = int(input("Qual o segundo numero que voce gostaria de colocar: "))           
        if mov_validos(a,b, original) == True:
            exec_movimento(a, b, original)
        print("Posições Disponiveis: %d" % len(numeros_disponiniveis(conjunto_de_palitos)))
        print(sorted(conjunto_de_palitos, reverse=True))
    

    

if __name__ == "__main__":
    main()

#enumarate procurar sobre