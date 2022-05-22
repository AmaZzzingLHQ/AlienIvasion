class Settings:
    """设置"""

    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        #self.bg_color = (77,148,200)
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (72,183,152)
        self.bullet_allowd = 3

        #外星人设置
        self.alien_speed = 0.01
        self.fleet_drop_speed = 10
        #fleet_direction 为 1 表示向右移， -1 表示向左移
        self.fleet_direction = 1