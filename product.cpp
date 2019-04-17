#include "product.h"

int counter=0;

product::product()
{
    corner[4]={0};
    shape[4]={0};
    stamp=0;

    currentLocation=" ";
    //pastLocations[5]={" "};
}

void product::setProduct(bool a[4], bool b)
{
    int i;
    for (i=0;i<4;i++){
        corner[i]=a[i];
        stamp=b;
    }
}

void product::updateLocation(string a)
{
    currentLocation=a;
    //pastLocations[counter]=a;
    counter++;
}


bool product::getCorner(int a)
{
    return (corner[a]);
}

bool product::getStamp()
{
    return (stamp);
}
