#include <iostream>
#include <fstream>
#include <stack>
#include <tuple>
#include <math.h>

#include "Map.h"

class ControlManager{
private:
    std::vector<Map> maps;
    

public:
    /*getters and setters*/
    std::vector<Map>& getMaps(){return this->maps;}
    
    /*output and input xml files.*/
    void readXML(const char * path);
    void writeXML(const char * path);

    /*ConvexHull*/
    std::vector<Point> ConvexHull(std::vector<Point> points);
    
    /* line of sight*/
    std::vector<Point> lineOfSight (Map &map, Point &startPoint);
    void creatGraph(Map& map);
};
