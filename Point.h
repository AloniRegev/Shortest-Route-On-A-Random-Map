#include <string>
#include <vector>
#include <iostream>

class Point{
    private:
        const int x;
        const int y;

        std::vector<Point> paths;

    public:
        Point(int x, int y) : x(x), y(y) {};

         bool operator==(const Point & point) const{
             return(this->getX() == point.getX() && this->getY() == point.getY());
         };

         int getX()const{return this->x;}
         int getY()const{return this->y;}

         //std::vector<Point> getPahts() const { return this->paths; }
         std::vector<Point> getPahts()  { return this->paths; }

         void setPaths(std::vector<Point> paths) {
             this->paths.clear();
             for (Point path : paths) {
                 Point point(path.getX(), path.getY());
                 this->paths.push_back(point);
             }
         } 

         std::string toString() { return "(" + std::to_string(getX()) + ", " + std::to_string(getY()) + ")"; }

};