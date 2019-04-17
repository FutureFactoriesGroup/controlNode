#ifndef PRODUCT_H
#define PRODUCT_H

#include <iostream>

using namespace std;

class product
{
private:
    bool corner[4];
    char shape[4];
    bool stamp;

    string currentLocation;
    //string pastLocations[5];

public:
    product();

    void setProduct (bool[], bool);
    void updateLocation (string);

    bool getCorner(int);
    bool getStamp();

};

#endif // PRODUCT_H
