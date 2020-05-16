class Player:
    def __init__(self, username='Guest', lvl=0, login='qwe', password='123'):
        self.lvl = lvl
        self.login = login
        self.password = password
        self.username = username

    def set_user(self, login, password):
        self.login = login
        self.password = password



