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
        if cell>2: 
            numeros.append(cell)
            #print("numero disponivel",numeros)
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


def div_disponiveis(divisiveis):
    for x in divisiveis:
        lista_menor = []
        if x > 2:
            if x%2 == 0:
                menor = (x/2)-1
                lista_menor.append(int(menor))
                return lista_menor

            else: 
                menor = x/2
                lista_menor.append(int(menor))
                return lista_menor

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""
num_list =[]
def minimax(palitos, profundidade, jogador):

    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(palitos):
        placar = avaliacao(palitos)
        return [-1, -1, placar]

    for numeros in numeros_disponiniveis(palitos):
        num_list.append(numeros)
        """
        print("-------")
        print("palitos", palitos)
        print("numeros selecionado",numeros)        
        print("numlist",num_list)
        """        
        for min in div_disponiveis(num_list):
            num_list.remove(numeros)
            #print("-------")

            #print("min",min)            
            posi = palitos.index(numeros)
            #print("posi",posi)
            palitos.insert(posi+1, numeros-min)
            """
            print("palitos",palitos)
            print("palitos posi",palitos[posi])
            """
            palitos[posi] = min  
            """
            print("palitos att", palitos)
            print("palitos posi att",palitos[posi])
            print("-------")
            """

                      
            placar = minimax(palitos, div_disponiveis(palitos), -jogador)            
            placar[0], placar[1] =  numeros-min, min
            #print("placar:",placar)
            #print("numeros:", numeros)
            palitos[posi] = numeros
            #print("palitos[posi]:",palitos[posi])
            palitos.pop(posi+1)
            """
            print("posi:",posi)
            print("palitos:",palitos)
            print("melhor:",melhor)
            input()
            """

            if jogador == COMP:
                if placar[2] > melhor[2]:
                    melhor = placar  # valor MAX
            else:
                if placar[2] < melhor[2]:
                    melhor = placar  # valor MIN
        return melhor
"""
Função para a vez da IA:
"""
def IA_vez(conjunto_de_palitos):

    profundidade = len(numeros_disponiniveis(conjunto_de_palitos))
    if profundidade == 0 or fim_jogo(conjunto_de_palitos):
        return
    
    print("Vez do computador aguarde")
    print(conjunto_de_palitos)

    if fim_jogo(conjunto_de_palitos) == True:
        x = conjunto_de_palitos[0]
    else:
        move = minimax(conjunto_de_palitos, profundidade, COMP)
        x = move[0]
        y = move[1]
        print("O computador subistituiu:",(x+y),"por",x ,"e",y)

    exec_movimento(x, y, (x+y))


"""
Metodo para a vez do humano
"""
def HUMANO_vez(conjunto_de_palitos):

    print("O conjunto de palitos é:", sorted(conjunto_de_palitos , reverse=True))
    
    original = int(input("Qual conjunto de palitos deseja dividir: "))
    
    while num_div(original) == False:
        print("A quantidade de palitos nao pode ser divida ou nao esta no conjunto.")            
        original = int(input("Qual conjunto de palitos deseja dividir: "))
    a = int(input("Qual o primeiro numero que voce gostaria de colocar: "))
    b = int(input("Qual o segundo numero que voce gostaria de colocar: "))
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
        IA_vez(conjunto_de_palitos)
        HUMANO_vez(conjunto_de_palitos)
        print("Posições Disponiveis: %d" % len(numeros_disponiniveis(conjunto_de_palitos)))
        print(sorted(conjunto_de_palitos, reverse=True))
    
if __name__ == "__main__":
    main()

#enumarate procurar sobre