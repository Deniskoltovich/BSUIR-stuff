#include <iostream>
#include <algorithm>
#include <fstream>
#include<string>
#include<vector>
#include <ctime>
using namespace std;
struct Date
{
    int day, month, year;
};
struct Store {
    string Item_name;
    int Number;
    int Cost;
    string date;
};
vector <Store> store_list;
time_t dateToTimeT(int month, int day, int year) {
    tm tmp = tm();

    tmp.tm_mday = day;

    tmp.tm_mon = month - 1;

    tmp.tm_year = year - 1900;

    return mktime(&tmp);
}
void Load() {
    ifstream in;
    in.open("file.txt");
    if (!in.is_open()) {
        cout << "Open Error!" << endl;
    }
    if (in.is_open()) {
        ::store_list.clear();
        while (!in.eof()) {
            Store temp_store;

            in >> temp_store.Item_name;
            in >> temp_store.Number;
            in >> temp_store.Cost;
            in >> temp_store.date;
            ::store_list.push_back(temp_store);
        }
        cout << "Done" << endl;

    }
    in.close();

}
void Print() {
    cout << "Store: " << endl;
    for (int i = 0; i < ::store_list.size(); i++) {
        cout << i + 1 << ")" << ::store_list[i].Item_name << "\t" << "number: " << ::store_list[i].Number << "\tcost : " << ::store_list[i].Cost << "\tdate : " << ::store_list[i].date << endl;
    }
}

void WriteToFile(string path, vector<Store> vec) {
    ofstream out;
    out.open(path);
    for (int i = 0; i < vec.size(); i++) {
        out << vec[i].Item_name << " ";
        out << vec[i].Number << " ";
        out << vec[i].Cost << " ";
        if (i != vec.size() - 1) {
            out << vec[i].date << "\n";
        }
        else
        {
            out << vec[i].date;
        }

    }
    out.close();
    cout << "Done!";
}
void CreateData() {
    int n;
    store_list.clear();
    cout << "How many objects do you want to create?" << endl;
    cin >> n;
    Store temp_store;
    for (int i = 0; i < n; i++) {
        cout << "Enter item's name\n";
        cin >> temp_store.Item_name;
        cout << "Enter number\n";
        cin >> temp_store.Number;
        cout << "Enter cost\n";
        cin >> temp_store.Cost;
        cout << "Enter date\n";
        cin >> temp_store.date;
        store_list.push_back(temp_store);
    }
    cout << "Done!";
    WriteToFile("file.txt", store_list);
}
void Add() {
    Store temp_store;
    cout << "Enter item's name ";
    cin >> temp_store.Item_name;
    cout << endl;
    cout << "Enter number ";
    cin >> temp_store.Number;
    cout << endl;
    cout << "Enter cost ";
    cin >> temp_store.Cost;
    cout << endl;
    cout << "Enter date ";
    cin >> temp_store.date;
    cout << endl;
    store_list.push_back(temp_store);
    cout << "Done!";
    WriteToFile("file.txt", store_list);
}

void LinSearch(string key) {
    int index = -1;
    for (int i = 0; i < store_list.size(); i++)
    {
        if (store_list[i].Item_name == key) {
            index = i;
            break;
        }
    }
    if (index == -1) {
        cout << "Can not find" << endl;
    }
    else
    {
        cout << "Finded! Its data:\n";
        cout << store_list[index].Item_name << "\t" << "number: " << store_list[index].Number << "\tcost : " << store_list[index].Cost << "\tdate : " << store_list[index].date << endl;
    }
}
void Sort(int begin, int end) {
    int left = begin;
    int rights = end;
    string x = store_list[(rights + left) / 2].Item_name;
    do
    {  
        while (store_list[left].Item_name < x) left++;
        while (store_list[rights].Item_name > x) rights--;
        if (left <= rights) {
            Store temp = store_list[rights];
            store_list[rights] = store_list[left];
            store_list[left] = temp;
            rights--;
            left++;
        }

    } while (left <= rights);
    if (begin < rights) Sort(begin, rights);
    if (left < end) Sort(left, end);
}
void BinarySearch(string key) {
    Sort(0, store_list.size() - 1);
    int index = -1;
    int start = 0;
    int end = store_list.size() - 1;
    while (start <= end) {
        int mid = (start + end) / 2;
        if (key == store_list[mid].Item_name) {
            index = mid;
            break;
        }
        if (key < store_list[mid].Item_name) {
            end = mid - 1;
        }
        else {
            start = mid + 1;
        }
    }
    if (index == -1)
    {
        cout << "Can not find\n";
    }
    else {
        cout << "Finded! Its data\n";
        cout << store_list[index].Item_name << "\t number:" << store_list[index].Number << "\t cost:" << store_list[index].Cost << "\t date:" << store_list[index].date << "\n";
    }
}
void Task(Date date) {
    vector<Store> result;
    int day, month, year;
    string sday, smonth, syear;
    for (int i = 0; i < store_list.size(); i++) {
        sday = store_list[i].date[0];
        sday += store_list[i].date[1];
        day = stoi(sday);
        smonth = store_list[i].date[3];
        smonth += store_list[i].date[4];
        month = stoi(smonth);
        syear = store_list[i].date[6];
        syear += store_list[i].date[7];
        syear += store_list[i].date[8];
        syear+= store_list[i].date[9];
        year = stoi(syear);

        time_t date1 = dateToTimeT(month, day, year);

        time_t date2 = dateToTimeT(date.month, date.day, date.year);
        long sec = difftime(date2, date1);

        long days = sec / (60 * 60 * 24);
        if (days > 30 && store_list[i].Cost > 100000) {
            result.push_back(store_list[i]);
        }
        
    }
    WriteToFile("task.txt", result);
}

int menu() {
    int res;
    cout << "=========================" << '\n' << "\nMenu:\n" << '\n';
    cout << 1 << "-" << "Create data" << '\n';
    cout << 2 << "-" << "Print structures\n";
    cout << 3 << "-" << "Write to file" << '\n';
    cout << 4 << "-" << "Add stucture" << '\n';
    cout << 5 << "-" << "load from file" << '\n';
    cout << 6 << "-" << "linear search" << '\n';
    cout << 7 << "-" << "Sort" << '\n';
    cout << 8 << "-" << "Binary search\n";
    cout << 9 << "-" << "Task\n";
    cout << 10 << "-" << "To exit\n" << "=========================" << '\n';
    cin >> res;
    return res;
}

int main() {
    string key;
    string time;
    int time_int;
    Date date;
    while (true)
    {
        switch (menu())
        {
        case 1:
            CreateData();
            break;
        case 2:
            Print();
            break;
        case 3:
            WriteToFile("file.txt", store_list);
            break;
        case 4:
            Add();
            break;
        case 5:
            Load();
            break;
        case 6:
            cout << "Enter key" << endl;
            cin >> key;
            cout << "=========================" << '\n';
            LinSearch(key);
        case 7:

            Sort(0, store_list.size() - 1);
            break;
        case 8:
            cout << "Enter key" << endl;
            cin >> key;
            BinarySearch(key);
            break;
        case 9:
            cin >> date.day >> date.month >> date.year;
            Task(date);
            break;
        default:
            return 0;
        }
    }
    return 0;
}