#include <iostream>
#include <fstream>
#include <stack>
#include <tuple>
#include <math.h>
#include <algorithm>

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
    void creatGraph(Map& map);
};
