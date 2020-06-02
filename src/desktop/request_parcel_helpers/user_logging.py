"""Запросы логина логаута"""

from net_connection.request_ids import RequestID
from ws.parcel_manager import ParcelManager


def send_login_request(login, password):
    """Отпрака запроса логина"""
    parcel = [RequestID.LOGIN, login, password]
    ParcelManager.send_parcel(parcel)


def send_logout_request():
    """Отправка запроса логаута"""
    parcel = [RequestID.LOGOUT]
    ParcelManager.send_parcel(parcel)
