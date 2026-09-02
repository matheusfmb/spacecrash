"""
Configurações do jogo.
"""

# TELA
SCREEN_W = 360
SCREEN_H = 640
FPS_CAP = 165
TITLE = "SPACE CRASH"

# CORES
WHITE_TEXT = (255, 225, 225)

# VELOCIDADES (em pixels por segundo)
SHIP_SPEED = 330.0
METEOR_SPEED = 412.5
COIN_SPEED = 247.5
LASER_SPEED = 660.0
BACKGROUND_SPEED = 165.0

# Variação aleatória de velocidade dos meteoros "2" e "4" (soma) e "3" (subtrai)
METEOR_VARIANCE_PLUS_MAX = 247.5
METEOR_VARIANCE_DOWN_MAX = 165.0

# LIMITES DE MOVIMENTO DA NAVE
SHIP_X_MIN = 0
SHIP_X_MAX = 300
SHIP_Y_MIN = 0
SHIP_Y_MAX = 580
SHIP_START_X = 160
SHIP_START_Y = 570

# REGRAS DE JOGO
STARTING_LIVES = 3
METEOR4_UNLOCK_SCORE = 10

# PISCA DA NAVE AO LEVAR UM HIT (não fatal)
SHIP_FLASH_DURATION = 0.9   
SHIP_FLASH_INTERVAL = 0.1   

# ANIMAÇÃO DE MORTE (quando a última vida se vai): a nave explode onde estava
SHIP_DEATH_EXPLOSION_RADIUS = 46
SHIP_DEATH_FRAME_DURATION = 0.06

# ÁUDIO
# MUSIC_VOLUME e DEFAULT_SFX_VOLUME
MUSIC_VOLUME = 0.01
DEFAULT_SFX_VOLUME = 1.0
VOLUME_STEP = 0.05

# Volume "base" de cada efeito — o volume final tocado é
GAMEOVER_SFX_VOLUME = 0.8     
METEOR_HIT_SFX_VOLUME = 0.9    
COIN_SFX_VOLUME = 0.7

SAVE_FILE = "save_settings.json"

# CRÉDITO NA TELA DE GAME OVER
CREDIT_TEXT = "Refatorado por Matheus 2026"
CREDIT_FONT_SIZE = 14

# TRANSIÇÃO (fade) ENTRE TELAS
FADE_DURATION = 0.3  # segundos

# ÍCONE E DICA DE ÁUDIO NO MENU
AUDIO_ICON_SIZE = 30
AUDIO_HINT_TEXT = "O: ABRIR AUDIO"
AUDIO_HINT_FONT_SIZE = 12
OPTIONS_HINT_FONT_SIZE = 12

# ÍCONE E MODAL DE CONTROLES NO MENU (fica acima do ícone de áudio)
CONTROLS_HINT_TEXT = "C: CONTROLES"
CONTROLS_MODAL_TITLE = "CONTROLES"
CONTROLS_LINES = [
    "SETAS: MOVER NAVE",
    "BACKSPACE: PAUSAR",
    "O: MENU DE AUDIO",
    "Q: MENU (QUANDO PAUSADO)",
    "ENTER: CONFIRMAR",
]
CONTROLS_MODAL_W = 300
CONTROLS_MODAL_H = 300

# MODAL DO MENU DE OPÇÕES (aparece por cima do menu, sem esconder o fundo)
MODAL_W = 300
MODAL_H = 260
MODAL_COLOR = (12, 14, 30)
MODAL_OPACITY = 255  

# ÍCONE DE VOLTAR AO MENU (ao lado do ícone de pause) E MODAL DE CONFIRMAÇÃO
QUIT_ICON_MARGIN = 10
QUIT_CONFIRM_TITLE = "VOLTAR AO MENU?"
QUIT_CONFIRM_HINT = "ENTER: SIM   ESC: NAO"
QUIT_MODAL_W = 260
QUIT_MODAL_H = 140

# CAMINHOS DE ASSETS (relativos à pasta assets/)
FONT_PATH = "04B_30__.TTF"
FONT_SIZE = 28

SHIP_IMAGE = "nave/spaceShips_008.png"
LASER_IMAGE = "nave/laserRed07.png"

METEOR_IMAGES = [
    "meteoros/meteoro1.png",
    "meteoros/meteoro2.png",
    "meteoros/meteoro3.png",
    "meteoros/meteoro4.png",
]
COIN_IMAGE = "meteoros/coin.png"

LIFE_IMAGES = [f"vidas/vida{i}.png" for i in range(1, 5)]

BACKGROUND_IMAGE = "cenario/nebula.jpg"
MENU_IMAGE = "cenario/startmenu.jpg"
PAUSE_IMAGE = "cenario/pause.png"
GAMEOVER_IMAGE = "cenario/gameover.jpg"
AUDIO_ICON_IMAGE = "cenario/audioOn.png"
JOYSTICK_IMAGE = "cenario/joystick.png"
RETURN_ICON_IMAGE = "cenario/return.png"

MUSIC_START = "musicas/start.wav"
SOUND_GAMEOVER = "musicas/GAMEOVERSOUND.wav"
SOUND_COIN = "musicas/fx_coin.wav"
SOUND_METEOR_HIT = "musicas/footstep_carpet_002.ogg"
