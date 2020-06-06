import exceptions
import user_info

from game_eng.player_action_ders.move_grid_tile_power_action import MoveGridTilePowerPlayerAction
from game_eng.player_action_ders.apply_pt_action import ApplyPTPlayerAction
from game_eng.player_action_ders.upgrade_grid_tile_action import UpgradeGridTilePlayerAction
from game_eng.player_action_ders.downgrade_grid_tile_action import DowngradeGridTilePlayerAction


class PlayerController:
    def __init__(self, game_vc):
        self.game_vc = game_vc

    @property
    def changes_available(self) -> bool:
        return (self.game_vc.model.current_player.id == user_info.user_id) or not user_info.online

    def try_move_power(self, value: int) -> bool:
        if not isinstance(value, int):
            raise exceptions.ArgumentTypeException()
        if not self.changes_available:
            return False
        try:
            player = self.game_vc.model.current_player
            target = self.game_vc.grid_vc.target_tile
            selected = self.game_vc.grid_vc.selected_tile
            action = MoveGridTilePowerPlayerAction(player, target, selected, value)
            return self.game_vc.model.current_player_turn.try_act(action)
        except exceptions.InvalidOperationException:
            return False

    def try_apply_pressure_tool(self, pts_type) -> bool:
        if not self.changes_available:
            return False
        try:
            player = self.game_vc.model.current_player
            target = self.game_vc.grid_vc.target_tile
            pt_set = player.pressure_tools[pts_type]
            action = ApplyPTPlayerAction(player, target, pt_set)
            return self.game_vc.model.current_player_turn.try_act(action)
        except (exceptions.InvalidOperationException, KeyError):
            return False

    def try_upgrade_grid_tile(self, upgrade: type) -> bool:
        if not isinstance(upgrade, type):
            raise exceptions.ArgumentTypeException()
        if not self.changes_available:
            return False
        try:
            player = self.game_vc.model.current_player
            target = self.game_vc.grid_vc.selected_tile
            action = UpgradeGridTilePlayerAction(player, target, upgrade)
            return self.game_vc.model.current_player_turn.try_act(action)
        except exceptions.InvalidOperationException:
            return False

    def try_downgrade_grid_tile(self) -> bool:
        if not self.changes_available:
            return False
        try:
            player = self.game_vc.model.current_player
            target = self.game_vc.grid_vc.selected_tile
            action = DowngradeGridTilePlayerAction(player, target)
            return self.game_vc.model.current_player_turn.try_act(action)
        except exceptions.InvalidOperationException:
            return False
