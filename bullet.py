import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.srceen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #存储小数表示的子弹位置
        self.y = float(self.rect.y)
    
    def update(self):
        """向上移动的子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    
    def draw_bullet(self):
        pygame.draw.rect(self.srceen,self.color,self.rect)