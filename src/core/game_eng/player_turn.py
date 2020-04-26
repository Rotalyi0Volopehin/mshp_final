import exceptions

from game_eng.player_action import PlayerAction


class PlayerTurn:
    def __init__(self):
        self.actions = []

    def try_act(self, action: PlayerAction) -> bool:
        if not isinstance(action, PlayerAction):
            raise exceptions.ArgumentTypeException()
        if action.try_do():
            self.actions.append(action)
            return True
        return False

    def try_undo(self) -> bool:
        action = self.actions[-1]
        if action.try_undo():
            self.actions.pop(-1)
            return True
        return False

    def sync(self):
        for action in self.actions:
            if not action.try_do():
                raise exceptions.InvalidOperationException(f"Sync failed on execution of '{type(action)}'!")

    def reset(self):
        self.actions.clear()
