import unittest

from game_eng.game_model import create_new_game_model, GameModel
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class CoreTester(unittest.TestCase):
    def create_game_model(self):
        return create_new_game_model("", 1, 500, [{"team": 0, "uid": 1, "name": "1"},
                                           {"team": 1, "uid": 2, "name": "2"},
                                           {"team": 2, "uid": 3, "name": "3"}])

    def test_create_game_model(self):
        self.create_game_model()

    def test_save_load_game_model(self):
        game = self.create_game_model()
        stream = BinaryWriter()
        GameModel.write(stream, game)
        stream = BinaryReader(stream.base_stream)
        game = GameModel.read(stream)

    def test_next_game_turn(self):
        game = self.create_game_model()
        game.next_player_turn()
