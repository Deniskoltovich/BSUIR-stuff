class Deque:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def pushFront(self, item):
        self.items.insert(0, item)

    def pushBack(self, item):
        self.items.append(item)

    def removeFront(self):
        return self.items.pop(0)

    def removeBack(self):
        return self.items.pop()

    def output(self):
        print('deque: [', end=" ")
        for i in self.items:
            print(i, end=" ")
        print("]")