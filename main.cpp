#include "ControlManager.h"
// #include "ControlManager.cpp"
#include <iostream>

int main(int argc,const char *argv[]){
     const char * inPath = argv[1];      // input name file
     const char * outPath = argv[2];     // output name file
    
    //const char * inPath = "C:/Code/GitHub/Shortest-Route-On-A-Random-Map/mapGenerator.xml";      // input name file
    //const char * outPath = "C:/Code/GitHub/Shortest-Route-On-A-Random-Map/algorithmOutput.xml";     // output name file

    std::vector<Map> maps;
    ControlManager control;             // initialize new control object.
    control.readXML(inPath, maps);            // read xml input.
 
    for (Map& map : maps) {
        //control.creatGraph(map);        // creats graph from the given map.
        std::vector<Point> routh = control.aStar(map.getStartPoint(), map.getTargetPoint(), map);
        map.setRoute(routh);
        for(Point& ptr: routh)
            std::cout << ptr.toString() << std::endl;
    }
    
    control.writeXML(outPath, maps);          // creats xml outputs.
}