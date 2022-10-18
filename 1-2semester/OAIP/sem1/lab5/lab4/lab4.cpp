#include <iostream>
#include <math.h>
#include <cstdlib>

using namespace std;
int main()
{
    int a[10], k=0, n, i, f = 0, s=0,res = 0;
    do {
        cout << "Enter number of elements(<=10)" << endl;
        cin >> n;
    } while (n > 10);
        cout << "for random press 0, for standart input press 1" << endl;
        cin >> f;
        if (f == 0) {
            srand(time(0));
            for (i = 0; i < n; i++) {

                a[i] = rand() % 4;
                cout << a[i] << " ";
                if ((a[i] == 0) && (f == 0)) {
                    s = k = i; f = 1;
                }
                if ((a[i] == 0) && (f == 1)) {
                    k = i;
                }
            }
        }
        else {
            f = 0; for (i = 0; i < n; i++) {
                cout << "a[" << i + 1 << "]= ";
                cin >> a[i];
                if ((a[i] == 0) && (f == 0)) {
                    s = k = i; f = 1;
                }
                if ((a[i] == 0) && (f == 1)) {
                    k = i;
                }
            }
        }
        if ((s == k) || (k-s == 1))
            cout << "Sum does not exist";
        else {
            for (i = s; i < k; i++)
                res += a[i];
            cout << "Sum = " << res;
        }
    
    return 0;
}

