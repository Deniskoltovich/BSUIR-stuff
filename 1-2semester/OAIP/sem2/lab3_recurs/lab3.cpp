

#include <iostream>
using namespace std;

int Fb_recurs(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    else return Fb_recurs(n - 1) + Fb_recurs(n - 2);
}
int Fb(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    int a = 0;
    int b = 1;
    int res = 0;
    for (int i = 2; i <= n; i++) {
        res = a + b;
        a = b;
        b = res;
    }
    return res;

}
int main()
{
    
    while (true) {
        int c;
        int n;
        cout << "Enter n:" << endl;
        cin>>n;
        cout << "Enter 0 for recursion; 1 - normal" << endl;
        cin >> c;
  
        switch (c)
        {
        case 0: 
            cout << "recursion: Fb(n) = " << Fb_recurs(n) << endl;
        break;
        case 1: 
            cout << "Fb(n) = " << Fb(n) << endl;
        break;
        default:
            cout << "wrong input" << endl;
            return false;
        }
    }
    return 0;
}
