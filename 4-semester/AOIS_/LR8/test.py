import random

class AssociativeMemory:
    def __init__(self, size):
        self.memory = [[0] * size for _ in range(size)]
        self.size = size


    def convert_to_diagonal(self):
        diagonal_memory = []
        for i in range(len(self.memory)):
            shifted_word = self.shift(self.memory[i], i)
            diagonal_memory.append(shifted_word)
        self.memory = list(zip(*diagonal_memory))
        
    def shift(self, word: list, index: int):
        flag = False
        if index < 0:
            index = -index
            flag = True
        word = list(word)
        for _ in range(index):
            if not flag:
                word.insert(0,word.pop())
            else:
                word.append(word.pop(0))

        return list(word)

    def convert_from_diagonal(self):
        self.memory = list(zip(*self.memory))
        memory = []
        for i in range(len(self.memory)):
            reverse_shifted_word = self.shift(self.memory[i], -i)
            memory.append(reverse_shifted_word)
        self.memory = memory

    def read_column(self, column:int):  
        column_data = [self.memory[i][(i + column) % self.size] for i in range(self.size)]
        return column_data

    def write_column(self, column: int, data: list):
        self.memory = list(map(list, self.memory))
        for i in range(self.size):
            word = self.read_word(i)
            word[column] = data[i]
            self.write_word(i, word)
        
            
    def read_word(self, index:int):
        return self.shift(self.memory[index], -index)
        
    def write_word(self, index: int, data: list):
        shifted_word = self.shift(data, index)
        self.memory = list(map(list, self.memory))
        for i in range(self.size):
            self.memory[i][index] = shifted_word[i]
        
        
    @staticmethod
    def f6(digit1: int, digit2: int):
        return int((not digit1 and digit2) or (digit1 and not digit2))

    @staticmethod
    def f9(digit1: int, digit2: int):
        return int((digit1 and digit2) or (not digit1 and not digit2))

    @staticmethod
    def f4(digit1: int, digit2: int):
        return int(not digit1 and digit2)

    @staticmethod
    def f11(digit1: int, digit2: int):
        return int(digit1 or not digit2)   
        
    def perform_logical_operation(self, operation:str, ind1, ind2):
        col1, col2 = self.read_column(ind1), self.read_column(ind2)
        operations = {'f4': self.f4,
                      'f6': self.f6,
                      'f9' : self.f9,
                      'f11' : self.f11
                      }
        
        return ''.join(list(map(lambda x: str(operations[operation](*x)), list(zip(col1, col2)))))

    def perform_arithmetic_operation(self, V: str):
        index = 0
        founded = []
        V = list(map(int, V))
        for i in range(self.size):
            word = self.read_word(i)
            if word[:3] == V:
                index = i
                founded = word
                
        print(founded)
        a, b = founded[3:7], founded[7:11]
        new_word = founded[:11] + self.arithmetic_operation(a,b)
        return " ".join(list(map(str, new_word))), index
        
    def arithmetic_operation(self, word1, word2):
        num1 = [int(x) for x in word1]
        num2 = [int(x) for x in word2]
        ans = ''
        carry = 0
        while num1 or num2 or carry:
            first = num1.pop() if num1 else 0
            sec = num2.pop() if num2 else 0
            temp_sum = first + sec + carry
            ans = str(temp_sum % 2) + ans
            carry = temp_sum // 10

        return list(ans)
        
    def find_flags(self, word_1: str, word_2: str):
        cur_g, cur_l = 0, 0
        for ind, word in enumerate(self.data):
            digit_1, digit_2 = list(map(lambda x: bool(int(x)), [word_1[ind], word_2[ind]] ))
            next_g = cur_g or (not digit_2 and digit_1 and not cur_l)
            next_l = cur_l or (digit_2 and not digit_1 and not cur_g)
            cur_g, cur_l = next_g, next_l
        return bool(cur_g), bool(cur_l)
    
    def compare(self, word_1: str, word_2: str):
        match self.find_flags(word_1, word_2):
            case (True, False): return 1
            case (False, True): return -1
            case (False, False): return 0
        
        raise KeyError()
    
    def sort(self, reverse=True):
        sorted_data = []
        copied_data = [''.join(list(map(str,self.read_word(i)))) for i in range(self.size)]
        for _ in range(len(copied_data)):
            item = max(copied_data)
            sorted_data.append(item)
            copied_data.remove(item) 
        if not reverse:
            return sorted_data[::-1]
        
        memory = list(map(list, sorted_data))
        self.memory = memory
        self.convert_to_diagonal()

    def get_max(self):
        max_word = ''.join(self.data[0])
        for word in self.data:
            if self.compare(''.join(word), max_word) != -1:
                max_word = word
        
        return max_word              
        

    def print_memory(self):
        for row in self.memory:
            print(' '.join(map(str, row)))



if __name__== '__main__':
        
    memory = AssociativeMemory(16)

    for i in range(16):
        column = [random.randint(0,1) for _ in range(16)]
        memory.write_column(i, column)

    print("Original Memory:")
    memory.print_memory()

    memory.convert_to_diagonal()
    print("\nMemory with Diagonal Addressing:")
    memory.print_memory()

    memory.convert_from_diagonal()
    print("\nMemory with Original Addressing:")
    memory.print_memory()
    memory.convert_to_diagonal()
    
    
    word = [random.randint(0,1) for _ in range(16)]
    index = 2
    print(f'\nWriting word {word} on index {index}\nMemory:')
    memory.write_word(index, word)
    memory.print_memory()


    column = [random.randint(0,1) for _ in range(16)]
    index = 2
    print(f'\nWriting column {column} on index {index}\nMemory:')
    memory.write_column(index, column)
    memory.print_memory()
    
    print('\nLogical operations')
    print('!x1*x2', f'x1= 1st col = {memory.read_column(0)}', f'x2= 2nd col = {memory.read_column(1)}', sep='\n')
    print(f'result = {memory.perform_logical_operation("f4", 0, 1)}')
    print()
    print('!x1*x2 + x1*!x2', f'x1= 1st col = {memory.read_column(0)}', f'x2= 2nd col = {memory.read_column(1)}', sep='\n')
    print(f'result = {memory.perform_logical_operation("f6", 0, 1)}')
    print()
    print('x1*x2 + !x1*!x2', f'x1= 1st col = {memory.read_column(0)}', f'x2= 2nd col = {memory.read_column(1)}', sep='\n')
    print(f'result = {memory.perform_logical_operation("f9", 0, 1)}')
    print()
    print('x1 + !x2', f'x1= 1st col = {memory.read_column(0)}', f'x2= 2nd col = {memory.read_column(1)}', sep='\n')
    print(f'result = {memory.perform_logical_operation("f11", 0, 1)}')
    print('\nArithmetic operations')
    
    print('V = 110')
    result, index = memory.perform_arithmetic_operation("110")
    print(f'founded word index = {index}', sep='\n')
    print(f'result = {result}')
    
    print('\nSorting words in memory')
    memory.sort()
    print('\nSorted with Diagonal Addressing\n')
    memory.print_memory()
    memory.convert_from_diagonal()
    
    print('\nSorted with Original Addressing\n')

    memory.print_memory()
    
