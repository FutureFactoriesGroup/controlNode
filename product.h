#ifndef PRODUCT_H
#define PRODUCT_H

#include <iostream>

using namespace std;

class product
{
private:
    bool corner[4];
    int colour[4];
    int shape[4];

    string currentLocation;

public:
    product();

    void setProduct (bool[], int[], int[]);
    void updateLocation (string);

    bool getCorner(int);
    int getColour(int);
    int getShape(int);

};

#endif // PRODUCT_H
