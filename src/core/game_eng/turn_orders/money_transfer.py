from game_eng.turn_order import TurnOrder
from game_eng.player import Player

import exceptions


# TODO: задокументировать


class MoneyTransferOrder(TurnOrder):
    def __init__(self, money_to_transfer_amount: int, giver: Player, target_player: Player):
        # vvv проверка параметров vvv
        if not (isinstance(money_to_transfer_amount, int) and
                isinstance(giver, Player) and isinstance(target_player, Player)):
            raise exceptions.ArgumentTypeException()
        if money_to_transfer_amount < 0:
            raise exceptions.ArgumentValueException()
        # vvv инициализация vvv
        self.money_to_transfer_amount = money_to_transfer_amount
        self.giver = giver
        self.target_player = target_player

    def try_execute(self) -> bool:
        if self.money_to_transfer_amount > self.giver.money:
            return False
        self.giver.money -= self.money_to_transfer_amount
        self.target_player.money += self.money_to_transfer_amount
        return True
