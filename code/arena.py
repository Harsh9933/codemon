import pygame
from pytmx import load_pygame
from os.path import join
from groups import *
from settings import *
from support import *
from sprites import *
from entites import *


class Arena:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('codemon')
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.import_assets()
        self.setup(self.tmx_maps['hospital'], 'world')
        self.active = False
        self.input_surface = pygame.image.load('white.jpeg')
        self.input_rect = self.input_surface.get_rect(center=(800, 600))
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.user_text = ''
        self.font = pygame.font.Font(None, 32)


    def import_assets(self):
        self.tmx_maps = {
            'hospital': load_pygame(join('..', 'data', 'maps', 'hospital.tmx'))
        }
        self.overworld_frames = {
            'characters': all_character_import('..', 'graphics', 'characters')
        }

    def setup(self, tmx_map, player_start_pos):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, z=WORLD_LAYERS['bg'])

        for x, y, surf in tmx_map.get_layer_by_name('Terrain Top').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, z=WORLD_LAYERS['bg'])

        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'top':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z=WORLD_LAYERS['top'])
            else:
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))


        for obj in tmx_map.get_layer_by_name('Entities'):
            graphic = obj.properties.get('graphic', None)
            if obj.name == 'Player':
                if obj.properties['pos'] == player_start_pos:
                    self.player = Player(
                        pos=(obj.x, obj.y),
                        frames=self.overworld_frames['characters']['young_guy'],
                        groups=self.all_sprites,
                    )
            else:
                self.character = Character(
                    pos=(obj.x, obj.y),
                    frames=self.overworld_frames['characters'][graphic],
                    groups=(self.all_sprites, self.collision_sprites)
                )

    def draw_textbox(self,surface, text, x, y, width, height):
        pass
            # pygame.draw.rect(self.display_surface, (200,22,50), (x, y, width, height), 2)
            # if text:
            #     text_surface = self.font.render(text, True, (0, 0, 0))
            #     surface.blit(text_surface, (x + 5, y + 5))

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        self.user_text += event.unicode

            self.all_sprites.update(dt)
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)

            pygame.draw.rect(self.display_surface,(250, 250, 250),self.input_rect,5)

            text_surface = self.font.render(self.user_text,True, (0, 0, 0))
            self.display_surface.blit(text_surface, (self.input_rect.x + 10,  self.input_rect.y + 10))
            self.input_rect.w = text_surface.get_width()+10
            # text = ''
            # self.draw_textbox(self.display_surface, text, x=650, y=500, width=800, height=230)
            #
            # self.all_sprites.draw(self.player.rect.center)
            # pygame.draw.rect(self.display_surface, (255, 255, 255), (650, 500, 800, 230))
            # # pygame.draw.rect(self.display_surface,[66, 135, 245], [50, 500, 50])


            pygame.display.update()


if __name__ == '__main__':
    game = Arena()
    game.run()
