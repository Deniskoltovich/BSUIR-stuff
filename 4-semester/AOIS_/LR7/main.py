from random import randint

class Processor:
    def __init__(self, word_size, size, data=None):
        if data:
            self.data = data
        else:
            self.data = ["".join([str(randint(0, 1)) for _ in range(word_size)]) for _ in range(size)]
            
    
    def search(self, search_str):
        max_match = 0
        match_indices = []
        
        for i, item in enumerate(self.data):
            match_count = 0
            
            for j in range(len(search_str)):
                if search_str[j] == item[j]:
                    match_count += 1
                
            if match_count > max_match:
                max_match = match_count
                match_indices = [i]
            elif match_count == max_match:
                match_indices.append(i)
        
        return [self.data[i] for i in match_indices]

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
        copied_data = [word for word in self.data]
        for i in range(len(copied_data)):
            item = max(copied_data)
            sorted_data.append(item)
            copied_data.remove(item) 
        if not reverse:
            return sorted_data[::-1]
        
        return sorted_data

    def get_max(self):
        max_word = self.data[0]
        for word in self.data:
            if self.compare(word, max_word) != -1:
                max_word = word
        
        return max_word              
    

if __name__ == '__main__':
    processor = Processor(3, 10)
    
    print(f'Сортировка по возрастанию: {processor.sort(reverse=False)}')
    print(f'Сортировка по убыванию: {processor.sort(reverse=True)}')

    print(f'Поиск по соответствию: {processor.search("111")}')  
    print(f'Поиск по соответствию: {processor.search("101")}')  
    print(f'Поиск по соответствию: {processor.search("000")}')  
    print(f'Поиск по соответствию: {processor.search("1x0")}')  


                
    

                
        
    
