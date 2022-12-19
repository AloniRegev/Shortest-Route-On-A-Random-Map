#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <tuple>
#include "./tinyxml2/tinyxml2.cpp"
#include "Map.h"


using namespace tinyxml2;

class ControlManager{
private:
    std::vector<Map> maps;
public:
    void readInput(char * inputFile);

    std::vector<Map> getMaps(){return this->maps;}
    
};
