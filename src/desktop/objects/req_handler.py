import os
"""
Позволяет находить требования выбора определённых опций диалогов и проверяет,
удовлетворяют ли характеристики и знакомства персонажа требованиям.
"""


STATS = {
    "{dex :",
    "{str :",
    "{cha :",
    "{sav :",
    "{ste :"
}

CONTACTS = {
    "{swan",
    "{krayn",
    "{smith",
    "{finch"
}


class ReqHandler:
    def __init__(self, data):
        self.data = data
        self.stats_requirements = []
        self.contacts_requirements = []
        self.now_word = 0

    def find_requirements(self, now_word):
        """
        Ищет требования в диалоговом файле.
        :param now_word:
        :return:
        """
        self.now_word = now_word
        for word in STATS:
            end_of_line = self.data.find('\n', self.now_word)
            if self.data.find(word, self.now_word, end_of_line) != -1:
                self.stats_requirements.append(self.data[self.data.find(word, self.now_word) + 1:
                                               self.data.find('}', self.now_word)])
                self.now_word = self.data.find('}', self.now_word)
        self.now_word = now_word
        for word in CONTACTS:
            end_of_line = self.data.find('\n', self.now_word)
            if self.data.find(word, self.now_word, end_of_line) != -1:
                self.contacts_requirements.append(self.data[self.data.find(word, self.now_word) + 1:
                                                  self.data.find('}', self.now_word)])
                self.now_word = self.data.find('}', self.now_word)

    def check_requirements(self):
        """
        Проверяет возможность выбора диалоговой ветки.
        :return:
        """
        path = os.path.join("quests", "stats")
        file = open(path, 'r')
        stat_data = file.read()
        flag = 2
        for item in self.stats_requirements:
            if int(stat_data[stat_data.find(item[:5]) + 5:
                             stat_data.find('|', stat_data.find(item[:5]))
                             ]) < int(item[5:]):
                flag = 1
            else:
                flag = 0
        for item in self.contacts_requirements:
            if stat_data.find(item) == -1:
                flag = 1
            else:
                flag = 0
        file.close()
        self.contacts_requirements = []
        self.stats_requirements = []
        return flag
