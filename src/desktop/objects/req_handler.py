STATS = {
    "{dex :",
    "{str :",
    "{cha :",
    "{sav :",
    "{ste :"
}


class ReqHandler:
    def __init__(self, data):
        self.data = data
        self.requirements = []

    def find_requirements(self, now_word):
        self.now_word = now_word
        for word in STATS:
            end_of_line = self.data.find('\n', self.now_word)
            if self.data.find(word, self.now_word, end_of_line) != -1:
                self.requirements.append(self.data[self.data.find(word, self.now_word) + 1:
                                         self.data.find('}', self.now_word)])
                self.now_word = self.data.find('}', self.now_word)

    def check_requirements(self):
        f = open('quests/config', 'r')
        stat_data = f.read()
        flag = 2
        for item in self.requirements:
            print(item)
            if int(stat_data[stat_data.find(item[:5]) + 5:
                            stat_data.find('|', stat_data.find(item[:5]))
                            ]) < int(item[5:]):
                flag = 1
            else:
                flag = 0
        f.close()
        self.requirements = []
        return flag