# TODO: задокументировать


# отнаследованные классы должны храниться в папке core/game_eng/turn_orders/
class TurnOrder:  # abstract
    def try_execute(self) -> bool:
        return True
