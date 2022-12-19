#include <vector>
#include "Polygon.h"

class Obstacle : private Polygon{
    private:
        const std::vector<Point> convexVertexes;

    public:
        Obstacle(Polygon &polygon, std::vector<Point> vec) :Polygon(polygon), convexVertexes(vec) {};

        std::vector<Point> getConvexVertexes()const{return this->convexVertexes;}
};