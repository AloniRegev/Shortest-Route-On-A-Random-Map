
#include "Point.h"

class Polygon{
    private:
        const int numOfVertices;
        const std::vector<Point> vertexes; 


    public:
        Polygon(int numOfVertices, std::vector< Point>& vec) : numOfVertices(numOfVertices), vertexes(vec) {};

        std::vector<Point> getVertexes()const{return this->vertexes;}
};