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
    std::vector<Map> maps;
    std::unordered_map<std::string, std::vector<Point>> lineOfSightTable;
public:

    /// output and input xml files. ///
    void readXML(const char * path); //Read and create map element from given xml file path.
    void writeXML(const char * path); //A function that creates a new xml file for the received map object.

    /// ConvexHull ///
    std::vector<Point> ConvexHull(std::vector<Point> points); //A function that creates a convex polygon from a general polygon it receives.

    /// line of sight ///
    std::vector<Point> lineOfSight (Map &map, Point &startPoint); // A function that finds for the current point all the other points that are in its line of sight.
    void findFullGraph(); //Creating a full graph for the map, for visualizing the arcs in the graph

    /// The easiest route ///
    std::vector<Point> aStar(Point& start, Point target, Map& map); //A function to implement an A* algorithm that finds the easiest route between a start point and a target point.
    void findRoute(); //Initializes the easiest route in the internal map object.
};


