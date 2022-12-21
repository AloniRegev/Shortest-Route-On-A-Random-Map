#include "ControlManager.h"

void ControlManager::readInput(const char * path){
    XMLDocument doc;
    doc.LoadFile(path);
    XMLElement *pRootElement = doc.RootElement();

    if (pRootElement != NULL) {
        XMLElement *pMap= pRootElement -> FirstChildElement("Maps")-> FirstChildElement("Map"); // pointer to the first map object data.
        while (pMap!=NULL){
            /*get map object attributes*/
            int weight = atoi(pMap -> FirstChildElement("Weight")->GetText());
            int height = atoi(pMap -> FirstChildElement("Height")->GetText());
            Point startPoint = Point(atoi(pMap ->FirstChildElement("StartPoint")->FirstChildElement("X")->GetText()), atoi(pMap ->FirstChildElement("StartPoint")-> FirstChildElement("Y")->GetText()));
            Point targetPoint = Point(atoi(pMap ->FirstChildElement("TargetPoint")->FirstChildElement("X")->GetText()), atoi(pMap ->FirstChildElement("TargetPoint")-> FirstChildElement("Y")->GetText()));
            
            std::vector<Obstacle> obstacles;

            XMLElement *pPolygon= pMap -> FirstChildElement("Polygons") -> FirstChildElement("Polygon"); // pointer to the first polygon object data.
            while(pPolygon!=NULL){
                /*get polygon object attributes*/
                std::vector<Point> vertexes;
                
                XMLElement *pVertex= pPolygon -> FirstChildElement("Vertexes") -> FirstChildElement("Vertex"); // pointer to the first vertex data.
                while (pVertex!=NULL){
                    Point vertex = Point(atoi(pVertex->FirstChildElement("X")->GetText()), atoi(pVertex ->FirstChildElement("Y")->GetText()));
                    vertexes.push_back(vertex); // add new vertex to vertex List.

                    pVertex = pVertex->NextSiblingElement("Vertex"); // move pointer to the next vertex data.
                }
                
                Polygon polygon= Polygon(vertexes.size(), vertexes); // create new polygon object.
                Obstacle obstacle = Obstacle(polygon, ConvexHull(vertexes)); // add new obstacle to obstacles List.
                obstacles.push_back(obstacle);

                pPolygon = pPolygon->NextSiblingElement("Polygon"); // move pointer to the next polygon object data.
            }
            Map map= Map(weight, height, startPoint, targetPoint, obstacles); // create new map object.
            maps.push_back(map); // add new map object to mapList. 

            pMap = pMap->NextSiblingElement("Map"); // move pointer to the next polygon object data.
        }
    }
}

void ControlManager::createOutput(const char * path){
    XMLDocument doc;
    XMLElement * pRoot = doc.NewElement("Root");
    doc.InsertFirstChild(pRoot);
    XMLElement * pMaps = doc.NewElement("Maps");
    pMaps->SetAttribute("size", maps.size());
    // // doc.InsertFirstChild(pMaps);
    // pRoot -> InsertEndChild(pMaps);

    maps=getMaps();
    for(int i=0; i<(int)maps.size(); i++){
        XMLElement * pMap = doc.NewElement("Map");
        pMap->SetAttribute("name", i);

            //insert weight value
            XMLElement * pWeight = doc.NewElement("Weight");
            pWeight->SetText(maps[i].getWeight());
            pMap->InsertEndChild(pWeight);

            //insert height value
            XMLElement * pHeight = doc.NewElement("Height");
            pHeight->SetText(maps[i].getHeight());
            pMap->InsertEndChild(pHeight);

            //insert start point
            XMLElement * pStartPoint = doc.NewElement("StartPoint");
            XMLElement *  pX= doc.NewElement("X");
            pX->SetText(maps[i].getStartPoint().getX());
            pStartPoint->InsertEndChild(pX);
            XMLElement *  pY= doc.NewElement("Y");
            pY->SetText(maps[i].getStartPoint().getY());
            pStartPoint->InsertEndChild(pY);
            pMap->InsertEndChild(pStartPoint);

            //insert target point
            XMLElement * pTargetPoint = doc.NewElement("TargetPoint");
            pX= doc.NewElement("X");
            pX->SetText(maps[i].getTargetPoint().getX());
            pTargetPoint->InsertEndChild(pX);
            pY= doc.NewElement("Y");
            pY->SetText(maps[i].getTargetPoint().getY());
            pTargetPoint->InsertEndChild(pY);
            pMap->InsertEndChild(pTargetPoint);

            //insert obsticals;
            XMLElement * pObsticals = doc.NewElement("Obsticals");
            pObsticals->SetAttribute("size", (int) maps[i].getObstacles().size());
            for(int j=0; j<(int) maps[i].getObstacles().size(); j++){
                XMLElement * pObstical = doc.NewElement("Obstical");
                pObstical->SetAttribute("name", j);

                XMLElement * pVertexes = doc.NewElement("Vertexes");
                pVertexes->SetAttribute("size", (int) maps[i].getObstacles()[j].getConvexVertexes().size());
                for(int k=0; k<(int) maps[i].getObstacles()[j].getConvexVertexes().size(); k++){
                    XMLElement * pVertex = doc.NewElement("Vertex");
                    pVertex->SetAttribute("name", k);

                        pX= doc.NewElement("X");
                        pX->SetText(maps[i].getObstacles()[j].getConvexVertexes()[k].getX());
                        pVertex->InsertEndChild(pX);
                        pY= doc.NewElement("Y");
                        pY->SetText(maps[i].getObstacles()[j].getConvexVertexes()[k].getY());
                        pVertex->InsertEndChild(pY);
                    
                    pVertexes->InsertEndChild(pVertex);
                }
                pObstical->InsertEndChild(pVertexes);
                pObsticals->InsertEndChild(pObstical);
            }
            pMap->InsertEndChild(pObsticals);

        pMaps->InsertEndChild(pMap);
    }
        pRoot->InsertEndChild(pMaps);

    doc.SaveFile(path);    
}


// Big cradit for GeeksforGeeks for there algorithem implementation.
std::vector<Point> ControlManager::ConvexHull(std::vector<Point> points){
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
    do
    {
        // Add current point to result
        hull.push_back(points[p]);
  
        // Search for a point 'q' such that orientation(p, q,
        // x) is counterclockwise for all points 'x'. The idea
        // is to keep track of last visited most counterclock-
        // wise point in q. If any point 'i' is more counterclock-
        // wise than q, then update q.
        q = (p+1)%n;
        for (int i = 0; i < n; i++)
        {
           // If i is more counterclockwise than current q, then
           // update q
           if (orientation(points[p], points[i], points[q]) == 2)
               q = i;
        }
  
        // Now q is the most counterclockwise with respect to p
        // Set p as q for next iteration, so that q is added to
        // result 'hull'
        p = q;
  
    } while (p != l);  // While we don't come to first point
  
   
    return hull;
}
  
int ControlManager::orientation(Point p, Point q, Point r)
{
    int val = (q.getY() - p.getY()) * (r.getX() - q.getX()) -
              (q.getX() - p.getX()) * (r.getY() - q.getY());
  
    if (val == 0) return 0;  // collinear
    return (val > 0)? 1: 2; // clock or counterclock wise
}
