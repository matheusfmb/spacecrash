import random
import pygame
import sys
pygame.init()

#CONTROLE DE FPS
clock = pygame.time.Clock()

#VARÍAVEIS DA TELA DO JOGO
sizex = 360
sizey = 640
janela = pygame.display.set_mode((sizex,sizey))
titulo = pygame.display.set_caption("SPACE CRASH")

#CENÁRIO DO JOGO E VARIÁVEIS PARA ANIMAR A CENA.
background = pygame.image.load("assets/cenario/nebula.jpg")
cena = 0
sizey_cena = 640

#IMAGEM PARA O MENU DE START E VARIÁVEL PARA FAZER CONTROLE DE TELA
backstart = pygame.image.load("assets\cenario\startmenu.jpg")
start = True

#IMAGEM DO BOTÃO PAUSE E VARIÁVEL PARA CONTROLE DE TELA DO PAUSE
stop = True
pauseimage = pygame.image.load("assets/cenario/pause.png")

#GAME OVER CONTROLE DE TELA
gameover = True
overimage = pygame.image.load("assets\cenario\gameover.jpg")
cute = pygame.image.load("assets/cenario/cute.png")
fx_over = pygame.mixer.Sound('assets\musicas\GAMEOVERSOUND.wav')
pygame.mixer.Sound.set_volume(fx_over, 0.3)
play_again = True


#MÚSICA
musica_fundo = pygame.mixer.music.load("assets/musicas/start.wav")
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(-1)

#VARIÁVEIS DA MOEDA - PONTUAÇÃO
score = 0
coin = pygame.image.load("assets/meteoros/coin.png")
coin_x = random.randrange(0,sizex-40)
coin_y = -40
velocidade_coin = 1.5
font = pygame.font.Font("assets/04B_30__.TTF",28)
text = font.render("score: " + str(score), True, (255,225,225))
pos_coin = []
pos_coin.append(coin_x)

#POSIÇÃO COIN
def coin_blit():
    janela.blit(coin,(coin_x,coin_y))
    janela.blit(text,(10,10))

#CARREGANDO IMAGEM DA NAVE E DEFININDO AS VARIÁVEIS PARA MOVIMENTO
nave = pygame.image.load("assets/nave/spaceShips_008.png")
laser = pygame.image.load("assets/nave/laserRed07.png")
velocidade_laser = 4
velocidade_nave = 2
nave_x = 160
laser_x = nave_x+25
nave_y = 570
laser_y = nave_y - 50
nave_rect = 0
nave_moveup = False
nave_movedown = False
nave_moveright = False
nave_moveleft = False

#POSIÇÃO DA NAVE NA TELA
def nave_blit():
    janela.blit(nave,(nave_x,nave_y))
    janela.blit(laser,(laser_x,laser_y))

#METEOROS CARREGANDO IMAGEM E DEFININDO VARIÁVEIS PARA MOVIMENTO
velocidade_meteoro = 2.5
velocidade_plus = random.uniform(0,1.5)
velocidade_down = random.random()

meteoro1 = pygame.image.load("assets\meteoros\meteoro1.png")
meteoro_1x = random.randrange(0,sizex-40)
meteoro_1y = 10

meteoro2 = pygame.image.load("assets\meteoros\meteoro2.png")
meteoro_2x = random.randrange(0,sizex-40)
meteoro_2y = 10

meteoro3 = pygame.image.load("assets\meteoros\meteoro3.png")
meteoro_3x = random.randrange(0,sizex-40)
meteoro_3y = 10

meteoro4 = pygame.image.load("assets\meteoros\meteoro2.png")
meteoro_4x = random.randrange(0,sizex-40)
meteoro_4y = 10

pos_meteoro = []
pos_meteoro.append(meteoro_1x)
pos_meteoro.append(meteoro_2x)
pos_meteoro.append(meteoro_3x)
pos_meteoro.append(meteoro_4x)

# POSIÇÃO DO METEORO NA TELA
def meteoro_blit():
    janela.blit(meteoro1,(meteoro_1x,meteoro_1y))
    janela.blit(meteoro2,(meteoro_2x,meteoro_2y))
    janela.blit(meteoro3,(meteoro_3x,meteoro_3y))
    if score >= 10:
        janela.blit(meteoro4,(meteoro_4x,meteoro_4y))

#POSIÇÃO DOS RECTS REFERENTE AOS ELEMENTOS DO JOGO
def rect():
    global meteoro1_rect
    global meteoro2_rect
    global meteoro3_rect
    global meteoro4_rect
    global nave_rect
    global coin_rect
    global score
    global laser_rect
    meteoro1_rect = pygame.draw.rect(janela,(225,0,0),(meteoro_1x+5,meteoro_1y,43,43),1,-3,40,40,40,40)
    meteoro2_rect = pygame.draw.rect(janela,(225,0,0),(meteoro_2x,meteoro_2y,43,43),1,-3,40,40,40,40)
    meteoro3_rect = pygame.draw.rect(janela,(225,0,0),(meteoro_3x,meteoro_3y,43,43),1,-3,40,40,40,40)
    meteoro4_rect = pygame.draw.rect(janela,(225,0,0),(meteoro_4x,meteoro_4y,43,43),1,-3,40,40,40,40)
    nave_rect = pygame.draw.rect(janela,(225,0,0),(nave_x+10,nave_y,40,49),1,-1,10000,10000,4,4)
    coin_rect = pygame.draw.rect(janela,(225,0,0),(coin_x,coin_y,40,40),1,-3,40,40,40,40)
    laser_rect = pygame.draw.rect(janela,(225,0,0),(laser_x,laser_y,9,37),1,-3)

# DEFININDO COLISÃO
def colisao():
    global gameover
    global play_again
    global meteoro_3y
    global meteoro_2y
    global meteoro_1y
    global start
    global velocidade_meteoro
    global nave_x
    global nave_y
    global coin_y
    global score
    global coin_x
    global text
    global meteoro_1x
    global meteoro_2x
    global meteoro_3x
    global meteoro_4x
    global meteoro_4y

    if nave_rect.colliderect(meteoro1_rect) or nave_rect.colliderect(meteoro2_rect) or nave_rect.colliderect(meteoro3_rect) or nave_rect.colliderect(meteoro4_rect):
        gameover = False
        play_again = False
        meteoro_1y = 10
        meteoro_2y = 10
        meteoro_3y = 10
        meteoro_4y = 10
        coin_y = -150
        nave_x = 160
        nave_y = 550
        fx_over.play()

    if nave_rect.colliderect(coin_rect):
        coin_x = random.randrange(0,sizex-40)
        coin_y = -150
        score+=1
        text = font.render("score: " + str(score), True, (255,225,225))

    if laser_rect.colliderect(meteoro1_rect):
        meteoro_1y = -150
        meteoro_1x = random.randrange(0,sizex-40) 
        if meteoro_1x in pos_meteoro:
            meteoro_1x = random.randrange(0,sizex-40) 
    if laser_rect.colliderect(meteoro2_rect):
        meteoro_2y = -150
        meteoro_2x = random.randrange(0,sizex-40) 
        if meteoro_2x in pos_meteoro:
            meteoro_2x = random.randrange(0,sizex-40)  
    if laser_rect.colliderect(meteoro3_rect):
        meteoro_3y = -150
        meteoro_3x = random.randrange(0,sizex-40) 
        if meteoro_3x in pos_meteoro:
            meteoro_3x = random.randrange(0,sizex-40) 
    if laser_rect.colliderect(meteoro4_rect):
        meteoro_4y = -150
        meteoro_4x = random.randrange(0,sizex-40) 
        if meteoro_4x in pos_meteoro:
            meteoro_4x = random.randrange(0,sizex-40)
    
#DESENHANDO NA TELA - A FUNÇÃO DRAW É A ÚNICA QUE ENTRA NO LOOP DO JOGO. TODAS AS FUNÇÕES PRECISAM SER CHAMADAS DENTRO DELA.
def draw():
    global start
    global cena
    global sizey_cena
    global nave_rect
    global score
    global text 

    if gameover:
        if start:
            score = 0
            text = font.render("score: " + str(score), True, (255,225,225))
            janela.blit(backstart,(0,0))
        elif start == False:
            rect()
            janela.blit(background,(0,cena))
            janela.blit(background,(0,-sizey_cena+cena))#CRIANDO OUTRA CENA EM CIMA DA CENA E AUMENTNDO 1 PIXEL NA PRINCIPAL E DIMINUINDO 1 PIXEL NA SECUNDÁRIA.
            if stop == False:
                janela.blit(pauseimage,(310,10))
            #FAZENDO EFEITO DE MOVIMENTO NA CENA
            if cena == sizey_cena:
                cena = 0
            if stop:
                cena+=1
            #DECLARANDO AS OUTRAS FUNÇÕES
            meteoro_blit() #POSIÇÃO DO METEORO NA TELA
            nave_blit() #POSIÇÃO DA NAVE NA TELA
            move_nave() #MOVIMENTAÇÃO DA NAVE
            move_ast_coin_laser() #MOVIMENTAÇÃO DOS METEOROS
            colisao()#COLISÃO
            coin_blit() #COIN 
    else:
        pygame.time.delay(200)
        janela.blit(overimage,(0,0))
        janela.blit(text,(100,400))
        janela.blit(cute,(100,80))
        pygame.mixer.music.stop()

# DEFININDO MOVIMENTAÇÃO DOS METEOROS
def move_ast_coin_laser():
    global meteoro_1y
    global meteoro_2y
    global meteoro_3y
    global meteoro_1x
    global meteoro_2x
    global meteoro_3x
    global velocidade_meteoro
    global velocidade_down
    global velocidade_plus
    global velocidade_coin
    global coin_y
    global coin_x
    global laser_y
    global laser_x
    global meteoro_4x
    global meteoro_4y

    if start == False and gameover:
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
                velocidade_plus = random.uniform(0,1.2)
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

        if score >= 10:
            meteoro_4y+=(velocidade_meteoro+velocidade_plus)
            if meteoro_4y > sizey:
                meteoro_4y = 10
                meteoro_4x = random.randrange(0,sizex-40)
                if stop:
                    velocidade_plus = random.random()
                if meteoro_4x in pos_meteoro:
                    meteoro_4x = random.randrange(0,sizex-40)
                else:
                    pos_meteoro.append(meteoro_4x)

        coin_y += velocidade_coin
        if coin_y > sizey:
            coin_y = -150
            coin_x = random.randrange(0,sizex-40)
            if coin_x in pos_coin:
                coin_x = random.randrange(0,sizex-40)
        laser_y -= velocidade_laser
        if laser_y < -600:
            laser_x = nave_x + 25
            laser_y = nave_y - 50
        
        if len(pos_coin) > 20:
            pos_coin.clear()
        if len(pos_meteoro) > 50:
            pos_meteoro.clear()

# DEFININDO MOVIMENTAÇÃO DA NAVE
def move_nave():
    global nave_x
    global nave_y
    global velocidade_nave
    global laser_x
    global laser_y

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
    clock.tick(165)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if play_again == False:
                    play_again = True
                    gameover = True
                    start = True
                    pygame.mixer.music.play()
            if evento.key == pygame.K_BACKSPACE:
                if stop and start == False and gameover:
                    stop = False
                    velocidade_nave = 0
                    velocidade_meteoro = 0
                    velocidade_plus = 0
                    velocidade_down = 0
                    velocidade_coin = 0
                    velocidade_laser = 0
                elif stop == False:
                    stop = True
                    velocidade_nave = 2
                    velocidade_meteoro = 2.5
                    velocidade_plus = random.uniform(0,1.2)
                    velocidade_down = random.random()
                    velocidade_coin = 1.5
                    velocidade_laser = 4
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