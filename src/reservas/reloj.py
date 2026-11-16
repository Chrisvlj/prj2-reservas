from datetime import datetime


class RelojSistema:
    def ahora(self) -> datetime:
        return datetime.now().replace(microsecond=0)


class RelojFijo:
    def __init__(self, momento: datetime):
        self.momento = momento

    def ahora(self) -> datetime:
        return self.momento
