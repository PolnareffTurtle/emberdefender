import pygame
import json
import math

NEIGHBOR_OFFSETS = [
    (-1,-1), (0,-1), (1,-1), (2,-1),
    (-1,0),  (0,0),  (1,0),  (2,0),
    (-1,1),  (0,1),  (1,1),  (2,1),
    (-1,2),  (0,2),  (1,2),  (2,2)
]

COLLIDE_RECTS = [16,17,18,19,20,21,22,23,
                 25,26,27,28,29,30,31,
                 33,34,35,36,37,38,39,
                 41,42,43,44,45,46,47,
                 49,50,51,52,53,54,55,
                 56,57,58,59,60,61,62,63]

WIN_TILES = [5,6,7]

LOSE_TILES = [32,40,48]

ITEMS = [0,1]

class Tile:
    def __init__(self,tile_index,pos):
        self.index = tile_index
        self.pos = pos

class Tilemap:
    def __init__(self, game, level, tile_size=16):
        self.game = game
        self.tilemaps = []
        self.tile_size = tile_size
        self.open_json(level)

    def open_json(self,level):
        with open('data/levels/'+str(level)+'.json') as f:
            rawdata = f.read()
            jsondata = json.loads(rawdata)


        self.main_layer = jsondata['properties'][0]['value']
        self.size = (jsondata['width'],jsondata['height'])

        for layer in jsondata['layers']:
            tilemap = {}
            for j, val in enumerate(layer['data']):
                if val != 0:
                    tilemap[(j%layer['width'],j//layer['width'])] = Tile(val-1,(j%layer['width'],j//layer['width']))
            self.tilemaps.append(tilemap)

    def tiles_around(self,pos):
        tiles = []
        for offset in NEIGHBOR_OFFSETS:
            check = (pos[0]//self.tile_size+offset[0],pos[1]//self.tile_size+offset[1])
            if check in self.tilemaps[self.main_layer]:
                tiles.append(self.tilemaps[self.main_layer][check])
        return tiles

    def physics_rects_around(self,pos):
        physics_rects = {'collide':[],'win':[],'lose':[],'items':[]}
        for tile in self.tiles_around(pos):
            tile_rect = pygame.rect.Rect(tile.pos[0]*self.tile_size,tile.pos[1]*self.tile_size,self.tile_size,self.tile_size)
            if tile.index in COLLIDE_RECTS:
                physics_rects['collide'].append(tile_rect)
            elif tile.index in WIN_TILES:
                physics_rects['win'].append(tile_rect)
            elif tile.index in LOSE_TILES:
                physics_rects['lose'].append(tile_rect)
            elif tile.index in ITEMS:
                physics_rects['items'].append((tile_rect,tile.index))
        return physics_rects

    def render(self,surf,offset=(0,0)):
        for tilemap in self.tilemaps:
            for x in range(offset[0]//self.tile_size,(offset[0]+surf.get_width())//self.tile_size+1):
                for y in range(offset[1]//self.tile_size,(offset[1]+surf.get_height())//self.tile_size+1):
                    if (x,y) in tilemap:
                        tile = tilemap[(x,y)]
                        shading = int(math.sqrt((self.game.player.rect().centerx-self.tile_size*(x+0.5))**2+(self.game.player.rect().centery-self.tile_size*(y+0.5))**2)//(self.tile_size*2*math.sqrt(2)))
                        if shading > 3: shading = 3
                        if self.game.player.fuel <= 60:
                            shading = min(shading+1,3)
                        if self.game.player.fuel <= 30:
                            shading = 3
                        surf.blit(self.game.assets['shading'+str(shading)][tile.index],(tile.pos[0]*self.tile_size-offset[0],tile.pos[1]*self.tile_size-offset[1]))

                        #surf.blit(self.game.assets['shading'][2],(tile.pos[0]*self.tile_size-offset[0],tile.pos[1]*self.tile_size-offset[1]))

