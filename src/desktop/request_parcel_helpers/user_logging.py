from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID


def send_login_request(login, password):
    parcel = [RequestID.LOGIN, login, password]
    ParcelManager.send_parcel(parcel)


def send_logout_request():
    parcel = [RequestID.LOGOUT]
    ParcelManager.send_parcel(parcel)
