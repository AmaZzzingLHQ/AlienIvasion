import pygame

from setting import Settings

class Ship:
    """管理飞船类"""

    def __init__(self,ai_game):
        """初始化飞船并设置其位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        #初始化设置
        #self.settings = Settings()

        #加载飞船并获取其外界矩形
        self.image = pygame.image.load('images/ship.bmp').convert()
        self.image.set_colorkey((30,30,30))
        self.rect = self.image.get_rect()
        

        #对于每艘新飞船，置于屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        #存储飞船的x float
        self.x = float(self.rect.x)

        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志改变飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
    
        self.rect.x = self.x
    
    def center_ship(self):
        """飞船居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = self.rect.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)
    

