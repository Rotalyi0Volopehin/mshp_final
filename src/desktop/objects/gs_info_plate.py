from .base import DrawObject
from net_connection.response_ids import ResponseID
from net_connection.participation_status_ids import ParticipationStatusID
from .text import Text
from .button import Btn
from datetime import datetime


class GSInfoPlate(DrawObject):
    def __init__(self, game, pos_x, pos_y, play_button_func, get_gs_func, auto_update_period=-1, auto_update_func=None):
        super().__init__(game)
        self.participation_status = None
        self.gs_title = None
        self.gathered_players_count = self.players_must_participate = None
        self.auto_update_period = auto_update_period
        self.auto_update_ticks_left = 0
        self.auto_update_func = auto_update_func
        self.participation_status_label = Text(game, is_bold=True, font_size=20, x=pos_x, y=pos_y)
        self.gs_title_label = Text(game, font_size=20, x=pos_x, y=pos_y + 20)
        self.player_count_label = Text(game, font_size=20, x=pos_x, y=pos_y + 40)
        self.update_labels()
        self.enter_gs_button = Btn(game, (pos_x - 50, pos_y + 20, 100, 40), text="Играть", function=play_button_func)
        self.waiting_for_first_turn_state_end_time = None
        self.waiting_for_first_turn_time_left_was = None
        self.get_gs_func = get_gs_func

    def update_labels(self):
        if self.participation_status is None:
            participation_status = "..."
        elif self.participation_status == ParticipationStatusID.NO_PARTICIPATION:
            participation_status = "Вы не участвуете в игровой сессии"
        elif self.participation_status == ParticipationStatusID.WAITING_FOR_BEGINNING:
            participation_status = "Набор игроков ..."
            self.gs_title_label.update_text("Название сессии : " + self.gs_title)
            self.player_count_label.update_text(
                f"Игроков набралось {self.gathered_players_count}/{self.players_must_participate}")
        elif self.waiting_for_first_turn_state_end_time is None:
            participation_status = "..."
        elif self.waiting_for_first_turn_time_left > 0.0:
            participation_status = f"Игра начнётся через {self.waiting_for_first_turn_time_left} секунд"
        else:
            participation_status = "Игра идёт"
        self.participation_status_label.update_text(participation_status)

    @property
    def waiting_for_first_turn_time_left(self) -> int:
        return int(self.waiting_for_first_turn_state_end_time - datetime.utcnow().timestamp())

    def set_waiting_for_first_turn_state(self, beginning_time: datetime):
        self.waiting_for_first_turn_state_end_time = beginning_time.timestamp()

    def update_info_from_parcel(self, parcel: list):
        if parcel[0] == ResponseID.FAIL:
            raise Exception("Fail - error 400!")
        self.participation_status = parcel[1]
        if len(parcel) > 2:
            if self.participation_status != ParticipationStatusID.NO_PARTICIPATION:
                self.gs_title = parcel[2]
                self.gathered_players_count = parcel[3]
                self.players_must_participate = parcel[4]
                if self.participation_status == ParticipationStatusID.PLAYING_GAME:
                    self.auto_update_period = -1
                    self.get_gs_func()
        self.update_labels()

    def process_logic(self):
        if self.auto_update_period >= 0:
            if self.auto_update_ticks_left == 0:
                self.auto_update_ticks_left = self.auto_update_period
                self.auto_update_func()
            self.auto_update_ticks_left -= 1
        if self.waiting_for_first_turn_state_end_time is not None:
            if self.waiting_for_first_turn_time_left != self.waiting_for_first_turn_time_left_was:
                self.waiting_for_first_turn_time_left_was = self.waiting_for_first_turn_time_left
                self.update_labels()

    def process_draw(self):
        self.participation_status_label.process_draw()
        if self.participation_status == ParticipationStatusID.WAITING_FOR_BEGINNING:
            self.gs_title_label.process_draw()
            self.player_count_label.process_draw()
        elif (self.waiting_for_first_turn_state_end_time is not None) and \
                (self.waiting_for_first_turn_time_left <= 0):
            self.enter_gs_button.process_draw()

    def process_event(self, event):
        if self.participation_status == ParticipationStatusID.PLAYING_GAME:
            self.enter_gs_button.process_event(event)
