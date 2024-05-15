import pygame
from sys import exit
from scripts.utils import load_image, load_images, Animation, Text
from scripts.entities import Player
from scripts.tilemap import Tilemap
from scripts.text import texts

class Game:
    GAME_RUNNING = 1
    MAIN_MENU = 2
    LEVEL_SELECT = 3
    OPTIONS = 4
    LOSE = 5
    WIN = 6
    GAME_MENU = 7

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((720,480))
        self.display = pygame.Surface((360,240))
        pygame.display.set_caption('Ember Defender!!')
        self.clock = pygame.time.Clock()
        self.gamestate = Game.MAIN_MENU
        self.level = 1

        self.option_index = [0, 0]
        self.option = 0




        self.assets = {
            'player_idle':Animation(load_images('ember/idle2',scale=2),10),
            'player_small':Animation(load_images('ember/small'),5),
            'player_shrink':Animation(load_images('ember/shrink'),2),
            'player_grow':Animation(load_images('ember/grow'),2),
            'player_dimmed':Animation(load_images('ember/dimmed2',scale=2),10),
            'player_jump':Animation(load_images('ember/jump',scale=2),10),
            'player_jump_dim':Animation(load_images('ember/jump_dim',scale=2),10),
            #'player_2':Animation(load_images('ember/idle2'),10),
            'shading0':load_images('tiles2',alpha=False,scale=2),
            'shading1':load_images('shading1',alpha=False,scale=2),
            'shading2':load_images('shading2',alpha=False,scale=2),
            'shading3':load_images('shading3',alpha=False,scale=2),
            'transition':load_image('trans.jpg'),
            'fireball':load_image('ember/fireball/unnamed.png')
        }



    def main_menu(self):
        option_index = 0
        self.transition_index = 0
        while self.gamestate == Game.MAIN_MENU:
            self.display.fill('#94eff7')
            self.display.blit(pygame.transform.scale_by(self.assets['player_idle'].img(),8),(20,60))

            self.assets['player_idle'].update()
            texts(self.display,'main_menu')
            Text(['Play','Levels','Options'][option_index],15,'white',self.display,(218,78+option_index*40))
            Text('>',15,'#EF8933',self.display,(190,76 + option_index*40))
            Text('>', 15, 'white', self.display, (188, 74 + option_index * 40))

            #Text('Use arrow keys/return',8,'#EF8933',self.display,(5,100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        option_index = (option_index-1)%3
                    elif event.key == pygame.K_DOWN:
                        option_index = (option_index+1)%3
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.gamestate = [Game.GAME_MENU,Game.LEVEL_SELECT,Game.OPTIONS][option_index]
                        self.transition_out()
                        break

            self.transition_in()

            self.clock.tick(60)
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))

    def level_select(self):
        option_index=0
        self.transition_index = 0
        while self.gamestate == Game.LEVEL_SELECT:
            self.display.fill('#94eff7')
            texts(self.display,'level_select')
            Text('>', 15, '#EF8933', self.display, (20 + (option_index % 5) * 72, 30 + (option_index // 5) * 40))
            Text('>',15,'white',self.display,(18+(option_index%5)*72,28+(option_index//5)*40))

            Text(str(option_index+1),15,'white',self.display,(38+(option_index%5)*72,28+(option_index//5)*40))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        option_index = (option_index-5)%20
                    elif event.key == pygame.K_DOWN:
                        option_index = (option_index+5)%20
                    elif event.key == pygame.K_LEFT:
                        option_index = (option_index-1)%20
                    elif event.key == pygame.K_RIGHT:
                        option_index = (option_index+1)%20

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.level = option_index+1
                        self.gamestate = Game.GAME_MENU
                        self.transition_out()
                        break
                    elif event.key == pygame.K_ESCAPE:
                        self.gamestate = Game.MAIN_MENU
                        self.transition_out()
                        break

            self.transition_in()

            self.clock.tick(60)
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def options(self):
        self.transition_index = 0
        while self.gamestate == Game.OPTIONS:
            self.display.fill('#EF8933')
            Text('[ESC]',10,'white',self.display,(5,5))
            Text('Sound',20,'white',self.display,(15,15))
            Text('Resolution',20,'white',self.display,(15,35))
            Text(['On','Off'][self.option_index[0]],10,'white',self.display,(110,15))
            Text(['720x480','1440x960','360x240'][self.option_index[1]],10,'white',self.display,(110,35))
            Text('>',20,'white',self.display,(5,15+self.option*20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_UP,pygame.K_DOWN]:
                        self.option=(self.option+1)%2
                    if event.key == pygame.K_RIGHT:
                        self.option_index[self.option] = (self.option_index[self.option]+1)%[2,3][self.option]
                        if self.option ==1:
                            pygame.display.set_mode([(720, 480), (1440, 960), (360, 240)][self.option_index[1]])

                    elif event.key == pygame.K_LEFT:
                        self.option_index[self.option] = (self.option_index[self.option]-1)%[2,3][self.option]
                        if self.option == 1:
                            pygame.display.set_mode([(720, 480), (1440, 960),  (360, 240)][self.option_index[1]])

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gamestate = Game.MAIN_MENU
                        self.transition_out()
                        break

            self.transition_in()

            self.clock.tick(60)
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

    def game_menu(self):
        self.transition_index = 0
        while self.gamestate == Game.GAME_MENU:
            self.display.fill('#EF8933')
            texts(self.display,'game_menu',self.level)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gamestate = Game.MAIN_MENU
                        self.transition_out()
                        break
                    elif event.key == pygame.K_SPACE:
                        self.gamestate = Game.GAME_RUNNING
                        self.transition_out()
                        break

            self.transition_in()

            self.clock.tick(60)
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
    def game_running(self):
        self.player = Player(self, (5, 0), self.assets['player_idle'].img().get_size())
        self.scroll = [self.player.rect().centerx - self.display.get_height()/2,self.player.rect().centery - self.display.get_height()/2]
        self.movement = [False,False]
        self.tilemap = Tilemap(self,self.level)
        self.transition_index = 0
        self.direction = 1

        while self.gamestate == Game.GAME_RUNNING:

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])/10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10

            self.render_scroll = [int(self.scroll[0]),int(self.scroll[1])]
            self.display.fill((123,123,135))

            Text('[ESC]', 10, 'white', self.display, (5, 5))

            self.tilemap.render(self.display,offset=self.render_scroll)
            self.player.update(self.tilemap,(self.movement[1]-self.movement[0],0))
            self.player.render(self.display,offset=self.render_scroll)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT,pygame.K_a]:
                        self.movement[0] = True
                        self.direction = -1
                    if event.key in [pygame.K_RIGHT,pygame.K_d]:
                        self.movement[1] = True
                        self.direction = 1
                    if event.key in [pygame.K_UP,pygame.K_w,pygame.K_SPACE]:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        self.gamestate = Game.MAIN_MENU
                        break
                    if event.key == pygame.K_r:
                        self.gamestate = Game.GAME_MENU
                        break
                    if event.key == pygame.K_j:
                        self.player.shift = 1
                    if event.key == pygame.K_k:
                        self.player.fireball((self.direction,0))
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT,pygame.K_a]:
                        self.movement[0] = False
                    if event.key in [pygame.K_RIGHT,pygame.K_d]:
                        self.movement[1] = False
                    if event.key == pygame.K_j:
                        self.player.shift = 0

            self.transition_in()

            self.clock.tick(60)
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0, 0))

    def lose(self):
        self.gamestate = Game.GAME_MENU
        self.transition_out()

    def win(self):
        self.level += 1
        self.gamestate = Game.GAME_MENU
        self.transition_out()
        
    def transition_in(self):
        if self.transition_index < self.assets['transition'].get_width():
            self.display.blit(self.assets['transition'], (self.transition_index, 0))
            self.transition_index += 20

    def transition_out(self):
        i=0
        while i<self.assets['transition'].get_width():
            self.display.blit(self.assets['transition'],(i-self.assets['transition'].get_width(),0))
            i+=10

            pygame.display.update()
            self.clock.tick(60)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))




    def run(self):
        while True:
            if self.gamestate == Game.GAME_RUNNING:
                self.game_running()
            elif self.gamestate == Game.MAIN_MENU:
                self.main_menu()
            elif self.gamestate == Game.LEVEL_SELECT:
                self.level_select()
            elif self.gamestate == Game.OPTIONS:
                self.options()
            elif self.gamestate == Game.GAME_MENU:
                self.game_menu()
            elif self.gamestate == Game.LOSE:
                self.lose()
            elif self.gamestate == Game.WIN:
                self.win()


if __name__ == '__main__':
    game = Game()
    game.run()