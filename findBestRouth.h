#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <tuple>
#include "./tinyxml2/tinyxml2.h"
#include "./tinyxml2/tinyxml2.cpp"
using namespace std;
using namespace tinyxml2;

class Point{
    private:
        const int x;
        const int y;

    public:
        Point(int x, int y) : x(x), y(y) {};

         int getX()const{return this->x;}
         int getY()const{return this->y;}
         string toString(){return "("+to_string(getX())+", "+to_string(getY())+")";}

};

class Polygon{
    private:
        const int numOfVertices;
        const vector<Point> vertexes;
        const vector<tuple<Point,Point>> edges;

    public:
        Polygon(int numOfVertices, vector< Point>& vec) : numOfVertices(numOfVertices), vertexes(vec) /*, edges(convexHull(vec))*/{};

        vector<Point> getVertexes()const{return this->vertexes;}
        // vector<tuple<tuple<int, int>,tuple<int, int>>> convexHull(const vector<tuple<int, int>> vec) const; //todo implement
};

class Map{ 
    private:
        const int weight;
        const int height;
        const Point startPoint;
        const Point targetPoint;
        const vector<Polygon> polygons;
    
    public:
        Map( int _weight,  int _height,  Point _startPoint,  Point _targetPoint,  vector<Polygon>& _polygons)
            :weight(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), polygons(_polygons){};

        int getWeight()const{return this->weight;}
        int getHeight()const{return this->height;}
        Point getStartPoint()const{return this->startPoint;}
        Point getTargetPoint()const{return this->targetPoint;}
        vector<Polygon>  getPolygons()const{return this->polygons;}
};

