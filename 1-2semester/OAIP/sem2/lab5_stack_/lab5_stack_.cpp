#include <iostream>

using namespace std;
struct Stack {
	int data;
	Stack* next;
};


Stack* NewStack(int value) {
	Stack* stack = new Stack;
	stack->data = value;
	stack->next = NULL;
	return stack;
}
void Push(Stack*& top, int value) {
	Stack* tmp_node = new Stack;
	tmp_node->next = top;
	tmp_node->data = value;
	top = tmp_node;
}
void View(Stack* top)
{
	cout << "your stack: ";
	Stack* temp = top; 
	while (temp != nullptr)
	{
		cout << temp->data << " ";
		temp = temp->next;
	}
	cout << endl;
}
void Pop(Stack*& top) {
	Stack* tmp = top->next;
	delete top;
	top = tmp;

}
void DelStack(Stack*& top) {
	Stack* tmp;
	while (top != NULL)
	{
		tmp = top;
		top = top->next;
		delete tmp;
	}
}
void Task(Stack*& top) {

		Stack* f = new Stack;
		f->next = top;
		top = f;
		Stack* tmp = top;
		Stack* del;
		tmp = top;
		while (tmp->next != NULL)
			if (tmp->next->data % 2 == 0) {
				del = tmp->next;
				tmp->next = del->next;
				delete del;
			}
			else
			{
				tmp = tmp->next;
			}

		top = top->next;
		delete f;
}
void Sort_info(Stack*& top) {
	Stack* t = NULL;
	Stack* t1;
	int r;
	do {
		for (t1 = top; t1->next != t && t1->next != NULL; t1 = t1->next)
			if (t1->data > t1->next->data) {
				r = t1->data;
				t1->data = t1->next->data;
				t1->next->data = r;
			}
		t = t1;
	} while (top->next != t);
}
void Sort_Addres(Stack*& top) {
	Push(top, 0);
	Stack* t = NULL, * t1, * r;
	if (top->next->next == NULL) return;
	do {
		for (t1 = top; t1->next->next != t; t1 = t1->next)
			if (t1->next->data > t1->next->next->data) {
				r = t1->next->next;
				t1->next->next = r->next;
				r->next = t1->next;
				t1->next = r;
			}
		t = t1->next;
	} while (top->next->next != t);
	Pop(top);
}


int menu() {
	int res;
	cout << "=========================" << '\n' << "\nMenu:\n" << '\n';
	cout << 1 << "-" << "Create stack" << '\n';
	cout << 2 << "-" << "Add element\n";
	cout << 3 << "-" << "Delete element" << '\n';
	cout << 4 << "-" << "Print stack" << '\n';
	cout << 5 << "-" << "Delete stack" << '\n';
	cout << 6 << "-" << "Task" << '\n';
	cout << 7 << "-" << "SortInfo" << '\n';
	cout << 8 << "-" << "SortAddres" << '\n';
	cout << 9 << "-" << "To exit\n" << "=========================" << '\n';
	cin >> res;
	return res;
}
int main()
{

	Stack* top;
	int value;
	cout << "Enter the first element: \n";
	cin >> value;
	top = NewStack(value);
	while (true)
	{
		switch (menu())
		{
		case 1:
			cout << "Enter the first element: \n";
			cin >> value;
			top = NewStack(value);
			View(top);
			break;
		case 2:
			cout << "Enter element: \n";
			cin >> value;
			Push(top, value);
			View(top);
			break;
		case 3:
			Pop(top);
			View(top);
			break;
		case 4:
			View(top); break;
		case 5:
			DelStack(top); break;
		case 6:
			Task(top);
			View(top);
			break;
		case 7:
			Sort_info(top);
			View(top);
			break;
		case 8:

			Sort_Addres(top);
			View(top);
			break;
		case 9:
			DelStack(top);
			return 0;
		default:
			break;
		}
	}
	DelStack(top); return 0;

}