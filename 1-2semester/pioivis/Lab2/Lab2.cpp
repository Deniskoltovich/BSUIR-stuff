#include <iostream>
#include <vector>
#include <climits>
#include <set>
#include <fstream>

using namespace std;


vector<long long> Dijkstra(vector<vector<pair<int, int>>>& graph, int& n) {
    
    long long infinity = 40000001;
    vector<long long> distances(n, infinity);
    int start = 0;
    distances[start] = 0;
    set<pair<long long, int>> queue;
    queue.insert({ 0, start });
    while (!queue.empty()) {
        auto top = queue.begin();
        int u = top->second;
        queue.erase(top);

        for (auto next : graph[u]) {
            int v = next.first;
            int length = next.second;
            if (distances[v] > distances[u] + length) {
                if (queue.find({ distances[v], v }) != queue.end())
                    queue.erase(queue.find({ distances[v], v }));
                distances[v] = distances[u] + length;
                queue.insert({ distances[v], v });
            }
        }
    }

    return distances;
}

int main() {
    int n, m;
    vector<vector<pair<int, int>>> graph;
    string path_in = "path.in";
    ifstream fin;
    fin.open(path_in);
   
    fin >> n >> m;
    graph.resize(n);

    for (int i = 0; i < m; ++i) {
        int u, v, w;
        fin >> u >> v >> w;
        graph[u - 1].push_back({ v - 1, w });
        graph[v - 1].push_back({ u - 1, w });`
    }
    fin.close();
    vector<long long> result = Dijkstra(graph, n);
    ofstream fout;
    string path_out = "path.out";
    fout.open(path_out);
    
    for (int i = 0; i < result.size(); ++i) {
        fout << result[i] << " ";
    }
    fout.close();
    return 0;
}





