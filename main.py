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

#PAUSE
stop = True
pauseimage = pygame.image.load("assets/cenario/pause.png")


#MÚSICA
musica_fundo = pygame.mixer.music.load("assets/musicas/start.wav")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)


#CARREGANDO IMAGEM DA NAVE E DEFININDO AS VARIÁVEIS PARA MOVIMENTO
nave = pygame.image.load("assets/nave/spaceShips_008.png")
velocidade_nave = 2
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
velocidade_meteoro = 2.5
velocidade_plus = random.uniform(0,1.5)
velocidade_down = random.random()

meteoro1 = pygame.image.load("assets\meteoros\meteoro1.png")
meteoro_1x = random.randrange(0,sizex-40)
meteoro_1y = 10

meteoro2 = pygame.image.load("assets\meteoros\meteoro1.png")
meteoro_2x = random.randrange(0,sizex-40)
meteoro_2y = 10

meteoro3 = pygame.image.load("assets\meteoros\meteoro1.png")
meteoro_3x = random.randrange(0,sizex-40)
meteoro_3y = 10

pos_meteoro = []
pos_meteoro.append(meteoro_1x)
pos_meteoro.append(meteoro_2x)
pos_meteoro.append(meteoro_3x)

#POSIÇÃO DO METEORO NA TELA
def meteoro_blit():
    janela.blit(meteoro1,(meteoro_1x,meteoro_1y))
    janela.blit(meteoro2,(meteoro_2x,meteoro_2y))
    janela.blit(meteoro3,(meteoro_3x,meteoro_3y))
    
#DESENHANDO NA TELA - A FUNÇÃO DRAW É A ÚNICA QUE ENTRA NO LOOP DO JOGO. TODAS AS FUNÇÕES PRECISAM SER CHAMADAS DENTRO DELA.
def draw():
    global start
    global cena
    global sizey_cena
    if start:
        janela.blit(backstart,(0,0))
    else:
        janela.blit(bg,(0,cena))
        janela.blit(bg,(0,-sizey_cena+cena))#CRIANDO OUTRA CENA EM CIMA DA CENA E AUMENTNDO 1 PIXEL QUANDO A CENA "PERDE 1 PIXEL"
        if stop == False:
            janela.blit(pauseimage,(5,10))
        #FAZENDO EFEITO DE MOVIMENTO NA CENA
        if cena == sizey_cena:
            cena = 0
        cena+=1
        #DECLARANDO AS OUTRAS FUNÇÕES
        meteoro_blit() #POSIÇÃO DO METEORO NA TELA
        nave_blit() #POSIÇÃO DA NAVE NA TELA
        move_nave() #MOVIMENTAÇÃO DA NAVE
        move_ast() #MOVIMENTAÇÃO DOS METEOROS

#DEFININDO MOVIMENTAÇÃO DOS METEOROS
def move_ast():
    global meteoro_1y
    global meteoro_2y
    global meteoro_1x
    global meteoro_2x
    global meteoro_3x
    global meteoro_3y
    global velocidade_meteoro
    global velocidade_down
    global velocidade_plus

    meteoro_1y += velocidade_meteoro
    if meteoro_1y > sizey:
        meteoro_1y = 10
        meteoro_1x = random.randrange(0,sizex-40)
        if meteoro_1x in pos_meteoro:
            meteoro_1x = random.randrange(0,sizex-40)
        else:
            pos_meteoro.append(meteoro_1x)
    
    meteoro_2y += (velocidade_meteoro+velocidade_plus)
    if meteoro_2y > sizey:
        meteoro_2y = 10
        meteoro_2x = random.randrange(0,sizex-40)
        if stop:
            velocidade_plus = random.uniform(0,1.5)
        if meteoro_2x in pos_meteoro:
            meteoro_2x = random.randrange(0,sizex-40)
        else:
            pos_meteoro.append(meteoro_2x)

    meteoro_3y += (velocidade_meteoro-velocidade_down)
    if meteoro_3y > sizey:
        meteoro_3y = 10
        meteoro_3x = random.randrange(0,sizex-40)
        if stop:
            velocidade_down = random.random()
        if meteoro_3x in pos_meteoro:
            meteoro_3x = random.randrange(0,sizex-40)
        else:
            pos_meteoro.append(meteoro_3x)
    

    if len(pos_meteoro) > 30:
        pos_meteoro.clear()

#DEFININDO MOVIMENTAÇÃO DA NAVE
def move_nave():
    global nave_x
    global nave_y
    global velocidade_nave

    if nave_moveup:
        nave_y -= velocidade_nave
    if nave_movedown:
        nave_y += velocidade_nave
    if nave_moveleft:
        nave_x -= velocidade_nave
    if nave_moveright:
        nave_x += velocidade_nave
    
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
            if evento.key == pygame.K_BACKSPACE:
                if stop:
                    stop = False
                    velocidade_nave = 0
                    velocidade_meteoro = 0
                    velocidade_plus = 0
                    velocidade_down = 0
                elif stop == False:
                    stop = True
                    velocidade_nave = 2
                    velocidade_meteoro = 2.5
                    velocidade_plus = random.uniform(0,1.5)
                    velocidade_down = random.random()
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