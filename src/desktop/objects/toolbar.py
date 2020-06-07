import pygame

from objects.base import DrawObject
from objects.toolbar_cell import ToolBarCell


class ToolBar(DrawObject):
    PTS_KEYS = None

    @staticmethod
    def init_pts_keys():
        from game_eng.pressure_tool_set_ders.ddos_pts import DDosPTSet
        from game_eng.pressure_tool_set_ders.phishing_pts import PhishingPTSet
        from game_eng.pressure_tool_set_ders.exploit_pts import ExploitPTSet
        from game_eng.pressure_tool_set_ders.virus_pts import VirusPTSet
        from game_eng.pressure_tool_set_ders.encryption_pts import EncryptionPTSet
        # ...
        from game_eng.pressure_tool_set_ders.antivirus_pts import AntivirusPTSet
        from game_eng.pressure_tool_set_ders.mining_farm_pts import MiningFarmPTSet
        from game_eng.pressure_tool_set_ders.reboot_pts import RebootPTSet
        ToolBar.PTS_KEYS = {
            DDosPTSet: "K_1",
            PhishingPTSet: "K_2",
            ExploitPTSet: "K_3",
            VirusPTSet: "K_4",
            EncryptionPTSet: "K_5",
            # ...
            AntivirusPTSet: "K_8",
            MiningFarmPTSet: "K_9",
            RebootPTSet: "K_0",
        }

    def __init__(self, game, geometry: tuple, game_model):
        super().__init__(game)
        self.cells = []
        self.geometry = geometry
        self.game_model = game_model
        self.tools = dict()
        self.__init_cells()
        self.update_tools()

    def update_tools(self):
        self.tools.clear()
        player = self.game_model.current_player
        for pts_type, pt_set in player.pressure_tools.items():
            key = ToolBar.PTS_KEYS[pts_type]
            self.tools[key] = pt_set
        self.__update_cell_tools()

    def __init_cells(self):
        for i in range(10):
            num = (i + 1) % 10
            x = self.geometry[0] + i * 74
            y = self.geometry[1]
            self.cells.append(ToolBarCell(self.game, x, y, 64, 64, num))

    def __update_cell_tools(self):
        for i in range(10):
            num = (i + 1) % 10
            key = "K_" + str(num)
            tool = self.tools[key] if key in self.tools else None
            self.cells[i].update_pt_set(tool)

    def process_event(self, event):
        if event.type == pygame.KEYUP:
            num = event.key - 48
            if num == 0:
                num = 9
            else:
                num -= 1
            if 9 >= num >= 0:
                self.cells[num].process_event(event)
        else:
            for item in self.cells:
                item.process_event(event)

    def process_draw(self):
        for item in self.cells:
            item.process_draw()


ToolBar.init_pts_keys()
