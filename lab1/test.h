#include<iostream>
#include<vector>
#include<string>
#include"lab1.h"

using namespace std;

class Test {
private:
    string word;
    string alphabet;
    int index;
	string a;
    string left_part = "", right_part = "";
    vector<std::pair<std::string, std::string>> rules;
    string line;
public:
    int testmain() {
		Tape tape;
		//tape.Read("file.txt");
		tape >> "file.txt";
		word = tape.getWord();
		Interpretator inter(word);
		tape.Write();
		while (true) {
			switch (menu())
			{
			case 1:
				inter.execute(tape.getRules());
				word = inter.getWord();
				tape.setWord(word);
				tape.Write();
				break;
			case 2:
				tape.Write();
				inter.changeLog();
				inter.execute(tape.getRules());
				inter.changeLog();
				word = inter.getWord();
				tape.setWord(word);
				break;
			case 3:
				cout << "Enter left part of rule\n";
				cin >> left_part;
				cout << "Enter right part of rule\n";
				cin >> right_part;
				tape.addRule(left_part, right_part);
				tape.Write();
				break;
			case 4:
				cout << "Enter new word\n";
				word.clear();
				cin >> word;
				tape.setWord(word);
				word = tape.getWord();
				inter.setWord(word);
				tape.Write();
				break;
			case 5:
				cout << "Enter the index of the rule\n";
				cin >> index;
				
				tape.changeRule(index, left_part, right_part);
				break;
			case 6:
				cout << "Enter the index of the rule\n";
				cin >> index;
				tape.delete_rule(index);
				break;
			case 7:
				tape.deleteRules();
				cout << "\n_________________________\nEnter the num of rules:\n_________________________\n";
				int n;
				cin >> n;
				rules.clear();
				for (int i = 0; i < n; ++i) {
					cout << "\nEnter " << i + 1 << " rule:\n_________________________\n";
					cout << "Enter left part of rule\n";
					cin >> left_part;
					cout << "Enter right part of rule\n";
					cin >> right_part;
					rules.push_back({ left_part,right_part });
				}
				tape.setRules(rules);
				break;
			case 8:
				cout << "Enter new alphabet:\n";
				cin >> alphabet;
				tape.setAlphabet(alphabet);
				break;
			case 9:
				tape.Write();
				break;
			default:
				return 0;
			}
		}
    }

    int menu() {
        int res;
        cout << "=========================" << '\n' << "\nMenu:\n" << '\n';
        cout << 1 << "-" << "Execute algorithm" << '\n';
        cout << 2 << "-" << "Execute algorithm with '-log' argument\n";
        cout << 3 << "-" << "Add rule" << '\n';
        cout << 4 << "-" << "Change word" << '\n';
        cout << 5 << "-" << "Change rule" << '\n';
        cout << 6 << "-" << "Delete rule" << '\n';
        cout << 7 << "-" << "New rules" << '\n';
		cout << 8 << "-" << "Change alphabet" << '\n';
		cout << 9 << "-" << "Show tape" << '\n';
        cout << 0 << "-" << "To exit\n" << "=========================" << '\n';
        cin >> res;
        return res;
    }
};
