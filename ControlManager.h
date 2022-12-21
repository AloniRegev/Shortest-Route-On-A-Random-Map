#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <stack>
#include <tuple>
#include "./tinyxml2/tinyxml2.cpp"
#include "./tinyxml2/tinyxml2.h"
#include "Map.h"


using namespace tinyxml2;

class ControlManager{
private:
    std::vector<Map> maps;
    int orientation(Point p, Point q, Point r);
    std::vector<Point> ConvexHull(std::vector<Point> points);   

public:
    std::vector<Map> getMaps(){return this->maps;}
    void readInput(const char * path);
    void createOutput(const char * path);
};
