#include <iostream>
#include <fstream>
#include <stack>
#include <tuple>
#include <math.h>
#include <algorithm>
#include <queue>
#include <unordered_map>

#include "Map.h"

class ControlManager{
private:
    //std::vector<Map> maps;
    

public:
    /*getters and setters*/
    //std::vector<Map>& getMaps(){return this->maps;}
    
    /*output and input xml files.*/
    void readXML(const char * path, std::vector<Map> &maps);
    void writeXML(const char * path, std::vector<Map>& maps);

    /*ConvexHull*/
    std::vector<Point> ConvexHull(std::vector<Point> points);
    //void ConvexHullMaps(std::vector<Map>&maps);

    /* line of sight*/
    std::vector<Point> lineOfSight (Map &map, Point &startPoint);
    //void creatGraph(Map& map);

    /*find the best routh from start point to target point*/
    std::vector<Point> aStar(Point& start, Point target, Map& map);

};


