#include <iostream>
#include <string>
#include <ctime>
#include <vector>

using namespace std;

struct Tree
{
	Tree* left = NULL;
	Tree* right = NULL;
	string info;
	int key;
};

void Add(Tree*&, int, string);
void DeleteNode(Tree*&);
void DeleteTree(Tree*&);
void ShowTree(Tree*, int = 0);
void Traversal_1(Tree*);
void Traversal_2(Tree*);
void GetNodes(Tree*, vector<Tree*>&);
void BubbleSort(vector<Tree*>&);
Tree* Balance(Tree*&, vector<Tree*>&, int = -1, int = 0);
Tree*& GetNodeByKey(Tree*&, int);
Tree*& GetMaxNode(Tree*&, Tree*** = NULL);
int Select(const string*, int, string = "");
int menu();

int main() {

	system("chcp 1251>nul");
	Tree* root = NULL;
	vector<Tree*> nodes;
	int key;
	Tree* keyNode;
	string name;
	int size;
	int choise;
	int count = 0;
	while (true) {
		switch (menu()) {
		case 1:
			DeleteTree(root);
			cout << "Enter size: " << endl;
			cin >> size;
			cout << "\n";
			for (int i = 0; i < size; i++)
			{
				cout << "Enter  " << i + 1 << " element's key: " << endl;
				cin >> key;
				cout << "Enter " << i + 1 << " element's info: " << endl;
				string name = "";
				cin >> name;
				cout << name << ": " << key << "\n";
				Add(root, key, name);
			}
			break;
		case 2:
			nodes.clear();
			GetNodes(root, nodes);
			count = 0;
			for (auto node : nodes) if (!node->left && !node->right) count++;
			cout << "Число листьев: " << count << "\n";
			nodes.clear();
			break;
		case 3:
			cout << "Введите ключ: " << endl;
			cin >> key;
			while (GetNodeByKey(root, key)) {

				cout << "Введите другой ключ: " << endl;
				cin >> key;
			}
			cout << "Введите имя: ";
			cin >> name;
			Add(root, key, name);
			break;
		case 4:
			cout << "Введите ключ: " << endl;
			cin >> key;
			DeleteNode(GetNodeByKey(root, key));
			break;
		case 5:
			ShowTree(root,0);
			break;
		case 6:
			cout << "Введите ключ: " << endl;
			cin >> key;
			keyNode = GetNodeByKey(root, key);
			if (keyNode)
			{
				cout << "Имя: " << keyNode->info << "\n";
			}
			else
			{
				cout << "Элемент не найден\n";
			}
			break;
		case 7:
			nodes.clear();
			GetNodes(root, nodes);
			BubbleSort(nodes);
			Balance(root, nodes, -1, 0);
			nodes.clear();
			break;
		case 8:
			cout << "Если хотите распечатать прямым обходом, то нажмите 1" << endl;
			cout << "Если хотите распечатать обратным обходом, то нажмите 2" << endl;
			cout << "Если хотите распечатать в порядке возрастания ключа, то нажмите 3" << endl;

			cin >> choise;
			switch (choise)
			{
			case 1:
				Traversal_1(root);
				break;
			case 2:
				Traversal_2(root);
				break;
			case 3:
				nodes.clear();
				GetNodes(root, nodes);
				BubbleSort(nodes);
				for (int i = 0; i < nodes.size(); ++i)
				{
					cout << nodes[i]->info << " ";
				}
				nodes.clear();
				break;
			}
			cout << "\n";
			break;
		case 9:
			return 0;

		default:
			break;
		}
	}
}
Tree* Creation(int inf) {
	Tree* t = new Tree;
	t->info = inf;
	t->left = t->right = NULL;
	return t;
}
void Add(Tree*& root, int key, string info)
{
	Tree** p = &root;
	while (*p)
	{
		if (key < (*p)->key)
		{
			p = &(*p)->left;
		}
		else if (key > (*p)->key)
		{
			p = &(*p)->right;
		}
	}
	Tree* newNode = new Tree;
	newNode->key = key;
	newNode->info = info;
	*p = newNode;
}

void DeleteNode(Tree*& target)
{
	if (!target) return;
	Tree* tempPtr = NULL;
	if ((target->left && !target->right) || (!target->left && target->right))
	{
		if (target->left)
		{
			tempPtr = target->left;
		}
		else
		{
			tempPtr = target->right;
		}

	}
	else if (target->left && target->right)
	{
		Tree** prevPtr = NULL;
		tempPtr = GetMaxNode(target->left, &prevPtr);
		if (!prevPtr)
		{
			tempPtr->right = target->right;
		}
		else
		{
			if (tempPtr->left)
			{
				(*prevPtr)->right = tempPtr->left;
			}
			else (*prevPtr)->right = NULL;
			tempPtr->right = target->right;
			tempPtr->left = target->left;
		}
	}
	else
	{
		target = NULL;
	}
	delete target;
	target = tempPtr;
}

void DeleteTree(Tree*& root){
	while (root) DeleteNode(root);
}

void ShowTree(Tree* p, int level){
	string str;
	if (!p)
	{
		return;
	}
	ShowTree(p->right, level + 1);
	for (int i = 0; i < level; i++) 
		str = str + "   ";
	cout << str << p->info << "\n";
	ShowTree(p->left, level + 1);
}
void Traversal_1(Tree* p)
{
	if (!p) return;
	cout << p->info << " ";
	Traversal_1(p->left);
	Traversal_1(p->right);
}

void Traversal_2(Tree* p)
{
	if (!p) return;
	Traversal_2(p->left);
	Traversal_2(p->right);
	cout << p->info << " ";
}

void GetNodes(Tree* p, vector<Tree*>& nodes)
{
	if (!p) return;
	nodes.push_back(p);
	GetNodes(p->left, nodes);
	GetNodes(p->right, nodes);

}

void BubbleSort(vector<Tree*>& nodes)
{
	int n = nodes.size();
	for (int i = 0; i < n - 1; i++)
	{
		for (int j = i + 1; j < n; j++)
		{
			if (nodes[i]->key > nodes[j]->key)
			{
				Tree* temp = nodes[i];
				nodes[i] = nodes[j];
				nodes[j] = temp;
			}
		}
	}
}

Tree* Balance(Tree*& root, vector<Tree*>& nodes, int k, int n)
{
	if (k == -1) k = nodes.size(), root = nodes[k / 2];
	if (n == k) return NULL;
	int m = (n + k) / 2;
	nodes[m]->left = Balance(root, nodes, m, n);
	nodes[m]->right = Balance(root, nodes, k, m + 1);
	return nodes[m];
}

Tree*& GetNodeByKey(Tree*& root, int key)
{
	Tree** p = &root;
	while (*p)
	{
		if ((*p)->key > key) p = &(*p)->left;
		else if ((*p)->key < key) p = &(*p)->right;
		else return *p;
	}
	return *p;
}

Tree*& GetMaxNode(Tree*& root, Tree*** prev)
{
	Tree** p = &root;
	while ((*p)->right)
	{
		if (prev)
			*prev = p;
		p = &(*p)->right;
	}
	return *p;
}


int menu() {
	int res;
	cout << "=========================" << '\n' << "\nMenu:\n" << '\n';
	cout << 1 << "-" << "Create tree" << '\n';
	cout << 2 << "-" << "Task\n";
	cout << 3 << "-" << "Add node" << '\n';
	cout << 4 << "-" << "Delete node by key" << '\n';
	cout << 5 << "-" << "View" << '\n';
	cout << 6 << "-" << "Search" << '\n';
	cout << 7 << "-" << "Balance" << '\n';
	cout << 8 << "-" << "Print\n";
	cout << 9 << "-" << "To exit\n" << "=========================" << '\n';
	cin >> res;
	return res;
}

