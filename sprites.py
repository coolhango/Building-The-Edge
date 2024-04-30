# classe de sprites
import pygame
from settings import *
from random import choice

vector = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = stop[0]
        self.image = pygame.transform.scale(self.image, (110, 110))
        self.image.set_colorkey(yellow)
        self.rect = self.image.get_rect()
        self.andando = False
        self.pulando = False
        self.current_frame = 0
        self.last_update = 0
        self.run_l = []
        self.carrega_imagens()
        self.rect.center = (widht / 2, height / 2)
        self.pos = vector(widht / 2, height / 2)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

    def carrega_imagens(self):
        for frame in run:
            self.run_l.append(pygame.transform.flip(frame, True, False))

    def update(self):
        self.animacao()
        self.acc = vector(0, gravidade)
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self.acc.x = -aceleracao_jogador
        if tecla[pygame.K_RIGHT]:
            self.acc.x = aceleracao_jogador
        if tecla[pygame.K_UP]:
            self.pulo()

        # equações para calcular o movimento:
        self.acc.x += self.vel.x * atrito_jogador
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # parando no topo
        if self.pos.y > height:
            self.pos.x = height
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos

    def animacao(self):
        agora = pygame.time.get_ticks()

        # definindo se esta andando parado ou pulando
        if self.vel.x != 0 and self.vel.y == 0:
            self.andando = True
        else:
            self.andando = False
        if self.vel.y != 0:
            self.pulando = True
        else:
            self.pulando = False

        # definindo animação para pulo e pulo para traz
        if (self.pulando and self.vel.x > 0) or self.pulando:
            if agora - self.last_update > 100:
                self.last_update = agora
                self.current_frame = (self.current_frame + 1) % len(jump)
                inferior = self.rect.bottom
                self.image = jump[self.current_frame]
                self.image = pygame.transform.scale(self.image, (110, 110))
                self.rect = self.image.get_rect()
                self.rect.bottom = inferior

        if self.pulando and self.vel.x < 0:
            if agora - self.last_update > 100:
                self.last_update = agora
                self.current_frame = (self.current_frame + 1) % len(backjump)
                inferior = self.rect.bottom
                self.image = backjump[self.current_frame]
                self.image = pygame.transform.scale(self.image, (110, 110))
                self.rect = self.image.get_rect()
                self.rect.bottom = inferior

        # mostando animação de andando
        if self.andando:
            if agora - self.last_update > 150:
                self.last_update = agora
                self.current_frame = (self.current_frame + 1) % len(run)
                inferior = self.rect.bottom
                if self.vel.x > 0:
                    self.image = run[self.current_frame]
                    self.image = pygame.transform.scale(self.image, (110, 110))
                else:
                    self.image = self.run_l[self.current_frame]
                    self.image = pygame.transform.scale(self.image, (110, 110))
                self.rect = self.image.get_rect()
                self.rect.bottom = inferior

        # mostando animação de IDLE
        if not self.pulando and not self.andando:
            if agora - self.last_update > 200:
                self.last_update = agora
                self.current_frame = (self.current_frame + 1) % len(stop)
                self.image = stop[self.current_frame]
                self.image = pygame.transform.scale(self.image, (110, 110))

    def pulo(self):
        self.rect.y += 1
        colisao = pygame.sprite.spritecollide(self, self.game.plataformas, False)
        self.rect.y -= 1
        if colisao:
            self.vel.y = -15


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)

        self.image = choice(plataforma)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(black)
        self.rect.x = x
        self.rect.y = y


class ground_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = turret[0]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.rect.x = x
        self.rect.y = y

    def update(self):
        agora = pygame.time.get_ticks()

        if agora - self.last_update > 125:
            inferior = self.rect.bottom
            self.last_update = agora
            self.current_frame = (self.current_frame + 1) % len(turret)
            self.image = turret[self.current_frame]
            self.image = pygame.transform.scale(self.image, (50, 50))

        self.image.set_colorkey(black)


class orb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = orbe[0]
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0
        self.rect.x = x
        self.rect.y = y

    def update(self):
        agora = pygame.time.get_ticks()

        if agora - self.last_update > 125:
            inferior = self.rect.bottom
            self.last_update = agora
            self.current_frame = (self.current_frame + 1) % len(orbe)
            self.image = orbe[self.current_frame]
            self.image = pygame.transform.scale(self.image, (40, 40))

        self.image.set_colorkey(black)
