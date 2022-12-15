#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
#include "./tinyxml2/tinyxml2.h"
#include "./tinyxml2/tinyxml2.cpp"
using namespace std;
using namespace tinyxml2;

class Polygon{
    private:
        const int numOfVertices;
        const vector<tuple<int, int>> vetrexes; //todo replace withe point class object
        const vector<tuple<tuple<int, int>,tuple<int, int>>> edges;//todo replace withe point class object

    public:
        Polygon(int numOfVertices, vector< tuple<int, int>>& vec) : numOfVertices(numOfVertices), vetrexes(vec) /*, edges(convexHull(vec))*/{};

        vector<tuple<int, int>> getVerexes()const{return this->vetrexes;} //todo replace withe point class object
        // vector<tuple<tuple<int, int>,tuple<int, int>>> convexHull(const vector<tuple<int, int>> vec) const; //todo implement
};

class Map{ 
    private:
        const int weight;
        const int height;
        const tuple<int, int> startPoint; //todo replace withe point class object
        const tuple<int, int> targetPoint; //todo replace withe point class object
        const vector<Polygon> polygons;
    
    public:
        Map( int _weight,  int _height,  tuple<int, int> _startPoint,  tuple<int, int> _targetPoint,  vector<Polygon>& _polygons)
            :weight(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), polygons(_polygons){};

        int getWeight()const{return this->weight;}
        int getHeight()const{return this->height;}
        tuple<int, int> getStartPoint()const{return this->startPoint;}
        tuple<int, int> getTargetPoint()const{return this->targetPoint;}
        vector<Polygon>  getPolygons()const{return this->polygons;}
};
