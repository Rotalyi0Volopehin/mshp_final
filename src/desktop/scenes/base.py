import pygame

from constants import Color


class Scene:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.create_objects()

    def create_objects(self):
        pass

    def process_frame(self, eventlist):
        self.process_all_events(eventlist)
        self.process_all_logic()
        self.process_all_draw()

    def process_all_events(self, eventlist):
        for event in eventlist:
            self.process_current_event(event)

    def process_current_event(self, event):
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def additional_event_check(self, event):
        pass

    def process_all_logic(self):
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def additional_logic(self):
        pass

    def process_all_draw(self):
        self.screen.fill(Color.BLACK)
        for item in self.objects:
            item.process_draw()
        self.additional_draw()
        pygame.display.flip()  # double buffering

    def additional_draw(self):
        pass

    # event
    def on_gone_to_deeper_scene_from_this(self):
        pass

    # event
    def on_closed(self):
        pass

    # event
    def on_returned_to_this_scene(self):
        pass
