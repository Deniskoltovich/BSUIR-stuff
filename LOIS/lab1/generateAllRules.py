class GenerateAllRules:
    def __init__(self, sets_symbols):
        self.sets_symbols = sets_symbols
        self.rules = []

    def generate(self):
        for i in range(len(self.sets_symbols)):
            for j in range(len(self.sets_symbols)):
                if i != j:
                    self.rules.append([self.sets_symbols[i], self.sets_symbols[j]])
        return self.rules
