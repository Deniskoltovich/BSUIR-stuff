class HashTable:
    ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    class HashTableNode:
        def __init__(self, key, value, next=None):
            self.key = key
            self.value = value
            self.next = next
    
    
    def __init__(self, tab_size: int) -> None:
        self.list = [0] * tab_size
        self.tab_size = tab_size 

        
    def hash_func(self, key: str):
        return (self.ALPHABET.index(key[0].upper()) * 33 + self.ALPHABET.index(key[1].upper())) % self.tab_size
    
    def find(self, key):
        hash_key = self.hash_func(key)
        cur_node = self.list[hash_key]
        while cur_node:
            if cur_node.key == key:
                return cur_node.value
            cur_node = cur_node.next
        raise KeyError(key)
    
    
    def insert(self, key, value):
        hash_key = self.hash_func(key)
        if not self.list[hash_key]:
            self.list[hash_key] = self.HashTableNode(key, value)
        else:
            cur_node = self.list[hash_key]
            while cur_node:
                if cur_node.key == key:
                    cur_node.value = value
                    return None
                cur_node = cur_node.next
            new_node, new_node.next  = self.HashTableNode(key, value), self.list[hash_key]
            self.list[hash_key] = new_node


    def pop(self, key):
        hash_key = self.hash_func(key)
        cur_node = self.list[hash_key]
        if not cur_node:
            raise KeyError(key)
    
        index, prev = 0, 0
        while cur_node:
            if cur_node.key == key:
                if index == 0:
                    self.list[hash_key] = cur_node.next
                elif index + 1 == self.tab_size:
                    prev.next = None
                else:
                     prev.next = cur_node.next
                return None
            prev, cur_node = cur_node, cur_node.next
            index += 1

        raise KeyError(key)       


    def print(self):
        for i in range(self.tab_size):
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


 
    print(table.find("Дифференциал"))
    print(table.find("Матрица"))
 
    print(table.find("Функция"))
    table.print()
    