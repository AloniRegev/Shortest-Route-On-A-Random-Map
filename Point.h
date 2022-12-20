#include <string>

class Point{
    private:
        const int x;
        const int y;

    public:
        Point(int x, int y) : x(x), y(y) {};

        // Point::operator=(const Point & point){
        //     return Point(point.getX(), point.getY());
        // };

         int getX()const{return this->x;}
         int getY()const{return this->y;}
         std::string toString(){return "("+std::to_string(getX())+", "+std::to_string(getY())+")";}

};