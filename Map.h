#include <vector>
#include "Obstacle.h"

class Map{ 
    private:
        const int weight;
        const int height;
        const Point startPoint;
        const Point targetPoint;
        const std::vector<Obstacle> obstacles;

    
    public:
        Map( int _weight,  int _height,  Point _startPoint,  Point _targetPoint, std::vector<Obstacle>& _obstacles)
            :weight(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), obstacles(_obstacles){};

        int getWeight()const{return this->weight;}
        int getHeight()const{return this->height;}
        Point getStartPoint()const{return this->startPoint;}
        Point getTargetPoint()const{return this->targetPoint;}
        std::vector<Obstacle> getObstacles()const{return this->obstacles;}

};
