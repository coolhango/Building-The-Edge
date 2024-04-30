# arquivo responsavel pela configuração do jogo
import pygame

pygame.init()
pygame.mixer.init()
# variaveis gerais
fps = 60
widht = 800
height = 600
TILESIZE = 64
titulo = "Building edge"
filename = "scores.txt"
bg = pygame.image.load("resources/img/bg/bg-1.png")
bg_game = pygame.image.load("resources/img/bg/bg-2.png")
fonte_menu = pygame.font.Font("resources/Font/olympiccarrierhalfital.ttf", 85)
fonte_start = pygame.font.Font("resources/Font/olympiccarrierhalfital.ttf", 50)
fonte_timer = pygame.font.Font("resources/Font/olympiccarrierhalfital.ttf", 25)

# variaveis do jogador
aceleracao_jogador = 0.6
atrito_jogador = -0.15
gravidade = 1

# imagens e sons
Icon = pygame.image.load("resources/img/icon/icon.jpg")  # importando imagem que sera usada para o icone
pygame.display.set_icon(Icon)  # escolhendo  o icone do jogo com a imagem ja importada
pygame.mouse.set_visible(False)  # Altera a visibilidade do mouse, true = visivel, false = invisivel.
run = [pygame.image.load("resources/img/player/run/run-1.png"), pygame.image.load("resources/img/player/run/run-2.png"),
       pygame.image.load("resources/img/player/run/run-3.png"), pygame.image.load("resources/img/player/run/run-4.png")]
stop = [pygame.image.load("resources/img/player/idle/idle-1.png"),
        pygame.image.load("resources/img/player/idle/idle-2.png"),
        pygame.image.load("resources/img/player/idle/idle-3.png"),
        pygame.image.load("resources/img/player/idle/idle-4.png")]
jump = [pygame.image.load("resources/img/player/jump/jump-1.png"),
        pygame.image.load("resources/img/player/jump/jump-2.png"),
        pygame.image.load("resources/img/player/jump/jump-3.png"),
        pygame.image.load("resources/img/player/jump/jump-4.png")]
backjump = [pygame.image.load("resources/img/player/back-jump/back-jump-1.png"),
            pygame.image.load("resources/img/player/back-jump/back-jump-2.png"),
            pygame.image.load("resources/img/player/back-jump/back-jump-3.png"),
            pygame.image.load("resources/img/player/back-jump/back-jump-4.png"),
            pygame.image.load("resources/img/player/back-jump/back-jump-5.png"),
            pygame.image.load("resources/img/player/back-jump/back-jump-6.png"),
            pygame.image.load("resources/img/player/back-jump/back-jump-7.png")]

turret = [pygame.image.load("resources/img/turret/turret-1.png"),
          pygame.image.load("resources/img/turret/turret-2.png"),
          pygame.image.load("resources/img/turret/turret-3.png"),
          pygame.image.load("resources/img/turret/turret-4.png"),
          pygame.image.load("resources/img/turret/turret-5.png"),
          pygame.image.load("resources/img/turret/turret-6.png")]

plataforma = [pygame.image.load("resources/img/tiles/plataform.png"),
              pygame.image.load("resources/img/tiles/plataform2.png")]

orbe = [pygame.image.load("resources/img/orb/frame 1.png"),
       pygame.image.load("resources/img/orb/frame 2.png"),
       pygame.image.load("resources/img/orb/frame 3.png"),
       pygame.image.load("resources/img/orb/frame 4.png"),
       pygame.image.load("resources/img/orb/frame 5.png")]


hurt = pygame.mixer.Sound("resources/BGM/hurt.ogg")
PLATFORM_LIST = [(0, height - 40, widht, 400),
                 (880, 475, 100, 50),
                 (1050, 400, 30, 20),
                 (1200, height - 40, 500, 100),
                 (1780, 476, 50, 30),
                 (1900, 400, 50, 30),
                 (2020, 324, 50, 30),
                 (2140, 248, 50, 30),
                 (2185, 225, 50, 30),
                 (2190, 225, 50, 30),
                 (2260, 172, 50, 30),
                 (2380, 225, 40, 30),
                 (2500, 225, 40, 30),
                 (2620, 225, 40, 30),
                 (2740, 225, 40, 30),
                 (2860, 225, 40, 30),
                 (2980, 225, 40, 30),
                 (3040, 225, 100, 30),  # fim dos repetidos
                 (3240, 325, 500, 100),
                 (3800, 425, 40, 30),
                 (4020, 525, widht*2, 200)]

turret_list = [(680, 510), (1250, 510), (1570, 510), (2180, 180), (3040, 180), (3240, 280), (3400, 280), (3560, 280)]

item_list = [(5000, 480)]
# definindo cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 155, 155)
indigo = (75, 0, 130)
