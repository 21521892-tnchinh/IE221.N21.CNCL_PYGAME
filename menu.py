import pygame
import sys
from settings import *
from timer import Timer

class Menu:
    def __init__(self,player,toggle_menu):

        #genera setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        #options
        self.width = 400
        self.space = 10
        self.padding = 8

        #entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        #movement
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom =(SCREEN_WIDTH / 2 , SCREEN_HEIGHT - 20 ))

        pygame.draw.rect(self.display_surface,'White', text_rect.inflate(10,10), 0 , 4)
        self.display_surface.blit(text_surf,text_rect)

    def setup(self):
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            text_surf = self.font.render(item,False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() +self.padding * 2
        self.total_height += (len(self.text_surfs) - 1 ) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height /2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2 ,self.menu_top,self.width,self.total_height)

        # buy/ sell
        self.buy_text = self.font.render('buy', False,'Black')
        self.sell_text = self.font.render('sell', False,'Black')
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
            if keys[pygame.K_SPACE]:
                self.timer.activate()

                #get item
                current_item = self.options[self.index]

                #sell
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -=1
                        self.player.money += SALE_PRICES[current_item]
                # buy
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] +=1
                        self.player.money -= PURCHASE_PRICES[current_item]


        #clamo the values
        if self.index <0 :
            self.index = len(self.options) -1
        if self.index > len(self.options) -1 :
            self.index = 0

    def show_entry(self,text_surf,amount,top,selected):

        #background
        bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + self.padding * 2)
        pygame.draw.rect(self.display_surface ,'White', bg_rect, 0, 4)

        #text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery ))
        self.display_surface.blit(text_surf,text_rect)

        #amount
        amount_surf =self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright =(self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf,amount_rect)

        #selected
        if selected:
            pygame.draw.rect(self.display_surface,'black', bg_rect, 4, 4)
            if self.index > self.sell_border: #sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text,pos_rect)
            else: #buy
                pos_rect = self.buy_text.get_rect(midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surf in enumerate( self.text_surfs):
            top = self.main_rect.top +text_index *(text_surf.get_height() +(self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf,amount,top, self.index == text_index)

class Pause:
    def __init__(self, player, toggle_pause, music_enabled = True):
        # General setup
        self.player = player
        self.toggle_pause = toggle_pause
        self.music_enabled = music_enabled
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)
        self.mouse_clicked = False

    def update(self):
        # Display pause menu
        menu_width = 400
        menu_height = 200
        menu_x = (SCREEN_WIDTH - menu_width) // 2
        menu_y = (SCREEN_HEIGHT - menu_height) // 2
        menu_surface = pygame.Surface((menu_width, menu_height))
        background_color = (221, 196, 136)  # Màu nền menu
        border_color = (165, 140, 82)  # Màu viền menu
        line_color = (165, 140, 82)  # Màu đường kẻ

        # Fill màu nền cho khung menu nhỏ
        menu_surface.fill(background_color)

        # Vẽ viền cho khung menu
        pygame.draw.rect(menu_surface, border_color, menu_surface.get_rect(), 3)

        # Hiển thị khung menu nhỏ tại vị trí tính toán
        self.display_surface.blit(menu_surface, (menu_x, menu_y))

        # Render menu options
        option_font = pygame.font.Font('font/LycheeSoda.ttf', 36)

        # Render tiêu đề menu
        title_font = pygame.font.Font('font/LycheeSoda.ttf', 48)
        title_text = title_font.render('Option', True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 40))
        self.display_surface.blit(title_text, title_rect)

        # Vẽ các ô lựa chọn
        option_width = 20
        option_height = 20
        option_x = menu_x + 20
        option_y = menu_y + 90

        pygame.draw.rect(menu_surface, border_color, (option_x, option_y, option_width, option_height), 2)  # Ô lựa chọn 1
        pygame.draw.rect(menu_surface, border_color, (option_x, option_y + 40, option_width, option_height), 2)  # Ô lựa chọn 2
        pygame.draw.rect(menu_surface, border_color, (option_x, option_y + 80, option_width, option_height), 2)  # Ô lựa chọn 3

        pause_text = option_font.render('Resume', True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.display_surface.blit(pause_text, pause_rect)

        music_text = option_font.render('Music: On', True, (255, 255, 255)) if self.music_enabled else option_font.render(
            'Music: Off', True, (255, 255, 255))
        music_rect = music_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.display_surface.blit(music_text, music_rect)

        quit_text = option_font.render('Quit Game', True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.display_surface.blit(quit_text, quit_rect)

        # Vẽ đường kẻ ngăn cách
        line_y1 = option_y + 30
        line_y2 = option_y + 70
        pygame.draw.line(menu_surface, line_color, (option_x, line_y1), (option_x + option_width, line_y1), 2)
        pygame.draw.line(menu_surface, line_color, (option_x, line_y2), (option_x + option_width, line_y2), 2)

        # Check for menu option selection
        mouse_pos = pygame.mouse.get_pos()
        if pause_rect.collidepoint(mouse_pos):
            pause_text = option_font.render('Resume', True, (138, 43, 226))
            self.display_surface.blit(pause_text, pause_rect)
            if pygame.mouse.get_pressed()[0]:
                self.toggle_pause()
        elif music_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.mouse_clicked:
                self.mouse_clicked = True
                self.music_enabled = not self.music_enabled
            music_text = option_font.render('Music: On', True,
                                            (138, 43, 226)) if self.music_enabled else option_font.render('Music: Off',
                                                                                                     True,
                                                                                                     (138, 43, 226))
            self.display_surface.blit(music_text, music_rect)

        elif quit_rect.collidepoint(mouse_pos):
            quit_text = option_font.render('Quit Game', True, (138, 43, 226))
            self.display_surface.blit(quit_text, quit_rect)
            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                sys.exit()
        if not pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = False