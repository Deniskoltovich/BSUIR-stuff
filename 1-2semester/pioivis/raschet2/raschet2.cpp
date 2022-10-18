#include<fstream>
#include <iostream>
using namespace std;



bool dfs(int i, int** matr, bool* used, int size) {
    if (used[i]) {          
        return false;
    }
    used[i] = true; 
    for (int j = 0; j < size; ++j) {
        if (matr[i][j]) { 
            dfs(j, matr, used, size); 
        }
    }
}

bool IsTree(int** matr, int k, int size) { 
    int edges = 0;
    for (int i = 0; i < size; ++i) {
        for (int j = i + 1; j < size; ++j) {
            if (matr[i][j]) {
                edges++;
            }
        }
    }
    if (edges != size - 1 - k) {
        return false;
    }
    return true;
}
bool isConnected(int** copy, int* toDel, int size, bool* used) { 
    memset(used, 0, size);
    for (int i = 0; i < size; i++) 
    {
        if (!toDel[i]) {
            dfs(i, copy, used, size);
            break;
        }
    }
    for (int i = 0; i < size; i++) 
    {
        if ((!toDel[i]) && (!used[i])) {
            return false;
        }
    }
    return true;
}


int main()
{
    
    int numOfElem = 0 , vertexToDel = 0, k = 0, vertexCounter = 0; 
    int h = 0;
    int maxvertex = 0;
    string path = "Matrix.txt";
    ifstream fin;
    fin.open(path);
    string elements;
    while (!fin.eof()) {
        fin >> elements;
        numOfElem++; 
    } 
   

   int size = sqrt(numOfElem);
    
   int** matr = new int* [size];
        for (int i = 0; i < size; i++)
            matr[i] = new int[size];
    
    int** copy = new int* [size];
        for (int i = 0; i < size; i++)
            copy[i] = new int[size];
    
    int* vertex = new int[size];
    
    int* vertexesToDel = new int[size];
    
    bool* used = new bool[size];
    
    for (int i = 0; i < size; i++) {
            vertex[i] = 1;
            vertexesToDel[i] = 0;
            used[i] = 0;
    }
    

        
    ifstream fin1;
    fin1.open(path);
    for (int i = 0; i < sqrt(numOfElem-1); i++) {
        for (int j = 0; j < sqrt(numOfElem -1); j++) {
            fin1 >> matr[i][j];
           
            cout << matr[i][j]<<" ";
     
       }
        cout << endl;
    }
   
    for (int i = 0; i < sqrt(numOfElem - 1); i++) {
        for (int j = 0; j < sqrt(numOfElem - 1); j++) {
            copy[i][j] = matr[i][j];

        }
        cout << endl;
    }
    
   fin1.close();
   if(isConnected(matr, vertexesToDel, size, used) && IsTree(matr,0, size)) {
       cout << "Number of deleted vertexes - " << vertexCounter << endl;
       cout << "Vertexes: ";
       for (int i = 0; i < size; i++)
           cout << vertexesToDel[i] << ' ';
       exit(0);
   }
     
    while (k != 1) {
        maxvertex = 0;
        h = 0;
        for (int i = 0; i < size; i++) {
            if (vertex[i] == 1) {
                for (int j = 0; j < size; j++) {
                    if (matr[i][j] == 1)
                        h++;
                }
                if (h > maxvertex) {
                    maxvertex = h;
                    vertexToDel = i;  
                }
                h = 0;
            }
        }
        for (int i = 0; i < size; i++) { 
            copy[vertexToDel][i] = 0;
            copy[i][vertexToDel] = 0;
        }
       
        vertexesToDel[vertexToDel] = 1;
        
        if (!isConnected(copy, vertexesToDel, size, used)) {
            for (int i = 0; i < size; i++) {
                copy[vertexToDel][i] = matr[vertexToDel][i];
                copy[i][vertexToDel] = matr[i][vertexToDel];
            }
            vertex[vertexToDel] = 0;
            vertexesToDel[vertexToDel] = 0; 
        }
        else {
            for (int i = 0; i < size; i++) {
                matr[vertexToDel][i] = copy[vertexToDel][i];
                matr[i][vertexToDel] = copy[i][vertexToDel];
            }
            vertex[vertexToDel] = 0; 
            vertexCounter++; 
            if (IsTree(matr, vertexCounter, size)) 
                k = 1;
        }
    }


    cout << "Number of deleted vertexes - " <<vertexCounter << endl;
    cout << "Vertexes: ";
    for (int i = 0; i < size; i++)
        cout << vertexesToDel[i] << ' ';
   
    delete[] matr;
    delete[] copy; 
    delete[] vertex;
    delete[] vertexesToDel;
     fin.close();
}