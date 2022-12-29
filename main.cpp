#include "ControlManager.h"
// #include "ControlManager.cpp"
#include <iostream>

int main(int argc,const char *argv[]){
    const char * inPath = argv[1];      // input name file
    const char * outPath = argv[2];     // output name file
    
    ControlManager control;             // initialize new control object.
    control.readXML(inPath);            // read xml input.
 
    for(Map& map: control.getMaps()) 
        control.creatGraph(map);        // creats graph from the given map.

    control.writeXML(outPath);          // creats xml outputs.

}