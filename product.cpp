#include "product.h"

product::product()
{
    corner[4]={0};
//    colour[4]={0};
//    shape[4]={0};

    currentLocation=" ";
}

void product::setProduct(bool a[4], int b[4], int c[4])
{
    int i;
    for (i=0;i<4;i++){
        corner[i]=a[i];
        colour[i]=b[i];
        shape[i]=c[i];
    }
}


bool product::getCorner(int a)
{
    return (corner[a]);
}

int product::getColour(int a)
{
    return (colour[a]);
}

int product::getShape(int a)
{
    return (shape[a]);
}
