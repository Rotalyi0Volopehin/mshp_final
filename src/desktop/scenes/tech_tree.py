import pygame
import os

from objects.text import Text, TextAlignment
from objects.btn_img import ImageButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.end_turn_button import EndTurnButton
from scenes.base import Scene
from objects.button import Btn
from constants import Color
from objects.grid_tile_info_plate import GridTileInfoPlate
from game_eng.grid_tile_upgrade_tree import GridTileUpgradeTree


class TreeScene(Scene):
    def create_objects(self):
        self.toolber = self.game.current_scene.toolbar
        self.start_team = None
        self.width = self.game.width
        self.height = self.game.height
        self.types = GridTileUpgradeTree.tile_upgrade_bases
        self.game_vc = self.game.current_scene.game_vc
        self.click_flag = [False]*8
        self.tile_text_1 = Text(self.game, text="", y=self.height-160, x =(10),font_size=20, alignment=TextAlignment.LEFT)
        self.tile_text_2 = Text(self.game, text="", y=self.height - 140, x=(10), font_size=20,
                                alignment=TextAlignment.LEFT)
        self.tile_text_3 = Text(self.game, text="", y=self.height - 120, x=(10), font_size=20,
                                alignment=TextAlignment.LEFT)
        self.tile_text_4 = Text(self.game, text="", y=self.height - 100, x=(10), font_size=20,
                                alignment=TextAlignment.LEFT)
        self.objects.append(self.tile_text_1)
        self.objects.append(self.tile_text_2)
        self.objects.append(self.tile_text_3)
        self.objects.append(self.tile_text_4)
        self.objects.append(self.game_vc)
        self.test_button = Btn(self.game, (30, 30, 100, 40), Color.WHITE,"Снять улучшение", self.downgrade())
        self.add_buttons()
        button_back = Btn(self.game, (self.width - 240, 5, 100, 40), Color.WHITE, 'Карта',
                          self.game.return_to_upper_scene)
        self.objects.append(button_back)
        grid_tile_info_plate = GridTileInfoPlate(self.game, self.game_vc, self.width - 20, 50, 340)
        self.end_turn_button = EndTurnButton(self.game, self.width - 100, self.height - 200)
        self.objects.append(self.end_turn_button)
        self.current_player_plate = CurrentPlayerPlate(self.game, self.width - 90, self.height - 183)
        self.objects.append(self.current_player_plate)
        self.info_text = Text(self.game, text="",font_size=25 ,y=self.height-190, x =(10), alignment=TextAlignment.LEFT)
        self.objects.append(self.info_text)
        self.money_text = Text(self.game, text="Деньги: "+str(self.game.current_scene.game_vc.model.current_team.money), y=self.height-60, x =(self.width//3), alignment=TextAlignment.LEFT)
        self.objects.append(self.money_text)
        self.objects.append(grid_tile_info_plate)
        self.line1 = pygame.draw.line(self.game.screen, Color.WHITE, [(self.width // 3 - 30 ),180], [(self.width // 3 - 30 )-120,300])
        self.line2 = pygame.draw.line(self.game.screen, Color.WHITE, [(self.width // 3 - 30 ),180], [(self.width // 3 - 30 )+120,300])
        self.line3 = pygame.draw.line(self.game.screen, Color.WHITE, [(self.width // 3 - 30 ),180], [(self.width // 3 -30),300])

    def add_buttons(self):
        tech_pos = 0
        image_num = 0
        vertical_move_count = 1
        tile_centered = True  # GridTile должен быть сверху посередине
        for upgrade_index in self.types:
            if image_num ==1:
                pass
            else:
                if self.is_central(upgrade_index) or tile_centered:
                    tile_centered = False
                    tech_pos = 0
                    btn = self.create_button(tech_pos, vertical_move_count, upgrade_index,image_num)
                    self.objects.append(btn)
                    tech_pos = -2
                    vertical_move_count += 1
                else:
                    tech_pos += 1
                    if tech_pos == 0:
                        tech_pos += 1
                    btn = self.create_button(tech_pos, vertical_move_count, upgrade_index,image_num)
                    self.objects.append(btn)
            image_num+=1

    def create_button(self, i, J, upgrade_index,num):
        y_move = 80
        x_move = 120
        img = (pygame.image.load(os.path.join("images","Upgrades", f"{num}.png")))
        x = self.width // 3 - 30 + x_move * i
        y = -60 + y_move * J
        img = pygame.transform.scale(img, (115, 70))
        return ImageButton(self.game, img, (x, y, 115, 70), "", self.upgrade_as_none(upgrade_index,num))

    def create_textes(self, tile):
        gg = tile(self.game_vc.grid_vc.model, self.game_vc.grid_vc.selected_tile.loc_x, self.game_vc.grid_vc.selected_tile.loc_y)
        content = [
            gg.name, None,
            str(gg.owners_income),
            str(gg.power_cap), str(gg.power_growth),
        ]
        self.tile_text_1.update_text("Название: "+content[0])
        self.tile_text_2.update_text(" Доход: "+content[2])
        self.tile_text_3.update_text(" Прирост очков: " + content[3])
        self.tile_text_4.update_text(" Лимит очков: " + content[4])

    def is_central(self, index):
        if str(index).find("Enhanced") != -1:  # даже не пытайтесь найти ключ GridTile, не поможет
            return True

    def udpate_player(self):
        self.start_team = self.current_player_plate.team.current_player


    #TODO: проверка на текущий ход для апгрейд и даунгрейд
    def upgrade_as_none(self, typee, num):
        def upgrade():
            tile = self.game_vc.grid_vc.selected_tile
            if not(self.click_flag[num]):
                self.create_textes(typee)
                for i in range(8):
                    self.click_flag[i] = False
                self.click_flag[num] = True
            else:
                if tile.team == self.current_player_plate.team:
                    if (tile.team.money >= typee.get_upgrade_price()):
                        if (GridTileUpgradeTree.tile_upgrade_bases[typee] == type(tile)):
                            self.game_vc.player_controller.try_upgrade_grid_tile(typee)
                            self.money_text.update_text("Деньги: "+str(self.game.current_scene.game_vc.model.current_team.money))
                        else:
                            self.info_text.update_text("Улучшение недоступно")
                    else:
                        self.info_text.update_text("Нехватает денег для улучшения")
                else:
                    self.info_text.update_text("Выберите клетку своей команды")
                self.click_flag[num] = False
        return upgrade

    def downgrade(self):
        return self.game_vc.player_controller.try_downgrade_grid_tile

    def process_all_draw(self):
        is_downgrade = self.is_downgrade
        if is_downgrade:
            self.objects.append(self.test_button)
        super().process_all_draw()
        if is_downgrade:
            self.objects.pop()
        pygame.draw.line(self.game.screen, Color.WHITE, [(self.width // 3-5), 150],
                         [(self.width // 3) - 120 + 25, 182])
        pygame.draw.line(self.game.screen, Color.WHITE, [(self.width // 3+22), 168],
                         [(self.width // 3+ 22), 182])
        pygame.draw.line(self.game.screen, Color.WHITE, [(self.width // 3)+48, 150],
                         [(self.width // 3) + 142, 182])
        pygame.display.update()


    def process_all_events(self, eventlist):
        is_downgrade = self.is_downgrade
        if is_downgrade:
            self.objects.append(self.test_button)
        super().process_all_events(eventlist)
        if is_downgrade:
            self.objects.pop()

    @property
    def is_downgrade(self):
        tile = self.game_vc.grid_vc.selected_tile
        if tile is None:
            return False
        return GridTileUpgradeTree.tile_upgrade_bases[type(tile)] is not None