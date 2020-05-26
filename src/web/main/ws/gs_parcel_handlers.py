from net_connection.error_response import ErrorResponse, ErrorResponseID
from channels.generic.websocket import WebsocketConsumer
from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from net_connection.participation_status_ids import ParticipationStatusIDs
from .logged_in_sockets import LoggedInSockets
from main.models import UserParticipation


class GSParcelHandlers:
    @staticmethod
    def handle_get_participation_status_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 1:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        user = LoggedInSockets.users_of_sockets[socket]
        participation = UserParticipation.objects.filter(user=user)
        if len(participation) == 0:
            status = ParticipationStatusIDs.NO_PARTICIPATION
        else:
            phase = participation[0].game_session.phase
            status = ParticipationStatusIDs.WAITING_FOR_BEGINNING if phase == 0 else ParticipationStatusIDs.PLAYING_GAME
        return [ResponseID.SUCCESS, status]


RequestParcelHandlers.register_handler(GSParcelHandlers.handle_get_participation_status_request,
                                       RequestID.GET_PARTICIPATION_STATUS)
