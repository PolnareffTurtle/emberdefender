import pygame
from scripts.utils import Text


class Player:
    def __init__(self,game,pos,size):
        pygame.init()
        self.game=game
        self.velocity = [0,0]
        self.action = ''
        self.pos=list(pos)
        self.size=list(size)
        self.set_animation('idle')
        self.jumps = 0
        self.fuel = 100
        self.fuel_jump = False
        self.big = True
        self.air_time=0
        self.flip = False
        self.shift = 0
        self.fireballs=[]

    def rect(self):
        return pygame.rect.Rect(self.pos,self.size)

    def update(self,tilemap,movement=(0,0)):
        self.bottomcollide=False
        self.collisions = {'up':False,'down':False,'left':False,'right':False}
        frame_movement = [movement[0]*2*(self.shift+1)*(max(0.5,self.fuel/100)) + self.velocity[0],movement[1]+self.velocity[1]]
        if frame_movement[0]:
            if frame_movement[0] > 0:
                self.flip = False
            else: self.flip = True

        rects = tilemap.physics_rects_around(self.pos)

        self.pos[1] += frame_movement[1]

        self_rect = self.rect()
        for rect in rects['collide']:
            if self_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    self_rect.bottom = rect.top
                    self.collisions['down'] = True


                elif frame_movement[1] < 0:
                    self_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = self_rect.y

        self.pos[0] += frame_movement[0]
        self_rect = self.rect()
        for c_rect in rects['collide']:
            #pygame.draw.rect(self.game.display,(255,0,0),x,width=1)
            if self_rect.colliderect(c_rect):
                if frame_movement[0] > 0:
                    self_rect.right = c_rect.left
                    self.collisions['right'] = True
                elif frame_movement[0] < 0:
                    self_rect.left = c_rect.right
                    self.collisions['left'] = True
                self.pos[0] = self_rect.x



        for rect in rects['win']:
            if self_rect.colliderect(rect):
                self.game.gamestate = self.game.WIN

        for rect in rects['lose']:
            if self_rect.collidepoint(rect.center):
                self.game.gamestate = self.game.LOSE

        for rect in rects['items']:
            if self_rect.colliderect(rect[0]):
                self.fuel += 25+rect[1]*25
                del tilemap.tilemaps[tilemap.main_layer][(rect[0].x//tilemap.tile_size,rect[0].y//tilemap.tile_size)]

        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
            if self.fuel > 50:
                self.set_animation('idle')
            else:
                self.set_animation('dimmed')

        self.air_time += 1
        if self.air_time > 4:
            self.jumps = 0

        self.velocity[1] = min(10, self.velocity[1] + 0.25)
        if self.velocity[0] > 0: self.velocity[0] = max(0,self.velocity[0]-0.1)
        else: self.velocity[0] = min(0,self.velocity[0]+0.1)

        #if self.pos[0] > 0.5*tilemap.size[1]*tilemap.tile_size:
        #    self.velocity[1] = 0
        #    self.rect().bottom = int(0.5*self.game.display.get_height())




        if self.fuel > 100:
            self.fuel = 100
        else:
            self.fuel -= 0.1*(self.shift*1.5+1)

        if self.fuel < 0:
            self.game.gamestate = self.game.LOSE
        elif self.fuel < 30:
            self.set_animation('dimmed')

        else:
            self.set_animation('idle')


        for fireball in self.fireballs:
            fireball.update()

        self.animation.update()
        if self.action == 'grow':
            if self.animation.frame_index == 4:
                self.set_animation('idle')

    def set_animation(self,action):
        if self.action != action:
            self.action = action
            self.animation = self.game.assets['player_'+action]
            self.size = self.game.assets['player_'+action].img().get_size()



    def jump(self):
        if self.jumps:
            self.velocity[1] = -5
            self.jumps = 0

    def fireball(self,direction):
        self.fireballs.append(Fireball(self.game,self.pos,direction))
        self.fuel-=30
        self.velocity[0] = -direction[0]*5



    def render(self,screen,offset=(0,0)):
        for fireball in self.fireballs:
            fireball.render(screen,offset)

        #x = pygame.image.load('data/graphics/ember/idle0000.png').convert_alpha()
        screen.blit(pygame.transform.flip(self.animation.img(),self.flip,0),(self.pos[0]-offset[0],self.pos[1]-offset[1]))
        Text(str(int(self.fuel))+'%',10,'white',screen,(self.pos[0]-offset[0],self.pos[1]-offset[1]-30))
        #pygame.draw.rect(self.game.display, (0, 0, 255),
        #                 pygame.rect.Rect(self.pos[0]-offset[0], self.pos[1]-offset[1], self.size[0], self.size[1]),
        #                 width=1)

class Fireball:
    def __init__(self,game,pos,direction):
        self.direction = direction
        self.image = game.assets['fireball']
        self.pos = list(pos)

    def update(self):
        self.pos[0] += self.direction[0]*5
        self.pos[1] += self.direction[1]*5

    def render(self,surf,offset):
        surf.blit(self.image,(self.pos[0]-offset[0],self.pos[1]-offset[1]))