import random
import pygame
import sys

pygame.init()

#VARÍAVEIS DA TELA DO JOGO
sizex = 360
sizey = 640
janela = pygame.display.set_mode((sizex,sizey))
titulo = pygame.display.set_caption("SPACE CRASH")

#CENÁRIO DO JOGO E VARIÁVEIS PARA ANIMAR A CENA.
background = pygame.image.load("assets/cenario/nebula.png")
bg = pygame.transform.scale(background,(360,640))
cena = 0
sizey_cena = 640

#CENÁRIO - START MENU
backstart = pygame.image.load("assets/cenario/startmenu.png")
start = True

#MÚSICA
musica_fundo = pygame.mixer.music.load("assets\musicas\start.wav")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)


#CARREGANDO IMAGEM DA NAVE E DEFININDO AS VARIÁVEIS PARA MOVIMENTO
nave = pygame.image.load("assets/nave/spaceShips_008.png")
nave_x = 160
nave_y = 550
nave_moveup = False
nave_movedown = False
nave_moveright = False
nave_moveleft = False

#POSIÇÃO DA NAVE NA TELA
def nave_blit():
    janela.blit(nave,(nave_x,nave_y))


#METEOROS CARREGANDO IMAGEM E DEFININDO VARIÁVEIS PARA MOVIMENTO
meteoro1 = pygame.image.load("assets\meteoros\meteoro1.png")
meteoro_1x = random.randrange(0,sizex-40)
meteoro_1y = 10
velocidade = 2.5

meteoro2 = pygame.image.load("assets\meteoros\meteoro1.png")
meteoro_2x = random.randrange(0,sizex-40)
meteoro_2y = 10

#POSIÇÃO DO METEORO NA TELA
def meteoro_blit():
    janela.blit(meteoro1,(meteoro_1x,meteoro_1y))
    janela.blit(meteoro2,(meteoro_2x,meteoro_2y))
    
#DESENHANDO NA TELA - A FUNÇÃO DRAW É A ÚNICA QUE ENTRA NO LOOP DO JOGO. TODAS AS FUNÇÕES PRECISAM SER CHAMADAS DENTRO DELA.
def draw():
    global start
    global cena
    global sizey_cena
    if start:
        janela.blit(backstart,(0,0))
    else:
        janela.blit(bg,(0,cena))
        janela.blit(bg,(0,-sizey_cena+cena))#CRIANDO OUTRA CENA EM CIMA DA CENA
        #FAZENDO EFEITO DE MOVIMENTO NA CENA
        if cena == sizey_cena:
            cena = 0
        cena+=1
        #DECLARANDO AS OUTRAS FUNÇÕES
        meteoro_blit()
        nave_blit()
        move_nave()
        move_ast()

#DEFININDO MOVIMENTAÇÃO DOS METEOROS
def move_ast():
    velocidade = 2.5
    global meteoro_1y
    global meteoro_1x
    global meteoro_2y
    global meteoro_2x
    meteoro_1y += velocidade
    if meteoro_1y > sizey:
        meteoro_1y = 10
        meteoro_1x = random.randrange(0,sizex-40)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    meteoro_2y += velocidade
    if meteoro_2y > sizey:
        meteoro_2y = 10
        meteoro_1x = random.randrange(0,sizex-40)
    

#DEFININDO MOVIMENTAÇÃO DA NAVE
def move_nave():
    global nave_x
    global nave_y

    if nave_moveup:
        nave_y -= 1.5
    if nave_movedown:
        nave_y += 1.5
    if nave_moveleft:
        nave_x -= 1.5
    if nave_moveright:
        nave_x += 1.5
    
    if nave_y <= 0:
        nave_y = 0
    elif nave_y >= 580:
        nave_y = 580
    if nave_x <= 0:
        nave_x = 0
    elif nave_x >= 300:
        nave_x = 300


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                start = False
            if evento.key == pygame.K_UP:
                nave_moveup = True
            if evento.key == pygame.K_DOWN:
                nave_movedown = True
            if evento.key == pygame.K_LEFT:
                nave_moveleft = True
            if evento.key == pygame.K_RIGHT:
                nave_moveright = True
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_UP:
                nave_moveup = False
            if evento.key == pygame.K_DOWN:
                nave_movedown = False
            if evento.key == pygame.K_LEFT:
                nave_moveleft = False
            if evento.key == pygame.K_RIGHT:
                nave_moveright = False
    draw()
    pygame.display.update()