#include "Obstacle.h"

class Map{ 
    private:
        const int weight;
        const int height;
        Point startPoint; // const Point startPoint; // need to be const
        //Point targetPoint; 
        const Point targetPoint; // need to be const
        std::vector<Obstacle> obstacles; // const std::vector<Obstacle> obstacles; // need to be const

    
    public:
        Map( int _weight,  int _height,  Point _startPoint,  Point _targetPoint, std::vector<Obstacle>& _obstacles)
            :weight(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), obstacles(_obstacles){};

        int getWeight()const{return this->weight;}
        int getHeight()const{return this->height;}
        Point& getStartPoint(){return this->startPoint;} // Point& getStartPoint() const {return this->startPoint;} // need to be const
        //Point& getTargetPoint(){return this->targetPoint;} 
        Point getTargetPoint() const {return this->targetPoint;} // need to be const
        std::vector<Obstacle> &getObstacles(){return this->obstacles;} // std::vector<Obstacle> &getObstacles() const {return this->obstacles;} // need to be const

};
