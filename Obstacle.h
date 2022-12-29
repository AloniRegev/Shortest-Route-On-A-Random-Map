#include "Polygon.h"

class Obstacle : public Polygon{
    private:
        std::vector<Point> convexVertexes; // const std::vector<Point> convexVertexes; // need to be const

    public:
        Obstacle(Polygon &polygon, std::vector<Point> vec) :Polygon(polygon), convexVertexes(vec) {};

        std::vector<Point> &getConvexVertexes() { return this->convexVertexes; } // std::vector<Point> getConvexVertexes()const{return this->convexVertexes;} // need to be const
};