#include <malloc.h>
#include <iostream>
using namespace std;
int main()
{
    int cols, str, h = 1;
    cout << "Enter number of strings" << endl;
    cin >> str;
    cout << "Enter number of colomns" << endl;
    cin >> cols;
    cout << endl;
    int* vecB = new int[str];
    int** matr = new int* [str];
        for (int i = 0; i < str; i++)
            matr[i] = new int[cols];

        for (int i = 0; i < str; i++) {
            for (int j = 0; j < cols; j++) 
            cin >> matr[i][j];
        }

        cout << "vecB = {";
        for (int i = 0; i < str; i++) 
        {
            for (int j = 0; j < cols-1; j++) {
            
                if (matr[i][j] > matr[i][j + 1])
                    h++;
                
            }
            if (h == cols) {
                vecB[i] = 1;
            }
            else {
                vecB[i] = 0;
            }
            h = 1;
            cout << vecB[i]<<", ";
        }

        cout << "}";

    delete[]matr;
    delete[]vecB;
   return 0;
}