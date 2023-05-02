class HashTableNode:
    def __init__(self, key, value, next = None):
        self.key = key
        self.value = value
        self.next = None
        

class HashTable:
    ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    def __init__(self, size: int) -> None:
        self.list = [0] * size
        self.size = size
        

        
    def hash_func(self, key: str):
        return (self.ALPHABET.index(key[0].upper()) * 33 + self.ALPHABET.index(key[1].upper())) % self.size
    
    
    def insert(self, key, value):
        hash_key = self.hash_func(key)
        if not self.list[hash_key]:
            self.list[hash_key] = HashTableNode(key, value)
        else:
            node = self.list[hash_key]
            while node:
                if node.key == key:
                    node.value = value
                    return None
                node = node.next
            new_node = HashTableNode(key, value)
            new_node.next = self.list[hash_key]
            self.list[hash_key] = new_node

    def search(self, key):
        hash_key = self.hash_func(key)
        node = self.list[hash_key]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(key)

    def remove(self, key):
        hash_key = self.hash_func(key)
        node = self.list[hash_key]
        if not node:
            raise KeyError(key)
        
        index = 0
        prev = 0
        while node:
            if node.key == key:
                if index == 0:
                    self.list[hash_key] = node.next
                    
                elif index == self.size - 1:
                    prev.next = None
                    
                else:
                     prev.next = node.next
                return None
            prev = node
            node = node.next
            index += 1

        raise KeyError(key)       



    def print(self):
        table = []
        for i in range(self.size):
            current = self.list[i]
            elements = []
            while current:
                elements.append((current.key, current.value))
                current = current.next
            print(elements)
                



if __name__ == '__main__':
 

    table = HashTable(10)
 

    table.insert("Дифференциал", 'анализ')
    table.insert("Интеграл", 'анализ')
    table.insert("Уравнение", 'алгебра')
    table.insert("Матрица", 'линейная алгебра')
    table.insert("Функция", 'анализ')
    table.insert("Множество", 'теория множеств')
    table.insert("Граф", 'теория графов')
    table.insert("Функция", 'анализ')
    table.insert("Множество", 'теория множеств')


 
    print(table.search("Дифференциал"))
    print(table.search("Матрица"))
 
    table.remove("Функция")

    table.print()
    