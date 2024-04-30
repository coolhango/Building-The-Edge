# jogo de plataforma like mario bross

# seção de imports:
import pygame
import time
from os import path
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # inicialização dos elementos do jogo
        pygame.init()
        pygame.mixer.init()  # mixer carrega e toca sons
        pygame.mixer.music.load(
            "resources/BGM/Final Fantasy XIII Lightning Returns - ReleaseSalvation Fanfare [Extended].mp3")
        self.tela = pygame.display.set_mode((widht, height))  # criando a janela do jogo
        pygame.display.set_caption(titulo)  # colocando titulo na janela
        self.clock = pygame.time.Clock()  # objeto que ajuda a "localizar o tempo"
        self.loop = True
        self.jogando = True
        self.menu = True
        self.tutorial = False
        self.recordes = False
        self.dead = False
        self.escrita = False
        self.finish = False
        self.tempo_inicial = 0
        self.tempo = 0
        self.tempo_exibido = 0
        self.tempo_game_over = 0
        self.melhor_tempo = 0
        self.valores = []
        self.todos_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.plataformas = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.item = pygame.sprite.Group()
        self.load_data()
        pygame.mixer.music.play(-1)

    def load_data(self):
        f = open(filename, "r")
        lines = f.readlines()
        for line in lines:
            self.valores.append(line)
        f.close()

    def new(self):
        # novo jogo

        self.todos_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Plataforma(*plat)
            self.todos_sprites.add(p)
            self.plataformas.add(p)
        for mob in turret_list:
            g = ground_enemy(*mob)
            self.todos_sprites.add(g)
            self.inimigos.add(g)
        for orbs in item_list:
            o = orb(*orbs)
            self.todos_sprites.add(o)
            self.item.add(o)
        self.run()

    def run(self):
        # loop do jogo

        while self.jogando:
            self.clock.tick(fps)  # limita fps do jogo
            while self.menu:
                self.mostra_tela_inicial()
            while self.recordes:
                self.mostra_recordes()
            while self.tutorial:
                self.mostra_tutorial()
            while self.dead:
                self.mostra_tela_gameover()
            while self.finish:
                self.mostra_tela_vitoria()
            # chamando outras funções:
            self.events()
            self.update()
            self.drawn()

    def update(self):
        self.todos_sprites.update()
        # atualizando tempo
        self.tempo = (pygame.time.get_ticks() - self.tempo_inicial) / 1000
        self.tempo_exibido = round(self.tempo, 1)

        # checando colisões com as plataformas, inimigos e item
        if self.player.vel.y > 0:
            colisao = pygame.sprite.spritecollide(self.player, self.plataformas, False)
            if colisao:
                lowest = colisao[0]
                for hit in colisao:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

            colisao = pygame.sprite.spritecollide(self.player, self.inimigos, False)
            if colisao:
                lowest = colisao[0]
                for hit in colisao:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        hurt.play()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("resources/BGM/FF7- Gameover  Continue HD OST.mp3")
                        pygame.mixer_music.play(-1)
                        self.dead = True
            colisao = pygame.sprite.spritecollide(self.player, self.item, False)
            if colisao:
                lowest = colisao[0]
                for hit in colisao:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(
                            "resources/BGM/FFXIV OST Duty Complete Theme ( A Victory Fanfare Reborn ).mp3")
                        pygame.mixer_music.play(-1)

                        self.valores = []
                        self.escrita = True
                        self.finish = True

        # fazendo a tela andar junto com o jogador:
        if self.player.rect.left >= height - 200:
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for plat in self.plataformas:
                plat.rect.right -= max(abs(self.player.vel.x), 2)
            for mob in self.inimigos:
                mob.rect.right -= max(abs(self.player.vel.x), 2)
            for orbs in self.item:
                orbs.rect.right -= max(abs(self.player.vel.x), 2)

        # morte do jogador por queda:
        if self.player.rect.bottom > height:
            hurt.play()
            self.dead = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load("resources/BGM/FF7- Gameover  Continue HD OST.mp3")
            pygame.mixer_music.play(-1)

    def events(self):
        # loop do jogo: eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False
                if self.jogando:
                    self.jogando = False

    def drawn(self):
        # loop do jogo: draw

        # colocando fundo na tela
        self.tela.fill(light_blue)
        picture = pygame.transform.scale(bg_game, (800, 600))
        self.tela.blit(picture, (0, 0))
        # desenhando os sprites e o tempo na tela
        self.todos_sprites.draw(self.tela)
        self.draw_text("time: " + str(self.tempo_exibido), white, widht - 75, 15)
        pygame.display.flip()  # atualiza o display

    def mostra_tela_inicial(self):
        menu_title = fonte_menu.render("Building Edge", True, indigo)
        recorde = fonte_start.render("Press R to view Records", True, yellow)
        start_title = fonte_start.render("Press Start to continue", True, yellow)
        tecla = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif tecla[pygame.K_RETURN]:
                self.menu = False
                self.tutorial = True
            elif tecla[pygame.K_r]:
                self.valores = []
                self.menu = False
                self.recordes = True
        self.tela.blit(bg, (0, 0))
        self.clock.tick(fps)
        self.tela.blit(menu_title, (widht / 2 - 300, height - 575))
        self.tela.blit(recorde, (widht / 2 - 325, height - 200))
        self.tela.blit(start_title, (widht / 2 - 325, height - 100))

        pygame.display.flip()

    def mostra_tela_gameover(self):
        tecla = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or tecla[pygame.K_ESCAPE]:  # se apertar esc ou no x fecha
                pygame.quit()
                quit()
            elif tecla[pygame.K_RETURN]:  # se apertar start, reseta o jogo
                self.reset()

        self.tela.blit(bg, (0, 0))
        self.draw_text("GAME OVER", yellow, widht / 2, height / 4)
        self.draw_text("or GIVE UP? ", yellow, widht / 2, height / 2)
        self.draw_text("CONTINUE?", yellow, widht / 2, height / 2 - 30)
        self.draw_text("Press Enter to reset the game!", yellow, widht / 2, height - 100)
        self.draw_text("Press esc to close the game!", yellow, widht / 2, height - 50)
        pygame.display.flip()

    def mostra_tela_vitoria(self):
        tecla = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or tecla[pygame.K_ESCAPE]:  # se apertar esc ou no x fecha
                pygame.quit()
                quit()
            elif tecla[pygame.K_RETURN]:  # se apertar start, reseta o jogo
                self.reset()
        self.load_data()  # carregando valores de tempos

        self.tela.blit(bg, (0, 0))
        self.draw_text("COONGRATS,YOU WON THE GAME!!", yellow, widht / 2, height / 4)
        self.draw_text("TIME: " + str(self.tempo), yellow, widht / 2, height / 2)

        if len(self.valores) == 0:  # conferindo se tem algum tempo ja salvo
            self.draw_text("New High Score!!", yellow, widht / 2, height / 2 - 30)
        elif self.tempo < float(self.valores[0]) or self.tempo == float(
                self.valores[0]):  # conferindo se tem um recorde
            self.draw_text("New High Score!!", yellow, widht / 2, height / 2 - 30)

        self.draw_text("Press Enter to reset the game!", yellow, widht / 2, height - 100)
        self.draw_text("Press esc to close the game!", yellow, widht / 2, height - 50)

        self.valores.append(self.tempo)  # adicionando o tempo novo ao arquivo
        floatval = []
        floatval = [float(i) for i in self.valores]
        floatval.sort()
        self.valores = [str(i) for i in floatval]
        if self.escrita:
            f = open(filename, 'w')
            for item in self.valores:
                f.write('%s\n' % item)
            f.close()
            self.escrita = False
        pygame.display.flip()

    def mostra_tutorial(self):
        self.tempo_inicial = pygame.time.get_ticks()
        start_title = fonte_start.render("Press Start to play", True, yellow)
        esq_dir = fonte_timer.render("use de keys Left and Right to move", True, yellow)
        up_down = fonte_timer.render("Use key up to jump ", True, yellow)
        obj = fonte_timer.render("Your objective is to jump in the item at  end of map", True, yellow)
        tecla = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif tecla[pygame.K_RETURN]:
                pygame.mixer_music.stop()
                pygame.mixer_music.load("resources/BGM/sci_fi_platformer02.ogg")
                pygame.mixer_music.play(-1)
                self.tutorial = False

        self.tela.blit(bg, (0, 0))
        self.clock.tick(fps)
        self.tela.blit(start_title, (widht / 2 - 275, height - 100))
        self.tela.blit(esq_dir, (widht / 2 - 245, height - 400))
        self.tela.blit(up_down, (widht / 2 - 150, height - 350))
        self.tela.blit(obj, (widht / 2 - 335, height - 300))
        pygame.display.flip()

    def mostra_recordes(self):
        tecla = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or tecla[pygame.K_ESCAPE]:
                pygame.quit()
                quit()
            elif tecla[pygame.K_RETURN]:
                self.menu = True
                self.recordes = False
        self.load_data()
        menu_title = fonte_menu.render("Building Edge", True, indigo)

        record1 = fonte_timer.render("1º: " + self.valores[0] + " seconds", True, yellow)
        record2 = fonte_timer.render("2º: " + self.valores[1] + " seconds", True, yellow)
        record3 = fonte_timer.render("3º: " + self.valores[2] + " seconds", True, yellow)
        record4 = fonte_timer.render("4º: " + self.valores[3] + " seconds", True, yellow)
        record5 = fonte_timer.render("5º: " + self.valores[4] + " seconds", True, yellow)
        self.tela.blit(bg, (0, 0))
        self.clock.tick(fps)
        self.tela.blit(menu_title, (widht / 2 - 300, height - 575))
        self.tela.blit(record1, (widht / 2 - 300, height - 400))
        self.tela.blit(record2, (widht / 2 - 300, height - 360))
        self.tela.blit(record3, (widht / 2 - 300, height - 320))
        self.tela.blit(record4, (widht / 2 - 300, height - 280))
        self.tela.blit(record5, (widht / 2 - 300, height - 240))

        self.draw_text("Press Enter to return!", yellow, widht / 2, height - 100)
        self.draw_text("Press esc to close the game!", yellow, widht / 2, height - 50)
        pygame.display.flip()

    def draw_text(self, text, color, x, y):
        text_surface = fonte_timer.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.tela.blit(text_surface, text_rect)

    def reset(self):
        # reiniciando o jogo
        self.__init__()
        self.new()


jogo = Game()
while jogo.loop:
    jogo.new()
