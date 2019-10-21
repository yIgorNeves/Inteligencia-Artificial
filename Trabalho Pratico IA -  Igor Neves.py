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

"""
Verificação dos movimentos validos
"""
def mov_validos(a, b, original):
    if (a == b) or ((a+b) != original):
        print("Movimento invalido os numeros sao iguais ou a soma deles é maior que o conjunto!")
        return False
    return True

"""
Função para verificar se o numero pode ser dividido
"""
def num_div(original):
    if int(original) > 2 and original in conjunto_de_palitos:
        return True
    else:
        return False

#condição de vitoria 
#se tiver algum numero maior que 2 o jogo ainda nao terminou
def vitoria(conjunto_de_palitos):
    venceu = True
    for x, row in enumerate(conjunto_de_palitos):
        num = int(conjunto_de_palitos[x])
        if x >2:
            venceu = False
    if venceu:
        return True
    else:
        return False


#Testa fim de jogo para ambos jogadores de acordo com estado atual
#return: será fim de jogo caso ocorra vitória de um dos jogadores.

def fim_jogo(conjunto_de_palitos):
    for i in conjunto_de_palitos:
        if i > 2:
            return False
    return True

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (a): valor de a
:param (y): valor de b
:param (orginal): valor original que sera substituido
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
def avaliacao(conjunto_de_palitos, jogador):
    
    if vitoria(conjunto_de_palitos) and jogador == -1:
        placar = +1
    elif vitoria(conjunto_de_palitos) and jogador == +1:
        placar = -1
    else:
        placar = 0

    return placar

"""
verifica se um numero pode ser dividido e retorna o resultado dessa divisao
"""
def div_disponiveis(divisiveis):
    lista_menor = []
    if divisiveis > 2:
        if divisiveis%2 == 0:
            menor = (divisiveis/2)-1
            lista_menor.append(int(menor))

            return lista_menor

        else: 
            menor = divisiveis/2
            lista_menor.append(int(menor))
            return lista_menor
"""
calcula profundidade do conjunto de palitos
"""
def calcula(palitos):
    profundidade =0
    for x in palitos:
        if x > 2:
            profundidade += 1
    return profundidade


"""
Função da IA que escolhe o melhor movimento
:param (palitos): estado atual do jogo
:param (profundidade): tamanho da lista de palitos
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
        placar = avaliacao(palitos, COMP)
        return [-1, -1, placar]
    
    for numeros in numeros_disponiniveis(palitos):
       
        for min in div_disponiveis(numeros):
            posi = palitos.index(numeros)
            palitos.insert(posi+1, numeros-min)
            palitos[posi] = min  
         
            placar = minimax(palitos, calcula(palitos), -jogador)            
            placar[0], placar[1] =  numeros-min, min

            palitos[posi] = numeros
            palitos.pop(posi+1)

            if jogador == COMP:
                if placar[2] > melhor[2]:
                    melhor = placar  # valor MAX
            else:
                if placar[2] < melhor[2]:
                    melhor = placar  # valor MIN
        return melhor
"""
Metodo para a vez da IA:
"""
def IA_vez(conjunto_de_palitos):

    profundidade = len(numeros_disponiniveis(conjunto_de_palitos))
    if profundidade == 0 or fim_jogo(conjunto_de_palitos):
        return
    
    print("Vez do computador aguarde")
    print(conjunto_de_palitos)

    if fim_jogo(conjunto_de_palitos) == True:
        x = conjunto_de_palitos[0]
    elif len(conjunto_de_palitos) == 1:
        info = conjunto_de_palitos[0]
        valor = info
        exec_movimento(info-1, 1, info)

    else:
        move = minimax(conjunto_de_palitos, profundidade, COMP)
        x = move[0]
        y = move[1]
        print("O computador subistituiu:",(x+y),"por",x ,"e",y)
        exec_movimento(x, y, (x+y))

    

    if fim_jogo(conjunto_de_palitos):
        print("Voce Perdeu")


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
   
    exec_movimento(a, b, original)

    if fim_jogo(conjunto_de_palitos):
        print("Voce venceu!!!!")
        
        
                
"""
Metodo Principal que chama os metodos para jogar
"""
def main():
    
    limpa_console()
    
    numero_de_palitos = int(input("Digite o numero de palitos parar o começar o jogo: "))
    conjunto_de_palitos.append(numero_de_palitos)
    
    print(conjunto_de_palitos)
    #Laço principal do jogo
    
    while fim_jogo(conjunto_de_palitos)== False:
        IA_vez(conjunto_de_palitos)
        if fim_jogo(conjunto_de_palitos):
            print("Posições Disponiveis: %d" % len(numeros_disponiniveis(conjunto_de_palitos)))
            print(sorted(conjunto_de_palitos, reverse=True))
            break
        print("Sua vez:")
        print("Posições Disponiveis: %d" % len(numeros_disponiniveis(conjunto_de_palitos)))
        print(sorted(conjunto_de_palitos, reverse=True))
        HUMANO_vez(conjunto_de_palitos)
    

if __name__ == "__main__":
    main()

#enumarate procurar sobre