from Deque_lib import Deque


string = str
deque = Deque()
print('pf -- pushFront', '\t\trf -- removeFront')
print('pb -- pushBack ', '\t\trb -- removeBack')
while True:
    print('\nEnter your choice')
    string = str(input())
    if string == 'pf':
        print('enter n')
        n = input()
        deque.pushFront(n)
        deque.output()
    elif string == 'pb':
        print('enter n')
        n = input()
        deque.pushBack(n)
        deque.output()
    elif string == 'rf':
        if not deque.isEmpty():
            deque.removeFront()
            deque.output()
        else:
            print('Error! Your deque is empty')
    elif string == 'rb':
        if not deque.isEmpty():
            deque.removeBack()
            deque.output()
        else:
            print('Error! Your deque is empty')
    elif string == 'exit':
        break;
