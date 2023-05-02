from itertools import permutations
from lab3_lib.lab2copy import TruthTableRow
from lab3_lib.lab_lib import Minimizer

def get_h(q: int, q0: int):
    return int(not(q == q0))

def create_h_truth_table():
    truth_table = []
    for ind, row in enumerate(h_table):
        truth_table_item = []
        for i, elem in enumerate(row):
            inter = TruthTableRow({'q1*': q0_table[ind][i],
                                   'q2*': q0_table[ind + 1][i],
                                   'q3*': q0_table[ind + 2][i],
                                   },
                                  elem)
            truth_table_item.append(inter)
            
        truth_table.append(truth_table_item)
        break
    return truth_table



def print_tables():
    
    for ind, row in enumerate(q0_table):
        print(f'q{ind + 1}*', *row)
          
    print()
    for ind, row in enumerate(q_table):
        print(f' q{ind + 1}', *row)
        
    print()
    for ind, row in enumerate(h_table):
        print(f' h{ind + 1}', *row)
        
        
def create_tables():
    q_table = [[0, 0, 0, 1, 1, 1, 1, 0],
               [0, 1, 1, 0, 0, 1, 1, 0],
                [1, 0, 1, 0, 1, 0, 1, 0],]
    
    q0_table = [[0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 1, 1, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1]] 
    
    h_table = []
    
    for q_ind ,row in enumerate(q_table):
        h = []
        for ind in range(len(row)):
            h.append(get_h(row[ind], q0_table[q_ind][ind]))
        h_table.append(h)
        
    return q_table, q0_table, h_table
        
             

    
def minimize(h_truth_table):
    minimizer = Minimizer(truth_table=h_truth_table, vars=['v', 'q1*', 'q2*', 'q3*'])
    minimized_list: list = minimizer.karnough_method()
    return minimized_list
    
    
    
if __name__ == '__main__':
    q_table, q0_table, h_table = create_tables()
    print_tables()
    h1, h2, h3 = minimize(create_h_truth_table())
    print('\nminimized h1:', h1)
    print('minimized h2:', h2)
    print('minimized h3:', h3)

