#include "findBestRouth.h"
vector<Map> readInput(const char * inputFile){
    XMLDocument doc;
    doc.LoadFile(inputFile);
    XMLElement *pRootElement = doc.RootElement();
    vector<Map> maps;

    if (pRootElement != NULL) {
        XMLElement *pMap= pRootElement -> FirstChildElement("Maps")-> FirstChildElement("Map"); // pointer to the first map object data.
        while (pMap!=NULL){
            /*get map object attributes*/
            int weight = atoi(pMap -> FirstChildElement("Weight")->GetText());
            int height = atoi(pMap -> FirstChildElement("Height")->GetText());
            Point startPoint = Point(atoi(pMap ->FirstChildElement("StartPoint")->FirstChildElement("X")->GetText()), atoi(pMap ->FirstChildElement("StartPoint")-> FirstChildElement("Y")->GetText()));
            Point targetPoint = Point(atoi(pMap ->FirstChildElement("TargetPoint")->FirstChildElement("X")->GetText()), atoi(pMap ->FirstChildElement("TargetPoint")-> FirstChildElement("Y")->GetText()));
            vector<Polygon> polygons;

            XMLElement *pPolygon= pMap -> FirstChildElement("Polygons") -> FirstChildElement("Polygon"); // pointer to the first polygon object data.
            while(pPolygon!=NULL){
                /*get polygon object attributes*/
                vector<Point> vertexes;
                
                XMLElement *pVertex= pPolygon -> FirstChildElement("Vertexes") -> FirstChildElement("Vertex"); // pointer to the first vertex data.
                while (pVertex!=NULL){
                    Point vertex = Point(atoi(pVertex->FirstChildElement("X")->GetText()), atoi(pVertex ->FirstChildElement("Y")->GetText()));
                    vertexes.push_back(vertex); // add new vertex to vertex List.

                    pVertex = pVertex->NextSiblingElement("Vertex"); // move pointer to the next vertex data.
                }
                Polygon polygon= Polygon(vertexes.size(), vertexes); // create new polygon object.
                polygons.push_back(polygon); // add new polygon to polygon List.

                pPolygon = pPolygon->NextSiblingElement("Polygon"); // move pointer to the next polygon object data.
            }
            Map map= Map(weight, height, startPoint, targetPoint, polygons); // create new map object.
            maps.push_back(map); // add new map object to mapList. 

            pMap = pMap->NextSiblingElement("Map"); // move pointer to the next polygon object data.
        }
    }
        return maps;
}

int main(int argc, char *argv[]){
    const char * path = argv[1]; // input read file
    // const char * path = "C:\\Code\\GitHub\\Shortest-Route-On-A-Random-Map\\mapGenerator.exe";

    vector<Map> mapList= readInput(path);
    std::cout<<mapList[0].getTargetPoint().toString() <<std::endl;
}