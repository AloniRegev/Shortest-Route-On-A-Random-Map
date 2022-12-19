#include "ControlManager.cpp"
#include <iostream>

int main(int argc, char *argv[]){
    char * path = argv[1]; // input read file
    // const char * path = "C:\\Code\\GitHub\\Shortest-Route-On-A-Random-Map\\mapGenerator.exe";

    ControlManager control;
    control.readInput(path);

    std::cout<<control.getMaps()[0].getTargetPoint().toString() <<std::endl;
}