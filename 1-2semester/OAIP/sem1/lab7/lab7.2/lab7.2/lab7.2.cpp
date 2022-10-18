#include<iostream>
#include<string>
using namespace std;
int main() {
	int f = 1, len, i, min, index = 0, n;
	string str;
	string S = " ";
	cin >> str;
	min = size(str);
	cout << endl;
	str += S;
		for (i = 0; i < size(str) - 1; i++) {
			if (str[i] == str[i + 1])
				f++;
			else {
				if (f < min) {
					min = f;
					index = i + 1 - f;
					f = 1;
				}
				else f = 1;

			}
		}
	cout << endl;

	cout << "the smallest group:";
	for (i = index; i < index + min; i++)
		cout <<str[i];
	return 0;
}