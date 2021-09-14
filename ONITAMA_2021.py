# ONITAMA 2021, versão 1

# imports iniciais
import pygame
import random

# TO DO / BUG_LIST
'''
criar um timing entre os movimentos amigos e inimigos
renderizar estilo B para ver a carta do oponente

melhorar interface / bugs
- bug da selecao fantasma

resolver bugs
- dois inimigos na mesma casa
- out of bounds
- movimento impossivel

fazer uma IA um pouco menos idiota
fazer um modo multiplayer
fazer uma seleção de cartas
fazer um criador de cartas
'''

#########################################################
#        ONITAMA 2021
#########################################################
"""
Onitama é um jogo de tabuleiro desenvolvido em 2014 por Shimpei Sato e publicado pela Arcane Wonders.
Essa implementação virtual e suas regras especificas (home rules) foram desenvovidos por Vitor Gasparetto.
O código foi feito por Vitor Gasparetto, com ajuda de Nathalia Hermann

Onitama é um boardgame baseado em xadrez, onde você joga em um tabuleiro de 5x5
Cada jogador têm 4 aprendizes (peões) e um sensei (rei), alem disso há tambem o Espirito do Vento que é uma peça neutra
Há cinco cartas em jogo, delimitando os movimentos que as peças podem fazer
(2 dessas cartas em sua mão, 2 na mão do oponente, uma no meio)
As jogadas são feitas selecionando uma carta e uma peça
Após a jogada ser feita, a carta utilizada vai para o meio e a carta do meio vai para a sua mão

Os peões e senseis podem comer peças do oponente ao parar em suas casas
O espirito do vento troca de lugar com a peça do oponente (apenas peões)

O jogo chega ao fim de quatro maneiras possiveis
"Caminho das Nuvens" = Levar o espirito do vento ao portão do seu oponente (a casa do sensei)
"Caminho das Pedras" = Destruir todos os aprendizes do oponente
"Caminho das Chamas" = Destruir o sensei do oponente
"Caminho do Rio" = Levar o seu sensei ao portão do oponente

O jogo conta apenas com um modo de um jogador, com uma IA basica para testes
perder contra essa IA é um desafio gigantesco

Abaixo pode ser visto o código, ele está bastante confuso, ineficiente e redundante
- As definições de funções pode ser agrupada de forma melhor
- As definições de variaveis podem ser agrupadas e chamadas de forma melhor
- Muitos valores são redundantes e tem nomes confusos
"""

#########################################################
# inicia o pygame
pygame.init()
#########################################################
# settings janela
# altura e largura da tela
display_width = 800
display_height = 500
'''
A ESQUERDA AS CARTAS (500 H, 300 W)
A DIREITA TABULEIRO (500x500)
'''

#########################################################
# display
DISPLAY = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ONITAMA 2021')
# clock
clock = pygame.time.Clock()


#########################################################
# imagens
# jpgs do tabuleiro
GridImages = [[None, None], # pawn
              [None, None], # sensei
              [None, None], # gate
              [None, None], # select
              None,         # wind
              None]         # empty
GridImages[0][0] = pygame.image.load('100_pawn_blue.png').convert_alpha()
GridImages[0][1] = pygame.image.load('100_pawn_red.png').convert_alpha()
GridImages[1][0] = pygame.image.load('100_sensei_blue.png').convert_alpha()
GridImages[1][1] = pygame.image.load('100_sensei_red.png').convert_alpha()
GridImages[2][0] = pygame.image.load('100_gate_blue.png').convert_alpha()
GridImages[2][1] = pygame.image.load('100_gate_red.png').convert_alpha()
GridImages[3][0] = pygame.image.load('100_select.png').convert_alpha()
GridImages[3][1] = pygame.image.load('100_selected.png').convert_alpha()
GridImages[4] = pygame.image.load('100_wind.png').convert_alpha()
GridImages[5] = pygame.image.load('100_empty.png').convert_alpha()

# jpgs das cartas
CardImages = [None, # normal
              None, # invert
              None] # select
CardImages[0] = pygame.image.load('card_normal.png').convert_alpha()
CardImages[1] = pygame.image.load('card_invert.png').convert_alpha()
CardImages[2] = pygame.image.load('card_select.png').convert_alpha()

BackGround = [None, # intro
              None] # jogo
BackGround[0] = pygame.image.load('backg.png').convert_alpha()
BackGround[1] = pygame.image.load('backg2.png').convert_alpha()

#########################################################
# cores
# color, cores basicas e feias
color = {"black": (0, 0, 0),
         "grey": (50, 50, 50),
         "white": (255, 255, 255),
         "brown": (150, 130, 80),
         "red": (200, 0, 0),
         "green": (0, 200, 0),
         "blue": (0, 0, 200)}
# coolor
# cores em paleta : letra1-letra5
coolor = {"a1": (129, 94, 91),
          "a2": (104, 81, 85),
          "a3": (122, 111, 155),
          "a4": (139, 133, 193),
          "a5": (255, 247, 245),
          "b1": (249, 160, 63),
          "b2": (247, 212, 136),
          "b3": (246, 216, 174),
          "b4": (252, 208, 161),
          "b5": (241, 191, 152),
          "c1": (58, 48, 66),
          "c2": (255, 120, 79),
          "c3": (255, 225, 156),
          "c4": (222, 184, 65),
          "c5": (222, 158, 54),
          "d1": (230, 232, 230),
          "d2": (206, 208, 206),
          "d3": (105, 181, 120),
          "d4": (58, 125, 68),
          "d5": (37, 77, 50),
          "e1": (231, 255, 185),
          "e2": (131, 231, 173),
          "e3": (95, 205, 178),
          "e4": (62, 176, 175),
          "e5": (31, 107, 155),
          "f1": (238, 162, 73),
          "f2": (248, 250, 193),
          "f3": (166, 185, 137),
          "f4": (108, 122, 97),
          "f5": (69, 68, 81)}
# keymap do coolor
# usado pra chamar essas cores
keymap = [["a1", "a2", "a3", "a4", "a5"],
          ["b1", "b2", "b3", "b4", "b5"],
          ["c1", "c2", "c3", "c4", "c5"],
          ["d1", "d2", "d3", "d4", "d5"],
          ["e1", "e2", "e3", "e4", "e5"],
          ["f1", "f2", "f3", "f4", "f5"]]

#########################################################
# funções graficas
# TEXTO                                                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# objeto texto
def text_objects(text, font, colour):
    text_surface = font.render(text, True, colour)
    return text_surface, text_surface.get_rect()

# mostrar mensagem em vermelho
def message_display(text, x, y, size):
    large_text = pygame.font.Font('freesansbold.ttf', size)
    text_surf, text_rect = text_objects(text, large_text, color["red"])
    text_rect.center = int(x), int(y)
    DISPLAY.blit(text_surf, text_rect)

# colocar imagem em ponto
def draw_img(img, x, y):
    DISPLAY.blit(img, (x, y))

# desenhar retangulo
def draw_rect(thingx, thingy, thingw, thingh, colour):  # x, y, largura, altura, cor
    pygame.draw.rect(DISPLAY, colour, [thingx, thingy, thingw, thingh])

# desenhar retangulo zoado
# usado pra efeitos visuais
def draw_rect_zoado(thingx, thingy, colour):  # x, y, 80, 80
    pygame.draw.rect(DISPLAY, colour, [thingx, thingy, 75 + (random.randint(-30, 20)), 75 + (random.randint(-30, 20))])

# desenhar quadrado 100x100
# tamanho da peca de tabuleiro
def draw_square100(thingx, thingy, colour):  # x, y, 100, 100
    pygame.draw.rect(DISPLAY, colour, [thingx, thingy, 100, 100])

# DESENHAR CARTAS, IMPORTANTISSIMO
# posicao da carta, qual carta imprimir, quem é o jogador ativo
# active b == inimigo
'''
a função active nao foi implementada, o plano era mudar a renderização grafica dependendo de se for o jogador 1 ou 2
mas como só tem modo para um jogador, isso acabou não sendo feito
'''
def draw_card(pos, carta, active):
    # pos :: a1, a2, b1, b2, c1
    # amigo, binimigo, centro (0esq, 1dir)

    # posicao dos X e Y das cartas
    global cardY, cardX
    if pos[0] == "a":
        cardY = 338+75
        if pos[1] == "1":
            # amigo esquerdo
            cardX = 30+50
        else:
            # amigo direito
            cardX = 160+50
    elif pos[0] == "b":
        cardY = 12+75
        if pos[1] == "1":
            # inimigo  esquerdo
            cardX = 30 + 50
        else:
            # inimigo direito
            cardX = 160+50
    elif pos[0] == "c":
        # centro
        cardY = 175+75
        cardX = 100+50
    # meio da carta
    # usado pra desenhar os pontinhos coloridos
    cardcenter = [cardX, cardY]

    if pos[0] == "b":
        message_display(carta.capitalize(), cardcenter[0], cardcenter[1] - 60, 15)
    else:
        if active == 'b':
            message_display(carta.capitalize(), cardcenter[0], cardcenter[1] - 60, 15)
        else:
            message_display(carta.capitalize(), cardcenter[0], cardcenter[1] + 60, 15)

    # desenhar pontos, movimentos da carta
    # as suas
    if pos[0] == "a":
        for un in range(1, len(cards[carta])):
            ptX = int((cards[carta][un][0]) * 20)
            ptY = int((cards[carta][un][1]) * 20)
            pygame.draw.circle(DISPLAY, color["red"], (cardcenter[0] + ptY, cardcenter[1] + ptX), 6)

    # do oponente
    if pos[0] == "b":
        for un in range(1, len(cards[carta])):
            ptX = int((cards[carta][un][0]) * 20)
            ptY = int((cards[carta][un][1]) * 20)
            pygame.draw.circle(DISPLAY, color["blue"], (cardcenter[0] - ptY, cardcenter[1] - ptX), 6)

    # centro
    # é pra variar de acordo com o active, mas active não foi implementado
    if pos[0] == "c":
        if active == 'b':
            for un in range(1, len(cards[carta])):
                ptX = int((cards[carta][un][0]) * 20)
                ptY = int((cards[carta][un][1]) * 20)
                pygame.draw.circle(DISPLAY, color["black"], (cardcenter[0] - ptY, cardcenter[1] - ptX), 6)
        else:
            for un in range(1, len(cards[carta])):
                ptX = int((cards[carta][un][0]) * 20)
                ptY = int((cards[carta][un][1]) * 20)
                pygame.draw.circle(DISPLAY, color["black"], (cardcenter[0] + ptY, cardcenter[1] + ptX), 6)

# fundo do tabuleiro
# essa função pode ser bastante simplificada usando loops
def draw_board_backg():
    draw_square100(300, 0, coolor['b2'])
    draw_square100(400, 0, coolor['f2'])
    draw_square100(500, 0, coolor['b2'])
    draw_square100(600, 0, coolor['f2'])
    draw_square100(700, 0, coolor['b2'])

    draw_square100(300, 100, coolor['f2'])
    draw_square100(400, 100, coolor['b2'])
    draw_square100(500, 100, coolor['f2'])
    draw_square100(600, 100, coolor['b2'])
    draw_square100(700, 100, coolor['f2'])

    draw_square100(300, 200, coolor['b2'])
    draw_square100(400, 200, coolor['f2'])
    draw_square100(500, 200, coolor['b2'])
    draw_square100(600, 200, coolor['f2'])
    draw_square100(700, 200, coolor['b2'])

    draw_square100(300, 300, coolor['f2'])
    draw_square100(400, 300, coolor['b2'])
    draw_square100(500, 300, coolor['f2'])
    draw_square100(600, 300, coolor['b2'])
    draw_square100(700, 300, coolor['f2'])

    draw_square100(300, 400, coolor['b2'])
    draw_square100(400, 400, coolor['f2'])
    draw_square100(500, 400, coolor['b2'])
    draw_square100(600, 400, coolor['f2'])
    draw_square100(700, 400, coolor['b2'])

    # linhas verticais
    pygame.draw.line(DISPLAY, color["black"], (300, 0), (300, 500))
    pygame.draw.line(DISPLAY, color["black"], (400, 0), (400, 500))
    pygame.draw.line(DISPLAY, color["black"], (500, 0), (500, 500))
    pygame.draw.line(DISPLAY, color["black"], (600, 0), (600, 500))
    pygame.draw.line(DISPLAY, color["black"], (700, 0), (700, 500))
    pygame.draw.line(DISPLAY, color["black"], (799, 0), (799, 500))
    # linhas horizontais
    pygame.draw.line(DISPLAY, color["black"], (300, 1), (800, 1))
    pygame.draw.line(DISPLAY, color["black"], (300, 100), (800, 100))
    pygame.draw.line(DISPLAY, color["black"], (300, 200), (800, 200))
    pygame.draw.line(DISPLAY, color["black"], (300, 300), (800, 300))
    pygame.draw.line(DISPLAY, color["black"], (300, 400), (800, 400))
    pygame.draw.line(DISPLAY, color["black"], (300, 499), (800, 499))

# active b == inimigo
def draw_backg(active, select):
    # DESENHAR OS FUNDOS DE CARTA
    # desenha a partir do selecionado
    # 0 prim, 1 seg, 2 none
    if select == 2:
        DISPLAY.blit(CardImages[0], (30, 338))
        DISPLAY.blit(CardImages[0], (160, 338))
    elif select == 0: # selecionado o da esquerda
        DISPLAY.blit(CardImages[2], (30, 338))
        DISPLAY.blit(CardImages[0], (160, 338))
    elif select == 1: # selecionado o da esquerda
        DISPLAY.blit(CardImages[0], (30, 338))
        DISPLAY.blit(CardImages[2], (160, 338))
    DISPLAY.blit(CardImages[1], (30, 12))
    DISPLAY.blit(CardImages[1], (160, 12))
    # imprime o do meio de acordo com quem vai jogar
    # b == opponent
    if active != 'b':
        DISPLAY.blit(CardImages[0], (100, 175))
    else:
        DISPLAY.blit(CardImages[1], (100, 175))
    draw_board_backg()

# desenha peca em posicao
# usa o grid do tabuleiro para isso
def draw_peca(pos,peca):
    gridY = pos[0]*100
    gridX = pos[1]*100 + 300
    # peao azul, rei azul, peao vermelho, rei vermelho, vento
    # min azul, mai verm, w vento
    print_dict = "pkPKw"
    if peca == print_dict[0]:
        DISPLAY.blit(GridImages[0][0], (gridX, gridY))
    elif peca == print_dict[1]:
        DISPLAY.blit(GridImages[1][0], (gridX, gridY))
    elif peca == print_dict[2]:
        DISPLAY.blit(GridImages[0][1], (gridX, gridY))
    elif peca == print_dict[3]:
        DISPLAY.blit(GridImages[1][1], (gridX, gridY))
    elif peca == print_dict[4]:
        DISPLAY.blit(GridImages[4], (gridX, gridY))

    elif peca == 'g': # portao azul
        DISPLAY.blit(GridImages[2][0], (gridX, gridY))
    elif peca == 'G': # portao vermelho
        DISPLAY.blit(GridImages[2][1], (gridX, gridY))
    elif peca == 'n':  # nada
        DISPLAY.blit(GridImages[5], (gridX, gridY))

    elif peca == 's': # select
        DISPLAY.blit(GridImages[3][0], (gridX, gridY))
    elif peca == 'S': # selected
        DISPLAY.blit(GridImages[3][1], (gridX, gridY))

# função grafica que desenha as cartas
def draw_hands(active):
    # desenha a mao
    draw_card("a1", Mao_a[0], active)
    draw_card("a2", Mao_a[1], active)
    draw_card("c1", Mao_c[0], active)
    draw_card("b1", Mao_b[0], active)
    draw_card("b2", Mao_b[1], active)

####################
# criador de grid                                                   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# usa a grid pra desenhar as peças nos locais indicados
def create_grid():
    for X in range(0,5):
        for Y in range(0,5):
            if grid[X][Y] in ' _':
                draw_peca([X,Y],'n')
            if Y == 2:
                if X == 0:
                    draw_peca([X,Y], 'g')
                elif X == 4:
                    draw_peca([X, Y], 'G')
            if grid[X][Y] in "pkPKw":
                draw_peca([X,Y], grid[X][Y])

#########################################################
# botao
# (hover, click)
def button(x, y, w, h, ic, ac, text="", action=None):  # x, y, larg, alt, inactive color, active color
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # testa posicao mouse
        pygame.draw.rect(DISPLAY, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:  # testa clique
            action()
    else:  # desenha botao sem mouse hover
        pygame.draw.rect(DISPLAY, ic, (x, y, w, h))

    message_display(text, (x + (x + w)) / 2, (y + (y + h)) / 2, 22)  # texto

# botao invisivel
def button_invisible(x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 and action is not None:  # testa clique
            action()

#########################################################
# botao peca
# (hover, click)
def button_peca(x, y, w, h, image, action=None):  # x, y, larg, alt, cor, imagem, acao
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    draw_img(image, x, y)  # desenha imagem
    # usar com select e selected

    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # testa posicao mouse
        if click[0] == 1 and action is not None:  # testa clique
            action()

#########################################################
#########################################################
#########################################################
#########################################################
# FUNCAO ESPECIAL
# teste de cor
'''
Essa função não tem sentido pratico, serve apenas para testar a paleta de cor do jogo
Uma função semelhante é usada ao vencer o jogo
'''
def colortest():
    DISPLAY.fill(color["brown"])
    t = 0
    while t == 0 or t == 1:
        if t == 0:  # segue mouse
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                t = 1

            mouse = pygame.mouse.get_pos()
            sqX = mouse[0] + random.randint(-150, 150)
            sqY = mouse[1] + random.randint(-150, 150)
            keymapX = random.randint(0, 5)
            keymapY = random.randint(0, 4)
            sqColor = coolor[keymap[keymapX][keymapY]]
            draw_rect_zoado(sqX, sqY, sqColor)

            pygame.display.update()
            clock.tick(20)

        if t == 1:  # coolor
            DISPLAY.fill(color["brown"])
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                t = 0

            sqX = 0
            sqY = 0

            for i in range(0, 6):
                keymapX = i
                for u in range(0, 5):
                    keymapY = u
                    sqColor = coolor[keymap[keymapX][keymapY]]
                    draw_square100(sqX, sqY, sqColor)
                    sqX += 80
                sqX = 0
                sqY += 80

            xxx, yyy = 500, 100
            for liup in range(0,4):
                draw_img(CardImages[random.randint(0,2)], xxx, yyy)
                xxx += 50
                yyy += 50

            pygame.display.update()
            clock.tick(20)

    pygame.quit()
    quit()

##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##
#
#
#
# LOGIC
# LOGICA DO JOGO

############# GRID
# gera a grid na posicao inicial
grid = [[" " for i in range(5)] for j in range(5)]
grid[0][2], grid [4][2] = '_', '_'

############# PECAS
# gera as pecas na posicao original
# X,Y
blue_pawn = [[0,0],[1,0],[3,0],[4,0]]
blue_king = [[2,0]]
red_pawn = [[0,4],[1,4],[3,4],[4,4]]
red_king = [[2,4]]
wind_spirit = [[2,2]]
# ESQ-DIR
# CIMA-BAIXO
# L
pieces = [blue_pawn, blue_king, red_pawn, red_king, wind_spirit]  # lista de peças
# coloca as pecas na lista pieces
# qqr mudança na peça tbm muda a list
# funcao que coloca as peças na lista list
'''
A grid e a lista pieces são as variaveis centrais do jogo, é a partir delas que toda a lógica do jogo funciona
Elas certamente poderiam ser trabalhadas de formas mais eficientes
Uma funciona em função da outra nas ações do jogo
'''


# limpa a grid
def clean_grid():
    # limpa a grid
    for i in range(0,5): # vertical
        for u in range(0,5): # horizontal
            if (i == 0 or i == 4) and u == 2:
                grid[i][u] = '_'
            else:
                grid[i][u] = ' '

# faz update na grid a partir da lista de peças
def update_grid():
    clean_grid()

    print_dict = "pkPKw"
    for p_d in range(0,5):
        for i in range(len(pieces[p_d])):
            grid[pieces[p_d][i][1]] [pieces[p_d][i][0]] = print_dict[p_d]


############# MAO
Mao_a = [None, None]
Mao_b = [None, None]
Mao_c = [None]
# não tao utilizada quanto a grid/lista de peças, mas ainda essencial para o funcionamento do jogo

############# DICIONARIO DE CARTAS
'''
Esse dicionario contem todas as cartas utilizadas no jogo, 5 são escolhidas cada vez que vai se jogar
O objetivo original era ter uma ferramenta de escolha/criação de cartas, bem como novas cartas desbloqueadas conforme se vence partidas
Porem nada disso foi implementado
A string "n" é inutil nessa implementação
'''
cards = {"Tigre": ("n", (-2, 0), (1, 0)),
         "Dragão": ("n", (-1, -2), (-1, 2), (1, -1), (1, 1)),
         "Caranguejo": ("n", (0, -2), (0, 2), (-1, 0)),
         "Elefante": ("n", (-1, -1), (-1, 1), (0, -1), (0, 1)),
         "Sapo": ("n", (0, -2), (-1, -1), (1, 1)),
         "Louva Deus": ("n", (-1,-1), (-1,1), (1,0)),
         "Javali": ("n", (-1,0), (0,-1), (0,1)),
         "Macaco": ("n", (-1,-1), (-1,1), (1, -1), (1,1)),
         "Garça": ("n", (-1,0), (1,-1), (1,1)),
         "Cavalo": ("n", (-1,0), (0,-1), (1,0)),
         "Boi": ("n", (-1,0), (0,1), (1,0)),
         "Enguia": ("n", (-1,-1), (1,-1), (0,1)),
         "Cobra": ("n", (0,-1), (-1,1), (1,1)),
         "Coelho": ("n", (-1,1), (1,-1), (0,2)),
         "Ganso": ("n", (0,-1), (-1,-1), (0,1), (1,1)),
         "Galo": ("n", (0,-1), (1,-1), (0,1), (-1,1)),
         "Girafa": ("n", (1,0), (-1,-2), (-1,2)),
         "Kirin": ("n", (-2,-1), (-2,1), (2,0)),
         "Tartaruga": ("n", (0,-2), (0,2), (1,-1), (1,1)),
         "Fênix": ("n", (-1,-1), (-1,1), (1,-2), (1,2)),
         "Iguana": ("n", (-1,0), (-1,-2), (1,1)),
         "Tanuki": ("n", (-1,0), (1,-1), (0,2)),
         "Víbora": ("n", (-1,0), (0,-2), (1,1)),
         "Serpente": ("n", (-1,0), (0,2), (1,-1)),
         "Lontra": ("n", (-1,-1), (0,2), (1,1)),
         "Castor": ("n", (0,-2), (1,-1), (-1,1)),
         "Rato": ("n", (-1,0), (0,-1), (1,1)),
         "Camundongo": ("n", (-1,0), (0,1), (1,-1)),
         "Urso": ("n", (-1,0), (-1,-1), (1,1)),
         "Panda": ("n", (-1,0), (-1,1), (1,-1)),
         "Cão": ("n", (0,-1), (-1,-1), (1,-1)),
         "Raposa": ("n", (0,1), (-1,1), (1,1)),
         "Vespa": ("n", (-1,0), (1,0), (2,-2), (2,-1), (2,1), (2,2)),
         "Aranha": ("n", (-2,-2), (2,-2), (-2,2), (2,2)),
         "Libélula": ("n", (0,-2), (-1,-2), (0,2), (-1,2)),
         "Formiga": ("n", (-1,0), (0,-1), (0,1), (1,0)),
         "Besouro": ("n", (-1,0), (-1,-1), (-1,1)),
         "Mosca": ("n", (0,-2), (0,2), (1,-1), (1,1), (2,0)),
         "Escorpião": ("n", (1,0), (-2,-2), (-2,2)),
         "Rolabosta": ("n", (0,-1), (-1,-1), (-1,0)),
         "Caracol": ("n", (-1,0), (-1,1), (0,1)),
         "Centopéia": ("n", (0,-1), (0,-2), (-1,-2)),
         "Lacraia": ("n", (0,1), (0,2), (-1,2)),
         "Grilo": ("n", (1,0), (-1,-1), (-2,-2)),
         "Gafanhoto": ("n", (1,0), (-1,1), (-2,2)),
         "Abelha": ("n", (1,1), (-1,-2), (-2,-2)),
         "Mosquito": ("n", (1,-1), (-1,2), (-2,2)),
         "Urubu": ("n", (-1,0), (0,2), (0,-2)),
         "Siri": ("n", (0,1), (0,2), (0,-1), (0,-2)),
         "Gaivota": ("n", (0,-1), (0,1), (-1,2), (-1,-2)),
         "Morcego": ("n", (-1,2), (-1,-2), (1,-2), (1,2)),
         "Golfinho": ("n", (0,-2), (-1,-1), (1,-1)),
         "Tubarão": ("n", (0,2), (-1,1), (1,1)),
         "Jacaré": ("n", (-1,0), (0,-1), (0,-2)),
         "Crocodilo": ("n", (-1,0), (1,-1), (0,1), (0,2)),
         "Ovelha": ("n", (0,1), (1,0), (-1,-1)),
         "Bode": ("n", (-1,1), (0,-1), (1,0)),
         "Pardal": ("n", (1,1), (-1,-1), (-1,-2)),
         "Corvo": ("n", (-1,1), (-1,2), (1,-1)),
         "Pato": ("n", (-1,-1), (0,-2), (1,-2)),
         "Cisne": ("n", (-1,1), (0,2), (1,2)),
         "Emu": ("n", (-2,-1), (-1,-2), (1,2), (2,1)),
         "Avestruz": ("n", (-2,1), (-1,2), (1,-2), (2,-1)),
         "Carpa": ("n", (-2,-1), (-1,-2), (0,-2)),
         "Koi": ("n", (-2,1), (-1,2), (0,2)),
         "Pavão": ("n", (0,1), (-1,-1), (1,-2)),
         "Flamingo": ("n", (-1,1), (0,-2), (1,2)),
         "Masa": ("n", (-1,0), (-1,1), (-1,-1), (0,-1), (0,1)),
         "Mune": ("n", (-2,-1), (-2,-2), (-1,-2), (-2,1), (-2,2), (-1,2)),
         "Dromedário": ("n", (0,-1), (0,1), (1,0)),
         "Camelo": ("n", (0,-1), (1,-1), (0,1), (1,1)),
         "Capivara": ("n", (-1,0), (1,0), (1,-1), (1,1)),
         "Porco": ("n", (-1,0), (0,-1), (1,-1)),
         "Vaca": ("n", (-1,0), (0,1), (1,1)),
         "Jaguar": ("n", (1,0), (-2,-1)),
         "Onça": ("n", (-2,1), (1,0)),
         "Axolot": ("n", (-2,2), (-2,-2), (2,-1), (2,1)),
         "Lhama": ("n", (-1,2), (-1,-2), (1,-2), (1,2)),
         "Carcará": ("n", (-1,1), (-1,-1), (1,1), (1,-1)),
         "Cascavel": ("n", (-1,0), (0,-1), (0,1), (1,0))
         }

# função usada no inicio do jogo
# seleciona as 5 cartas do jogo e dá para os jogadores
def deal_hands():
    cardsNames = []
    for x, y in cards.items():
        cardsNames.append(str(x)) # bota todos os nomes no vetor
    # aleatoriza, pega a carta, tira do vetor
    randy = random.randint(1, len(cardsNames) - 1)
    Mao_a[0] = cardsNames[randy]
    cardsNames.remove(cardsNames[randy])
    randy = random.randint(1, len(cardsNames) - 1)
    Mao_a[1] = cardsNames[randy]
    cardsNames.remove(cardsNames[randy])
    randy = random.randint(1, len(cardsNames) - 1)
    Mao_c[0] = cardsNames[randy]
    cardsNames.remove(cardsNames[randy])
    randy = random.randint(1, len(cardsNames) - 1)
    Mao_b[0] = cardsNames[randy]
    cardsNames.remove(cardsNames[randy])
    randy = random.randint(1, len(cardsNames) - 1)
    Mao_b[1] = cardsNames[randy]
    cardsNames.remove(cardsNames[randy])

#####################################################################################
#####################################################################################
# variaveis centrais
# variaveis definidas no inicio do jogo
# certamente isso é uma má-pratica

deal_hands() # dá as cartas no inicio do jogo
ativo = 'a'  # começa com voce jogando (essa função acabou inutilizada)
selected_card = random.randint(0, 1)  # carta que voce selecionou (posicao)
selected_card_name = Mao_a[selected_card] # nome da carta
selected_piece = None
selected_type = None
selected_pos = None

enemy_bixo = None
enemy_card = None
enemy_move = None
s_card_v = None

winn = False

#####################################################################################
# FUNCOES DE BOTOES

# clica carda, esquerda ou direita
def click_card():
    mouseX, mouseY = pygame.mouse.get_pos()
    global selected_card, selected_card_name
    if 30 <= mouseX <= 130:
        selected_card = 0
        selected_card_name = Mao_a[0]
    elif 160 <= mouseX <= 260:
        selected_card = 1
        selected_card_name = Mao_a[1]

# botoes do tabuleiro, para selecioanr a peça certa
# button_peca(x, y, w, h, image, action=None)
def click_board():
    mouseX, mouseY = pygame.mouse.get_pos()
    global selected_piece, pieces, selected_type
    for x in range(300, 800, 100):
        for y in range(0, 500, 100):
            if x <= mouseX <= x+100 and y <= mouseY <= y+100:
                select_piece = [(x-300)//100, y//100]

                for p_d in range(2, 5):
                    for i in range(len(pieces[p_d])):
                        if select_piece[0] == pieces[p_d][i][0] and select_piece[1] == pieces[p_d][i][1]:
                            selected_piece = select_piece
                            selected_type = p_d

################################################## ESSA FUNÇÃO É O DNA DE TODA A LOGICA DO JOGO
########################## TESTPOS
'''
Testa a validade de cada movimento possivel, de acordo com a peça e carta selecionada
Retorna uma lista, a ser usada pra renderizar os botões de movimento
'''
def testpos_bound(bixo, carta):
    global cards, pieces, grid
    update_grid()
    listaa = []
    for pos in range(1, len(cards[carta])):
        newX = bixo[0] + cards[carta][pos][1]
        newY = bixo[1] + cards[carta][pos][0]
        if 0 <= newX <= 4 and 0 <= newY <= 4:
            if grid[newY][newX] in ' _pk':
                if grid[bixo[0]][bixo[1]] == 'w' and grid[newY][newX] == 'k':
                    pass
                else:
                    novoP = (newX, newY)
                    listaa.append(novoP)
    return listaa

# função botao especial, para selecionar os botões de peça e movimento
def button_peca_sel(x, y, w, h, image):  # x, y, larg, alt, cor, imagem, acao
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    draw_img(image, x, y)  # desenha imagem
    # usar com select e selected

    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # testa posicao mouse
        if click[0] == 1:  # testa clique
            xX = (x-300)//100
            yY = y//100

            move_piece_friend(selected_type, selected_piece, [xX, yY])
            turn_tick()

# desenhar os botões de movimento
def draw_move_buttons():
    button_peca((selected_piece[0] * 100) + 300, selected_piece[1] * 100, 100, 100, GridImages[3][1])
    listosa = testpos_bound(selected_piece, selected_card_name)
    for item in listosa:
        button_peca_sel((item[0] * 100) + 300, item[1] * 100, 100, 100, GridImages[3][0])

####################################                        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# função que roda um turno
# essa função é rodada depois de se fazer uma jogada
def turn_tick():
    global selected_card, selected_card_name, selected_piece, selected_type, selected_pos
    global enemy_bixo, enemy_card, enemy_move, s_card_v
    # não sei a necessidade dessa redefinição
    # certamente há formas melhores
    selected_piece = None
    selected_type = None
    selected_pos = None
    enemy_bixo = None
    enemy_card = None
    enemy_move = None
    s_card_v = None

    pygame.time.wait(30)
    swap_cards_friend() # troca a carta usada pela do meio
    update_grid()       # isso era pra dar um render
    test_win()          # testa se voce venceu o jogo
    enemy_type, enemy_bixo, enemy_card, enemy_move, s_card_v = sel_move_enemy() # seleciona o movimento do inimigo
    move_piece_enemy(enemy_type, enemy_bixo, enemy_move) # move a peca inimiga de acordo com a selecao
    pygame.time.wait(30)
    swap_cards_enemy() # troca a carta usada pela do meio
    update_grid() # isso era pra dar um render
    test_win()  # testa se o inimigo venceu o jogo

# testa a vitoria do jogo
def test_win():
    global pieces, winn
    if not pieces[0]: # se nao tem mais peoes inimigos
        winn = 'earth'
    elif not pieces[1]: # se nao tem mais sensei inimigo
        winn = 'fire'
    elif not pieces[2]: # se nao tem mais peoes amigos
        winn = 'Learth'
    elif not pieces[3]: # se nao tem mais sensei amigo
        winn = 'Lfire'
    else:
        if pieces[3]:
            if pieces[3][0] == [2,0]: # se seu sensei ta no portao iminigo
                winn = 'water'
        if pieces[4]:
            if pieces[4][0] == [2,0]: # se vento esta no portao iminigo
                winn = 'wind'
    if pieces[1]:
        if pieces[1][0] == [2,4]: # se sensei inimigo esta em seu portao
            winn = 'Lwater'
    if pieces[4]:
        if pieces[4][0] == [2,4]: # se vento esta em seu portao
            winn = 'Lwind'

    # SE VENCEU, IR PRO RENDER DE VITORIA  !!!!
    if winn:
        wincon()

# funcao que faz a troca da carta utilizada pela do meio
def swap_cards_friend():
    global selected_card, selected_card_name, Mao_a, Mao_c
    vaipramao = Mao_c[0]
    Mao_c[0] = selected_card_name
    Mao_a[selected_card] = vaipramao

# funcao que faz a troca da carta utilizada pela do meio
def swap_cards_enemy():
    global s_card_v, enemy_card, Mao_b, Mao_c
    vaipramao = Mao_c[0]
    Mao_c[0] = enemy_card
    Mao_b[s_card_v] = vaipramao

# IA do inimigo
'''
Essa função é extremamente simples, não tem nenhum tipo de avaliação de melhor movimento
Alem disso ela parece conter varios bugs, não me surpreenderia se maioria dos erros que acontecem são devido a ela
'''
def sel_move_enemy():
    sel_type = random.randint(0,1) # seleciona se vai jogar com peão ou sensei (vento não implementado)
    sel_bixo = pieces[sel_type][random.randint(0, len(pieces[sel_type])-1)] # seleciona a peça (caso mais de um peão)
    s_c_v = random.randint(0,1) # a carta selecionada (0 esq, 1 dir)
    sel_card = Mao_b[s_c_v] # nome da carta selecionada
    enemy_moves = testpos_bound_enemy(sel_bixo, sel_card) # testa a validade dos movimentos inimigos
    selel_move = [None, None]
    while len(enemy_moves[0])-1 < 1: # caso não haja nenhum movimento valido, repetir o processo
        if s_c_v == 0:
            s_c_v = 1
        elif s_c_v == 1:
            s_c_v = 0
        sel_card = Mao_b[s_c_v]
        enemy_moves = testpos_bound_enemy(sel_bixo, sel_card)
        selel_move = [None, None]
    else:
        random_rand = random.randint(0, len(enemy_moves)-1) # seleciona aleatoriamente um dos movimentos
    selel_move[0] = enemy_moves[random_rand][0]
    selel_move[1] = enemy_moves[random_rand][1]
    return sel_type, sel_bixo, sel_card, selel_move, s_c_v

# teste de movimentos validos pro oponente
# funcao importantissima e bugada kkkkkkkk
def testpos_bound_enemy(bixo, carta):
    global cards
    listaa = []
    for pos in range(1, len(cards[carta])):
        newX = bixo[0] - cards[carta][pos][1]
        newY = bixo[1] - cards[carta][pos][0]
        if 0 <= newX <= 4 and 0 <= newY <= 4:
            if grid[newY][newX] in ' _PK':
                if grid[bixo[0]][bixo[1]] == 'w' and grid[newY][newX] == 'K':
                    pass
                else:
                    novoP = (newX, newY)
                    listaa.append(novoP)
    return listaa


############################################################################################ !@!!!!!!!!!!!!!!!!!!!!!!!1
### MOVIMENTO
'''
essa função que faz o movimento das peças
para isso ela faz uam troca das listas de peças, eliminando a antiga e appendando a nova conforme ncessario
bastante bugs, como é de praxe
alem disso, varias regras de jogo em relação a movimento do vento estão implementadas de forma distinta do boardgame original
'''
# movimento do amigo
# type : de onde veio a peca [2]peao : [3]sensei : [4]vento
def move_piece_friend(piecetype, oldpiece, nextpiece):
    global pieces
    windtarget = 0  # se o alvo é um vento ou nao
    if oldpiece in pieces[piecetype]:
        if piecetype != 4: # se não vento
            if nextpiece in pieces[0]:
                pieces[0].remove(nextpiece)
            if nextpiece in pieces[1]:
                pieces[1].remove(nextpiece)
            if nextpiece in pieces[4]: # se o alvo é vento (nao implementado)
                windtarget = 1
                pieces[4] = []
            if windtarget == 1:
                pieces[4].append(oldpiece)
        else: # se vento
            if nextpiece in pieces[0]:
                pieces[0].remove(nextpiece)
                pieces[0].append(oldpiece)
        pieces[piecetype].remove(oldpiece)
        pieces[piecetype].append(nextpiece)

# movimento do oponente
# type : de onde veio a peca [0]peao : [1]sensei : [4]vento
def move_piece_enemy(piecetype, oldpiece, nextpiece):
    global pieces
    windtarget = 0  # se o alvo é um vento ou nao
    if oldpiece in pieces[piecetype]:
        if piecetype != 4:
            if nextpiece in pieces[2]:
                pieces[2].remove(nextpiece)
            if nextpiece in pieces[3]:
                pieces[3].remove(nextpiece)
            if nextpiece in pieces[4]:
                windtarget = 1
                pieces[4] = []
            if windtarget == 1:
                pieces[4].append(oldpiece)
        else:
            if nextpiece in pieces[4]:
                pieces[4].remove(nextpiece)
                pieces[4].append(oldpiece)
        pieces[piecetype].remove(oldpiece)
        pieces[piecetype].append(nextpiece)

#############################################################    !@!!!!!!!!!!!!!!!!!!!!!!!1
#############################################################                 !@!!!!!!!!!!!!!!!!!!!!!!!1
#############################################################     !@!!!!!!!!!!!!!!!!!!!!!!!1
#############################################################                 !@!!!!!!!!!!!!!!!!!!!!!!!1
#############################################################     !@!!!!!!!!!!!!!!!!!!!!!!!1
'''
função que renderiza a tela
cria o background, as cartas, o tabuleiro, etc
'''
# renderizar tela
def render_game():
    global ativo, selected_card, selected_piece
    draw_backg(ativo, selected_card)
    draw_hands(ativo)

    update_grid()
    create_grid()

    # botao das carta
    button_invisible(30, 338, 100, 150, click_card)
    button_invisible(160, 338, 100, 150, click_card)
    button_invisible(300, 0, 500, 500, click_board)

    if selected_piece:
        draw_move_buttons()
        # testbound, test friendly
        # cria botao nos possiveis
        # botoes clicaveis rodam a parada

    # display update, importantissimo
    pygame.display.update()

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
# LOOPS PRINCIPAIS
# LOOPS DE JOGO QUE RODAM GRAFICOS

# tela de introdução
def game_intro():
    intro = True
    while intro:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                colortest()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        DISPLAY.fill(color["white"])
        draw_img(BackGround[0], 150, 0)
        button(300, 325, 170, 100, coolor['a1'],coolor['a3'], "Iniciar!", game_loop)
        # display update, importantissimo
        pygame.display.update()

    pygame.quit()
    quit()

# loop principal do jogo
gloop = True
def game_loop():
    global gloop
    listosa = []
    global grid, pieces, selected_card, selected_card_name, selected_piece, selected_pos, selected_type
    global enemy_bixo, enemy_card, enemy_move

    while gloop:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouseX,mouseY = pygame.mouse.get_pos()
        DISPLAY.fill(color["white"])
        draw_img(BackGround[1], 150, 0)
        render_game()


    pygame.quit()
    quit()

# tela de vitoria/derrota
def wincon():
    global winn, gloop

    winning = True
    gloop = False
    listosa = []
    DISPLAY.fill(color["white"])
    draw_img(BackGround[1], 150, 0)
    while winning:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if winn[0] == 'L':
            message_display('VOCÊ PERDEU !', 400, 200, 50)
            if winn[1:] == 'wind':
                message_display('Caminho das Nuvens', 400, 300, 20)
            elif winn[1:] == 'earth':
                message_display('Caminho das Pedras', 400, 300, 20)
            elif winn[1:] == 'fire':
                message_display('Caminho das Chamas', 400, 300, 20)
            elif winn[1:] == 'water':
                message_display('Caminho do Rio', 400, 300, 20)
        else:
            message_display('VOCÊ VENCEU !', 400, 200, 50)
            if winn[0:] == 'wind':
                message_display('Caminho das Nuvens', 400, 300, 20)
            elif winn[0:] == 'earth':
                message_display('Caminho das Pedras', 400, 300, 20)
            elif winn[0:] == 'fire':
                message_display('Caminho das Chamas', 400, 300, 20)
            elif winn[0:] == 'water':
                message_display('Caminho do Rio', 400, 300, 20)

        mouse = pygame.mouse.get_pos()
        sqX = mouse[0] + random.randint(-100, 100)
        sqY = mouse[1] + random.randint(-100, 100)
        keymapX = random.randint(0, 5)
        keymapY = random.randint(0, 4)
        sqColor = coolor[keymap[keymapX][keymapY]]
        draw_rect_zoado(sqX, sqY, sqColor)

        pygame.display.update()
        clock.tick(20)

    pygame.quit()
    quit()

#####################################################################################
#####################################################################################
# PROGRAMA

# o jogo roda a partir daqui
game_intro()


