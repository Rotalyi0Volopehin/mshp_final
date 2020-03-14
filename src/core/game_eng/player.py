import exceptions

from game_eng.turn_order import TurnOrder
from game_eng.game_object_model import GameObjectModel


# TODO: задокументировать


class Player(GameObjectModel):
    def __init__(self, money: int, team: int):
        # vvv проверка параметров vvv
        if not (isinstance(money, int) and isinstance(team, int)):
            raise exceptions.ArgumentTypeException()
        if (team < -1) or (team > 2) or (money < 0):
            raise exceptions.ArgumentValueException()
        # vvv инициализация vvv
        self.money = money
        self.__team = team
        self.__turn_orders_stack = []
        self.__order_exec_index = 0

    @property
    def team(self) -> int:
        return self.__team

    @property
    def are_orders_in_execution(self):
        return self.__order_exec_index >= len(self.__turn_orders_stack)

    def __check_orders_are_not_in_exec(self):
        if self.are_orders_in_execution:
            raise exceptions.InvalidOperationException("Orders are in execution!")

    def push_order(self, order: TurnOrder):
        if not isinstance(order, TurnOrder):
            raise exceptions.ArgumentTypeException()
        self.__check_orders_are_not_in_exec()
        self.__turn_orders_stack.append(order)

    def pop_order(self):
        self.__check_orders_are_not_in_exec()
        self.__turn_orders_stack.pop()

    # необходимо выполнять в конце каждого хода
    # выполнять по очереди для каждого члена фракции, пока все не выдатут False
    # параметр exec_fail_handler - это обработчик невыполненных запросов; аргументом принимает невыполненный запрос
    def try_execute_order(self, exec_fail_handler=None) -> bool:
        if self.__order_exec_index >= len(self.__turn_orders_stack):
            return False
        order = self.__turn_orders_stack[self.__order_exec_index]
        if not order.try_execute():
            if exec_fail_handler is not None:
                exec_fail_handler(order)
        self.__order_exec_index += 1
        return True

    def reset_orders(self):
        self.__order_exec_index = 0
        self.__turn_orders_stack.clear()

    def process_logic(self):
        self.reset_orders()
