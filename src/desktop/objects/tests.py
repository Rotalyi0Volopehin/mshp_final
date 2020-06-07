import os
import sys
import unittest
import pygame


def fix_project_roots(*root_names):
    current_path = os.path.abspath(sys.modules[__name__].__file__)
    src_path = current_path[:current_path.find("src") + 4]
    for root_name in root_names:
        sys.path.append(src_path + root_name)

try:
    import exceptions
except:
    print("Direct import failed. Patching . . . ", end='')
    fix_project_roots("core", "desktop", "web")
    import exceptions
    print("SUCCESS")


from game import Game
from .text_bar import TextBar
from .image_handler import ImageHandler
from run import init_libs
init_libs()


class TextBarTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = Game()
        self.TextBarT = TextBar(self.g, file_name='test_data_0', path_to_file='quests/test/')
        self.path_test = os.path.join('quests', 'test', '')

    def test_simple(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_0', '')
        self.assertEqual(TextBar.search_btns(self.TextBarT, self.TextBarT.data), 2)

    def test_empty(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_1', '')
        self.assertEqual(TextBar.search_btns(self.TextBarT, self.TextBarT.data), 1)

    def test_big(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_2', '')
        self.assertEqual(TextBar.search_btns(self.TextBarT, self.TextBarT.data), 49)

    def test_set_next_dialog(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_3', '')
        self.TextBarT.is_start = True
        self.assertEqual(self.TextBarT.set_next_dialog(), None)

    def test_choose_option(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_3', '')
        self.TextBarT.choose_option()
        self.assertEqual(len(self.TextBarT.buttons), 1)

    def test_draw(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_3', '')
        self.TextBarT.set_next_dialog()
        self.assertEqual(self.TextBarT.process_draw(), None)

    def test_process_logic_null(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_3', '')
        self.assertEqual(self.TextBarT.process_logic(), None)

    def test_next_event_unbound(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_0', '')
        self.assertRaises(UnboundLocalError, self.TextBarT.set_next_ev, '3')

    def test_choice_1_unbound(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_0', '')
        self.assertRaises(UnboundLocalError, self.TextBarT.choice_1)

    def test_choice_2_unbound(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_0', '')
        self.assertRaises(UnboundLocalError, self.TextBarT.choice_2)

    def test_choice_3_unbound(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_0', '')
        self.assertRaises(UnboundLocalError, self.TextBarT.choice_3)

    def test_process_empty_event(self):
        self.TextBarT.data = self.TextBarT.get_data_ff(self.path_test, 'test_data_0', '')
        self.assertRaises(AttributeError, self.TextBarT.process_event, pygame.event)


class ImageHandlerTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.g = Game()
        self.image_handler_t = ImageHandler(self.g)

    def test_empty_data(self):
        data = ""
        self.image_handler_t.find_characters(data)
        self.assertEqual(self.image_handler_t.found_characters, [])

    def test_small_data(self):
        data = "Симмонс: иди"
        response = ["Симмонс:"]
        self.image_handler_t.find_characters(data)
        self.assertEqual(self.image_handler_t.found_characters, response)

    def test_big_data(self):
        data = "Симмонс: иди" \
               "Лилия Свон: стой"
        self.image_handler_t.find_characters(data)
        response = ["Симмонс", "Лилия Свон"]
        self.assertEqual(self.image_handler_t.found_characters, response)
