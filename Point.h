#include <string>
#include <vector>
#include <iostream>
#include <math.h>

class Point{
    private:
        /*const*/ int x;
        /*const*/ int y;

        //std::vector<Point> lineOfSight;

    public:
        Point(int x, int y) : x(x), y(y) {};

        Point() : x(0), y(0){};

        //Point(const Point& other) : x(other.x), y(other.y), lineOfSight(other.lineOfSight) {};

        /// operators overloading ///
        bool operator==(const Point & other) const{
            return(this->getX() == other.getX() && this->getY() == other.getY());
        };
         
        /* Point operator=(const Point& other) const {
            return Point(other);
        }*/

        /// getters and setters //
        int getX()const{return this->x;}
        int getY()const{return this->y;}

        //std::vector<Point> getPahts()  { return this->lineOfSight; }

        //void setPaths(std::vector<Point> lineOfSight) {
        //    this->lineOfSight.clear();
        //    for (Point point : lineOfSight) {
        //        Point ver(point.getX(), point.getY()); // TODO remove
        //        this->lineOfSight.push_back(ver);
        //    }
        //} 

        /// Class functions ///
        std::string toString() { return "(" + std::to_string(getX()) + ", " + std::to_string(getY()) + ")"; }

        bool prtCmp(const Point & other) const{
            return(this->getX() == other.getX() && this->getY() == other.getY());
        };

};