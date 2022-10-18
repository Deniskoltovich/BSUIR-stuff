#include <iostream>
#include <string>
#include <cctype>
using namespace std;

struct Student {
	string surname;
	string initials;
	string date;
	string group;
	int phys;
	int math;
	int inf;
	int chem;
	double avr;
};


int main()
{
	int n;
	Student arr[100];
	cout << "Enter number of students:" << endl;
	cin >> n;
	for (int i = 0; i < n; i++) {
		cout << "Enter student's surname:" << endl;
		cin >> arr[i].surname;
		cout << "Enter student's initials:" << endl;
		cin >> arr[i].initials;
		cout << "Enter student's date of birth:" << endl;
		cin >> arr[i].date;
		cout << "Enter student's group:" << endl;
		cin >> arr[i].group;
		cout << "Enter student's physics mark:" << endl;
		cin >> arr[i].phys;
		cout << "Enter student's math mark:" << endl;
		cin >> arr[i].math;
		cout << "Enter student's informatics mark:" << endl;
		cin >> arr[i].inf;
		cout << "Enter student's chem mark:" << endl;
		cin >> arr[i].chem;
		arr[i].avr = (arr[i].phys + arr[i].math + arr[i].inf + arr[i].chem) / 4.0;
	}
	
	char symb;
	cout << "Enter any letter:" << endl;
	cin >> symb;
	for (int i = 0; i < n; i++) {
		if (arr[i].surname[0] == toupper(symb) && arr[i].avr >= 9) {
			cout << arr[i].surname << " " << arr[i].initials << " " << arr[i].date << " group " << arr[i].group <<
				"  phys mark: " << arr[i].phys << ", math mark: " << arr[i].math << ", informatics mark: " << arr[i].inf <<
				", chemistry mark: " << arr[i].chem << ", average: " << arr[i].avr;
		}
		cout << endl;
	}
	return 0;
}
