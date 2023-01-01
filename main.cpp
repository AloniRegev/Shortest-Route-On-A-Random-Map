#include "ControlManager.h"
// #include "ControlManager.cpp"
#include <iostream>

int main(int argc,const char *argv[]){
    const char * inPath = argv[1];      // input name file
    const char * outPath = argv[2];     // output name file
    

    std::vector<Map> maps;
    ControlManager control;             // initialize new control object.
    control.readXML(inPath, maps);            // read xml input.
 
    for(Map& map: maps)
        control.creatGraph(map);        // creats graph from the given map.

    control.writeXML(outPath, maps);          // creats xml outputs.

}