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
public:    
    /// output and input xml files. ///
    void readXML(const char * path, std::vector<Map> &maps); //Read and create map element from given xml file path.
    void writeXML(const char * path, std::vector<Map>& maps); //A function that creates a new xml file for the received map object.

    /// ConvexHull ///
    std::vector<Point> ConvexHull(std::vector<Point> points); //A function that creates a convex polygon from a general polygon it receives.

    /// line of sight ///
    std::vector<Point> lineOfSight (Map &map, Point &startPoint); // A function that finds for the current point all the other points that are in its line of sight.

    /// The easiest route ///
    std::vector<Point> aStar(Point& start, Point target, Map& map); //A function to implement an A* algorithm that finds the easiest route between a start point and a target point.

};


