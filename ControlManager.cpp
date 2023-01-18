#include "controlManager.h"
#include "./tinyxml2/tinyxml2.h"


///output and input xml files.///


/*
 *  Read and create map element from given xml file path.
 *
 * @param path - Address from which the xml file is read.
 * @param maps - A map object to which the value is saved.
 */
void ControlManager::readXML(const char* path) {
    tinyxml2::XMLDocument doc;
    doc.LoadFile(path);
    tinyxml2::XMLElement* pRootElement = doc.RootElement();

    if (pRootElement != NULL) {
        tinyxml2::XMLElement* pMap = pRootElement->FirstChildElement("Maps")->FirstChildElement("Map"); // pointer to the first map object data.
        while (pMap != NULL) {
            /* get map object attributes */
            int width = atoi(pMap->FirstChildElement("Width")->GetText());
            int height = atoi(pMap->FirstChildElement("Height")->GetText());
            Point startPoint = Point(atoi(pMap->FirstChildElement("StartPoint")->FirstChildElement("X")->GetText()), atoi(pMap->FirstChildElement("StartPoint")->FirstChildElement("Y")->GetText()));
            Point targetPoint = Point(atoi(pMap->FirstChildElement("TargetPoint")->FirstChildElement("X")->GetText()), atoi(pMap->FirstChildElement("TargetPoint")->FirstChildElement("Y")->GetText()));

            std::vector<Obstacle> obstacles; //TODO remove

            tinyxml2::XMLElement* pPolygon = pMap->FirstChildElement("Polygons")->FirstChildElement("Polygon"); // pointer to the first polygon object data.
            while (pPolygon != NULL) {
                /* get polygon object attributes */
                std::vector<Point> vertexes;

                tinyxml2::XMLElement* pVertex = pPolygon->FirstChildElement("Vertexes")->FirstChildElement("Vertex"); // pointer to the first vertex data.
                while (pVertex != NULL) {
                    Point vertex(atoi(pVertex->FirstChildElement("X")->GetText()), atoi(pVertex->FirstChildElement("Y")->GetText()));
                    vertexes.push_back(vertex); // add new vertex to vertex List.

                    pVertex = pVertex->NextSiblingElement("Vertex"); // move pointer to the next vertex data.
                }
                Polygon polygon(vertexes.size(), vertexes); // create new polygon object.
                Obstacle obstacle(polygon, ConvexHull(vertexes)); // add new obstacle to obstacles List. TODO remove
                obstacles.push_back(obstacle);

                pPolygon = pPolygon->NextSiblingElement("Polygon"); // move pointer to the next polygon object data.
            }
            Map map(width, height, startPoint, targetPoint, obstacles); // create new map object.
            maps.push_back(map); // add new map object to mapList. 

            pMap = pMap->NextSiblingElement("Map"); // move pointer to the next polygon object data.
        }
    }
}

/*
 *  A helper function to add all the attributes of a point object to an xml file.
 *
 * @param doc - xml file to write to.
 * @param root - xml node to which a new point object is associated.
 * @param point - A point we want to add.
 */
void addPointToXML(tinyxml2::XMLDocument& doc, tinyxml2::XMLElement* &root, Point point) {
    tinyxml2::XMLElement* pX = doc.NewElement("X");
    pX->SetText(point.getX());
    root->InsertEndChild(pX);
    tinyxml2::XMLElement* pY = doc.NewElement("Y");
    pY->SetText(point.getY());
    root->InsertEndChild(pY);
}


/*
 *  A helper function adds the line of sight list of a point to the xml file.
 *
 * @param doc - xml file to write to.
 * @param root - xml node to which a new point object is associated.
 * @param point - A point we want to add the line of sight of.
 */
void addLosToXML(tinyxml2::XMLDocument& doc, tinyxml2::XMLElement*& root, std::vector<Point> points) {
    tinyxml2::XMLElement* plos = doc.NewElement("LineOfSight");
    plos->SetAttribute("size", (int)points.size());
    int namePath = 0;
    for (Point& path : points) {
        tinyxml2::XMLElement* pPath = doc.NewElement("Vertex");
        pPath->SetAttribute("name", namePath++);

        addPointToXML(doc, pPath, path);

        plos->InsertEndChild(pPath);
    }
    root->InsertEndChild(plos);
}

/*
 *  A function that creates a new xml file for the received map object.
 * 
 * @param path - Address from which we whant to save our new xml file.
 * @param maps - A map object to which the values are written.
 */
void ControlManager::writeXML(const char* path) {
    tinyxml2::XMLDocument doc;
    tinyxml2::XMLElement* pRoot = doc.NewElement("Root");
    doc.InsertFirstChild(pRoot);
    tinyxml2::XMLElement* pMaps = doc.NewElement("Maps");
    pMaps->SetAttribute("size", maps.size());


    int mapName = 0;
    for (Map& map : maps) {
        tinyxml2::XMLElement* pMap = doc.NewElement("Map");
        pMap->SetAttribute("name", mapName++);

        //insert width value
        tinyxml2::XMLElement* pWidth = doc.NewElement("Width");
        pWidth->SetText(map.getWidth());
        pMap->InsertEndChild(pWidth);

        //insert height value
        tinyxml2::XMLElement* pHeight = doc.NewElement("Height");
        pHeight->SetText(map.getHeight());
        pMap->InsertEndChild(pHeight);

        //insert start point
        tinyxml2::XMLElement* pStartPoint = doc.NewElement("StartPoint");
        addPointToXML(doc, pStartPoint, map.getStartPoint());
        if (lineOfSightTable.find(map.getStartPoint().toString()) != lineOfSightTable.end()) {
            addLosToXML(doc, pStartPoint, lineOfSightTable[map.getStartPoint().toString()]);
        }
        pMap->InsertEndChild(pStartPoint);

        //insert target point
        tinyxml2::XMLElement* pTargetPoint = doc.NewElement("TargetPoint");
        addPointToXML(doc, pTargetPoint, map.getTargetPoint());
        pMap->InsertEndChild(pTargetPoint);

        //insert obstacles;
        tinyxml2::XMLElement* pObstacles = doc.NewElement("Obstacles");
        pObstacles->SetAttribute("size", (int)map.getObstacles().size());
        int nameObstacle = 0;
        for (Obstacle obstacle: map.getObstacles()){
            tinyxml2::XMLElement* pObstacle = doc.NewElement("Obstacle");
            pObstacle->SetAttribute("name", nameObstacle++);

            tinyxml2::XMLElement* pVertexes = doc.NewElement("Vertexes");
            pVertexes->SetAttribute("size", (int)obstacle.getConvexVertexes().size());

            int nameConvex = 0;
            for (Point convex : obstacle.getConvexVertexes()) {
                tinyxml2::XMLElement* pVertex = doc.NewElement("Vertex");
                pVertex->SetAttribute("name", nameConvex++);

                addPointToXML(doc, pVertex, convex);
                if (lineOfSightTable.find(convex.toString()) != lineOfSightTable.end()) {
                    addLosToXML(doc, pVertex, lineOfSightTable[convex.toString()]);
                }

                pVertexes->InsertEndChild(pVertex);
            }
            pObstacle->InsertEndChild(pVertexes);
            pObstacles->InsertEndChild(pObstacle);
        }
        pMap->InsertEndChild(pObstacles);
        
        //insert Route;
        tinyxml2::XMLElement* pRoute = doc.NewElement("Route");
        pRoute->SetAttribute("size", (int)map.getRoute().size());
        int nameRoute = 0;
        for (Point &routeVer : map.getRoute()) {
            tinyxml2::XMLElement* pNode = doc.NewElement("Vertex");
            pNode->SetAttribute("name", nameRoute++);

            addPointToXML(doc, pNode, routeVer);

            pRoute->InsertEndChild(pNode);
        }
        pMap->InsertEndChild(pRoute);

        //insert Map;
        pMaps->InsertEndChild(pMap);
    }
    pRoot->InsertEndChild(pMaps);

    doc.SaveFile(path);
}

/// Utilitis ///

/*
 *  A utility function function to find orientation of ordered triplet (p, q, r).
 *
 * @param p - point object.
 * @param q - point object.
 * @param r - point object.
 * 
 * @return The function returns intager with following values:
 * 0 --> p, q and r are collinear
 * 1 --> Clockwise
 * 2 --> Counterclockwise
 */
int orientation(Point p, Point q, Point r)
{
    int val = (q.getY() - p.getY()) * (r.getX() - q.getX()) -
        (q.getX() - p.getX()) * (r.getY() - q.getY());

    if (val == 0) return 0;  // collinear
    return (val > 0) ? 1 : 2; // clock or counterclockwise wise
}

/*
 * A utility function to calculates euclidean distance of 2 points.
 *
 * @param p1 - point object.
 * @param p2 - point object.
 *
 * @return The function returns floating point number of the euclidean distance of the 2 points.
 */
float euclideanDistance(Point p1, Point p2)
{
    // Calculating distance
    return sqrt(pow(p2.getX() - p1.getX(), 2) + pow(p2.getY() - p1.getY(), 2) * 1.0);
}

/*
 * A utility function that given three collinear points p, q, r, the function checks if point q lies on line segment 'pr'
 *
 * @param p - point object.
 * @param q - point object.
 * @param r - point object.
 *
 * @return true if they are on the same line otherwise it will return false.
 */
bool onSegment(Point p, Point q, Point r)
{
    if (q.getX() <= std::max(p.getX(), r.getX()) && q.getX() >= std::min(p.getX(), r.getX()) &&
        q.getY() <= std::max(p.getY(), r.getY()) && q.getY() >= std::min(p.getY(), r.getY()))
        return true;

    return false;
}

/*
 * A utility function that checks if 2 given straight lines intersect.
 *
 * @param p1 - Point one thet describing straight line 1.
 * @param q1 - Point two thet describing straight line 1.
 * @param p2 - Point one thet describing straight line 2.
 * @param q2 - Point two thet describing straight line 2.
 *
 * @return true if they are intersect otherwise it will return false.
 */
bool doIntersect(Point p1, Point q1, Point p2, Point q2)
{
    // Find the four orientations needed for general and
    // special cases
    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);

    // General case
    if (o1 != o2 && o3 != o4)
        return true;

    // Special Cases
    // p1, q1 and p2 are collinear and p2 lies on segment p1q1
    if (o1 == 0 && onSegment(p1, p2, q1)) return true;

    // p1, q1 and q2 are collinear and q2 lies on segment p1q1
    if (o2 == 0 && onSegment(p1, q2, q1)) return true;

    // p2, q2 and p1 are collinear and p1 lies on segment p2q2
    if (o3 == 0 && onSegment(p2, p1, q2)) return true;

    // p2, q2 and q1 are collinear and q1 lies on segment p2q2
    if (o4 == 0 && onSegment(p2, q1, q2)) return true;

    return false; // Doesn't fall in any of the above cases
}

/// ConvexHull ///

// Big credit for Geeks-for-Geeks for there algorithm implementation.
/*
 * A function that creates a convex polygon from a general polygon it receives.
 *
 * @param points - A vector of points describing a polygon.
 *
 * @return A vector of points describing the convex polygon if unsuccessful will return an empty vector of points.
 */
std::vector<Point> ControlManager::ConvexHull(std::vector<Point> points) {
    // There must be at least 3 points
    int n = points.size();
    // Initialize Result
    std::vector<Point> hull;
    if (n < 3) return hull;


    // Find the leftmost point
    int l = 0;
    for (int i = 1; i < n; i++)
        if (points[i].getX() < points[l].getX())
            l = i;

    // Start from leftmost point, keep moving counterclockwise
    // until reach the start point again.  This loop runs O(h)
    // times where h is number of points in result or output.
    int p = l, q;
    double epsilon = 0.05;
    do
    {
        // Add current point to result
        hull.push_back(points[p]);

        // Search for a point 'q' such that orientation(p, q, x) is counterclockwise for all points 'x'. The idea
        // is to keep track of last visited most counterclockwise-
        // wise point in q. If any point 'i' is more counterclockwise-
        // wise than q, then update q.
        q = (p + 1) % n;
        for (int i = 0; i < n; i++)
        {
            // If i is more counterclockwise than current q, then update q
            if (orientation(points[p], points[i], points[q]) == 2 && abs(euclideanDistance(points[p], points[i]) - abs(euclideanDistance(points[p], points[q]) + euclideanDistance(points[q], points[i]))) > epsilon) { //todo fix
                q = i;
            }

        }

        // Now q is the most counterclockwise with respect to p
        // Set p as q for next iteration, so that q is added to
        // result 'hull'
        p = q;

    } while (p != l);  // While we don't come to first point

    if (hull.size() < 3) { //todo fix
        std::vector<Point> empty;
        return empty;
    }


    return hull;
}


/// Line of sight ///


/*
 * A utility function determines whether it is possible to reach a single arc (line of sight) from a receiving point to the destination point defined for it.
 *
 * @param map - The map object being called.  
 * @param currPoint -  The current point we are checking its line of sight.
 * @param testPoint - A point we check if it is in the line of sight of the current point
 * 
 * @return true if the tested point is in line of sight of the current point, otherwise return false.
 */
bool isLos(Map& map, Point& currPoint, Point& testPoint) {
    int nextInd = 0;
    for (Obstacle& obIn : map.getObstacles()) {
        for (int i = 0; i < (int)obIn.getConvexVertexes().size(); i++) {
            nextInd = i < (int)obIn.getConvexVertexes().size() - 1 ? i + 1 : 0;

            Point firstP = obIn.getConvexVertexes()[i];
            Point secondP = obIn.getConvexVertexes()[nextInd];
            if (!(currPoint == firstP) && !(currPoint == secondP) && !(testPoint == firstP) && !(testPoint == secondP) && doIntersect(currPoint, testPoint, firstP, secondP))
                return false;
        }
    }
    return true;
}



/*
 * A function that finds for the current point all the other points that are in its line of sight.
 *
 * @param map - The map object being called.
 * @param currPoint -  The current point we are checking its line of sight.
 *
 * @return will return a list of all the points that are in the line of sight of the current point.
 */
std::vector<Point> ControlManager::lineOfSight(Map& map, Point& currPoint) {

    std::vector<Point> los;
    Point target = map.getTargetPoint();
    if (isLos(map, currPoint, target))
        los.push_back(map.getTargetPoint());

    for (Obstacle& obOut : map.getObstacles()) {

        std::vector<Point>& convexVertexes = obOut.getConvexVertexes();
        auto it = std::find(convexVertexes.begin(), convexVertexes.end(), currPoint);
        if (it != convexVertexes.end()) {
            int index = it - convexVertexes.begin();
            int before = index > 0 ? index - 1 : convexVertexes.size() - 1;
            int after = index < (int)convexVertexes.size() - 1 ? index + 1 : 0;

            los.push_back(convexVertexes[before]);
            los.push_back(convexVertexes[after]);

            continue;
        }

        for (Point& ver : convexVertexes) {
            if (isLos(map, currPoint, ver))
                los.push_back(ver);
        }
    }
    return los;
}

/*
 * Creating a full graph for the map, for visualizing the arcs in the graph.
 * Initializes a hashmap for tracking the line of sight of each point.
 */
void ControlManager::findFullGraph() {
    for (Map& map : maps) {             // creats route for the map.
        lineOfSightTable[map.getStartPoint().toString()] = lineOfSight(map, map.getStartPoint());

        for (Obstacle& obstacle : map.getObstacles()) {
            for (Point& point : obstacle.getConvexVertexes()) {
                lineOfSightTable[point.toString()] = lineOfSight(map, point);
            }
        }
    }
}


/// The easiest route ///

struct CompareF {
    
    /*
     * An operator that helps to define a relationship between 2 pairs for the purpose of using Priority Queue.
     *
     * @param p1 - A pair on which a relationship is defined.
     * @param p2 - A pair on which a relationship is defined.
     *
     * @return True if p1 > p2 otherwise returns false
     */
    bool operator()(std::pair<double, Point> const& p1, std::pair<double, Point> const& p2)
    {
        // return "true" if "p1" is ordered
        // before "p2", for example:
        return p1.first > p2.first;
    }
};

/*
 * An auxiliary function that chains one after the other the route from the starting point to the target point.
 *
 * @param input - The target point from which the routh track begins to be built
 * @param cameFrom - A hashmap for each point holds the point it came from.
 *
 * @return A vector of points describing the nodes in the path between the start point and the target point.
 */
std::vector<Point> reconstruct_path(Point *input, std::unordered_map<std::string, Point> & cameFrom) {
    Point* current = input;
    std::vector<Point> total_path = { *current };
        while (cameFrom.find(current->toString())!= cameFrom.end()) {
            current = &cameFrom[current->toString()];
            total_path.push_back(*current);
        }
        std::reverse(total_path.begin(), total_path.end());
        return total_path;
}

/*
 * A function to implement an A* algorithm that finds the easiest route between a start point and a target point.
 *
 * @param map - The map object being called.
 * @param start - A starting point from which the route begins.
 * @param target - The target you want to reach.
 * 
 * 
 * @return A vector of points describing the nodes in the path between the start point and the target point. will return an empty vector if the start point cannot be reached to the target point.
 */
std::vector<Point> ControlManager::aStar(Point& start, Point target, Map& map) {
    std::priority_queue<std::pair<double, Point>, std::vector<std::pair<double, Point>>, CompareF> openSet;

    std::unordered_map<std::string, double> gScore;
    std::unordered_map<std::string, double> fScore;
    std::unordered_map<std::string, Point> cameFrom;
    
    gScore[start.toString()] = 0;
    fScore[start.toString()] = euclideanDistance(start, target);

    openSet.push(std::make_pair(fScore[start.toString()], start));

    
    while (!openSet.empty()) {
        Point current = openSet.top().second;

        if (current == target)
            return reconstruct_path(&current, cameFrom);

        openSet.pop();
        for (Point& neighbor : lineOfSight(map, current)) {

            if (gScore.find(neighbor.toString()) == gScore.end()) {
                gScore[neighbor.toString()] = INFINITY;
            }
            double tentative_gScore = gScore[current.toString()] + euclideanDistance(current, neighbor);

            if (tentative_gScore < gScore[neighbor.toString()]) {
                cameFrom[neighbor.toString()] = current;
                gScore[neighbor.toString()] = tentative_gScore;
                fScore[neighbor.toString()] = tentative_gScore + euclideanDistance(neighbor, target);

                std::pair<double, Point> neighborPair = std::make_pair(fScore[neighbor.toString()], neighbor);
                
                openSet.push(neighborPair); 
            }
        }
    }

    std::vector<Point> result;
    return result;
}


/*
 * Initializes the easiest route in the internal map object.
 */
void ControlManager::findRoute() {
    for (Map& map : maps) {             // creats route for the map.
        std::vector<Point> route = aStar(map.getStartPoint(), map.getTargetPoint(), map);
        map.setRoute(route);
        for (Point& ptr : route)
            std::cout << ptr.toString() << std::endl;
    }
}
