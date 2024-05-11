import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from sprites import Sprite,AnimatedSprite ,BorderSprite, TransitionSprite
from entites import Player,  Character
from groups import AllSprites
from support import *
from dialog import *



class Game:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('codemon')
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.import_assets()
        self.setup(self.tmx_maps['world'], 'house')
        self.game_state = 'active'
        self.transition_sprites = pygame.sprite.Group()


    def import_assets(self):
        self.tmx_maps = {
            'world': load_pygame(join('..', 'data', 'maps', 'world.tmx')),
            'hospital': load_pygame(join('..', 'data', 'maps', 'hospital.tmx'))
        }
        self.overworld_frames = {
            'water': import_folder('..', 'graphics', 'tilesets', 'water'),
            'coast': coast_importer(24, 12, '..', 'graphics', 'tilesets', 'coast'),
            'characters': all_character_import('..', 'graphics', 'characters')
        }



    def setup(self, tmx_map, player_start_pos):
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Character':
                char_id = obj.properties.get('character_id')
                if char_id == 'o1':
                    print("Dialog")

        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, z=WORLD_LAYERS['bg'])

        for x, y, surf in tmx_map.get_layer_by_name('Terrain Top').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites,  z=WORLD_LAYERS['bg'])

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'top':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites,  z=WORLD_LAYERS['top'])
            else:
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Monsters'):
            Sprite((obj.x, obj.y), obj.image, (self.all_sprites))

        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x, y), self.overworld_frames['water'], self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Collisions'):
            BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.collision_sprites))

        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites,  z=WORLD_LAYERS['bg'])

        for obj in tmx_map.get_layer_by_name('Entities'):
            graphic = obj.properties.get('graphic', None)
            if obj.name == 'Player':
                if obj.properties['pos'] == player_start_pos:
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.overworld_frames['characters']['young_guy'],
                        groups=self.all_sprites
                        )
            else:
                 self.character = Character(
                    pos=(obj.x, obj.y),
                    frames=self.overworld_frames['characters'][graphic],
                    groups=(self.all_sprites, self.collision_sprites)
                )

    def create_dialog(self, character):
        if not self.dialog_tree:
            self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'],self.end_dialog)
    def transition_check(self):
        sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.player.block()
            self.transition_target = sprites[0].target

    def run(self):
        while True:
            if self.game_state == 'active':
                dt = self.clock.tick() / 1000
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                self.all_sprites.update(dt)
                self.display_surface.fill('black')
                self.transition_check()
                self.all_sprites.draw(self.player.rect.center)
                pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()