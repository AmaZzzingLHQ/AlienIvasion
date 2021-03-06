import sys
from time import sleep
import pygame
 
from setting import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvavsion:
    """管理游戏资源和行为"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Aline Invasion") #为当前窗口设置标题

        #创建一个用于存储统计游戏信息的类
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #创建play按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()


    def _check_events(self):
        #监视键盘和鼠标
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #重置游戏信息
            self.stats.reset_stats()
            self.stats.game_active = True

            #清空余下的外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            #创建新的外星人和飞船
            self._create_fleet()
            self.ship.center_ship()

            #隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
            if event.key == pygame.K_RIGHT:
            #飞船向右移动
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()

    def _check_keyup_events(self,event):
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _fire_bullet(self):
        """创建1颗子弹，并将其加入bullets"""
        if len(self.bullets) < self.settings.bullet_allowd:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹"""
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_akien_collisons()

    def _check_bullet_akien_collisons(self):
        # 检查是否有子弹命中了外星人
        # 如果是，删除子弹和外星人
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        #删除子弹并生成新的外星人
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _create_fleet(self):
        """创建外星人群"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可以容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建第一行外星人
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self,alien_number, row_number):
        # 创建一个外星人并加入当前行
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edge(self):
        """外星人到达边缘后"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break
    
    def _check_aliens_bottom(self):
        """检测外星人是否到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞击一样处理
                self._ship_hit()
                break
    
    def _change_fleet_direction(self):
        """将外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """更新外星人的位置"""
        self._check_fleet_edge()
        self.aliens.update()

        # 检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        # 检测是否有外星人到达了底端
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        #print(self.stats.ships_left)
        if self.stats.ships_left > 0:
            #将 ships_left -1
            self.stats.ships_left -= 1

            #清空余下的外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            #创建新的外星人和飞船
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        #每次循环重置屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #play按钮
        if not self.stats.game_active:
            self.play_button._draw_button()

        #让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    #创建游戏实例并运行
    ai = AlienInvavsion()
    ai.run_game()
