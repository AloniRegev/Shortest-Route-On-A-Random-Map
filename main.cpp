#include "ControlManager.h"

int main(int argc,const char *argv[]){
     const char * inPath = argv[1];     // input name file
     const char * outPath = argv[2];    // output name file

    ControlManager control;             // initialize new control object.
    control.readXML(inPath);            // read xml input.
    control.findFullGraph();            // Creating a full graph for the map, for the purpose of visualizing only. To improve efficiency can be put as a comment.
    control.findRoute();                // creats route and full graph for the map.
    control.writeXML(outPath);          // creats xml outputs.
}