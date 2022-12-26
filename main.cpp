#include "ControlManager.cpp"
#include <iostream>

int main(int argc,const char *argv[]){
    const char * inPath = argv[1]; // input read file
    const char * outPath = argv[2]; // input read file

    // const char * path = "C:\\Code\\GitHub\\Shortest-Route-On-A-Random-Map\\mapGenerator.exe";

    ControlManager control;
    control.readInput(inPath);

//    std::cout<<"\npolygon"<<std::endl;
//    std::vector<Point> polygonList = control.getMaps()[0].getObstacles()[0].getVertexes();
//    for (int i = 0; i < (int) polygonList.size(); i++){
//        std::cout<<polygonList[i].toString()<<std::endl; //todo remove
//    }
//
//    std::cout<<"\nconvex"<<std::endl;
//    std::vector<Point> obsticalList=control.getMaps()[0].getObstacles()[0].getConvexVertexes();
//    for (int i = 0; i < (int) obsticalList.size(); i++){
//        std::cout<<obsticalList[i].toString()<<std::endl; //todo remove
//
//    }
//
//     std::cout<<std::endl;
//    std::cout<<"\ntarget point"<<std::endl;
//    std::cout<<control.getMaps()[0].getTargetPoint().toString() <<std::endl;

    control.createOutput(outPath);
}