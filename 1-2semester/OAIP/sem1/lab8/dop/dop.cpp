#include <string>
#include <iostream>
#include <cstdlib>
using namespace std;
int main()
{
	int i;
	int min1 = 0, max1 = 0, g;

	string s1, s2, h,result;
	cout << "enter the first string" << endl;
	getline(cin, s1);
	s1 += " ";


	cout << "enter the second string" << endl;
	getline(cin, s2);
	s2.insert(0, " ");
	s2 += " ";
	


	for (i = 0; i < size(s1) ; i++)
	{
		if (s1[i] == ' ') {
			max1 = i - min1;
			h = s1.substr(min1, max1);
			min1 = i + 1;
			g = s2.find(" "+h+" ");

			
			///if ((g != -1) && (s2[g -1] == ' ') && (s2[g + max1] == ' '))
			if (g != -1)
			
				result += "*** ";
			
			else 
				result += h + " ";
		}
	}
	cout<< result;



	return 0;
}


