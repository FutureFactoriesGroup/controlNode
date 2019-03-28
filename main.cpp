#include <iostream>

#include "funcs.cpp"
#include "node.h"
#include "product.h"

#define SIZE 4

using namespace std;

int main()
{
    //product prdt;

    int pathCounter=0;

    importData();
    calculate();

    while (pathCounter<getPathSteps()){
        issueCommand(pathCounter);
        pathCounter++;                     // Here an if loop will be added to receive the "end" command from the nodes
    }

}
