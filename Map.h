#include "Obstacle.h"

class Map{ 
    private:
        const int width;
        const int height;
        //Point startPoint; 
        const Point startPoint; // need to be const
        
        //Point targetPoint; 
        const Point targetPoint; // need to be const
        std::vector<Obstacle> obstacles; // const std::vector<Obstacle> obstacles; // need to be const
        std::vector<Point> route;

    
    public:
        Map( int _weight,  int _height,  Point _startPoint,  Point _targetPoint, std::vector<Obstacle>& _obstacles)
            :width(_weight), height(_height), startPoint(_startPoint), targetPoint(_targetPoint), obstacles(_obstacles){};

        /// Getters and setters ///
        int getWeight()const{return this->width;}
        int getHeight()const{return this->height;}
        
        //Point& getStartPoint(){return this->startPoint;} 
         Point getStartPoint() const {return this->startPoint;} // need to be const
        
        //Point& getTargetPoint(){return this->targetPoint;} 
        Point getTargetPoint() const {return this->targetPoint;} // need to be const
        
        std::vector<Obstacle> &getObstacles(){return this->obstacles;} 
        // std::vector<Obstacle> &getObstacles() const {return this->obstacles;} // need to be const

        std::vector<Point> getRoute()const { return this->route; }
        
        void setRoute(std::vector<Point> route) {  //deep copy for route.
            this->route.clear();
            for (Point point : route) {
                Point ver(point.getX(), point.getY());
                this->route.push_back(ver);
            }
        }
};
