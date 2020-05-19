from .service_tile import ServiceGridTile


class ServiceGridTilePlus(ServiceGridTile):
    @staticmethod
    def get_upgrade_price() -> int:
        return 48

    @property
    def owners_income(self) -> int:
        return 8

    @property
    def power_growth(self) -> int:
        return 0

    @property
    def power_cap(self) -> int:
        return 64

    @property
    def name(self) -> str:
        return super().name + " +"
