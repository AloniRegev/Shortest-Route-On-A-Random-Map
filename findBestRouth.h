#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
#include "./tinyxml2/tinyxml2.h"
#include "./tinyxml2/tinyxml2.cpp"
using namespace std;
using namespace tinyxml2;

class Polygon{
    public:
        Polygon(int numOfVertices, vector<tuple<int, int>> const& vec) : numOfVertices(numOfVertices), vetrexes(vec){};

    private:
        const int numOfVertices;
        const vector<tuple<int, int>> vetrexes; 

};

class Map{ 
    private:
        const int weight;
        const int height;
        const tuple<int, int> startPoint;
        const tuple<int, int> targetPoint;
        const vector<Polygon> Polygons;
    
    public:
        Map( int _weight,  int _height,  tuple<int, int> _startPoint,  tuple<int, int> _targetPoint,  vector<Polygon> _Polygons):weight(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), Polygons(_Polygons){};
};
