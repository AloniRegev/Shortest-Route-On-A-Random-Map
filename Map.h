#include <vector>
#include "Polygon.h"

class Map{ 
    private:
        const int weight;
        const int height;
        const Point startPoint;
        const Point targetPoint;
        const std::vector<Polygon> polygons;
    
    public:
        Map( int _weight,  int _height,  Point _startPoint,  Point _targetPoint,  std::vector<Polygon>& _polygons)
            :weight(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), polygons(_polygons){};

        int getWeight()const{return this->weight;}
        int getHeight()const{return this->height;}
        Point getStartPoint()const{return this->startPoint;}
        Point getTargetPoint()const{return this->targetPoint;}
        std::vector<Polygon> getPolygons()const{return this->polygons;}
};
