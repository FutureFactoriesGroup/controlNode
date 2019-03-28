#include "node.h"


#include <iostream>
#include <iomanip>

using namespace std;

node::node()
{
    ID=" ";

    timeIn=0;
    plannedTimeOut=0;
    timeOut=0;

    record[50]={0};
    average=0;

    timetable[50]={0};

    counter1=0;
    counter2=0;
}

void node::setID(string a)
{
    ID=a;
}

void node::setRecord(int a,int b)
{
    record[counter1]=b-a;
    counter1 ++;
}

void node::setTimetable(int a)
{
    timetable[counter2]=a;
    counter2++;
}

void node::setAverage()
{
    int i;
    for (i=0;i<counter1;i++){
        average=average+record[i];
    }
    average=average/(counter1);
}




string node::getID()
{
    return(ID);
}

int node::getAverage()
{
    return (average);
}

int node::getCounter2()
{
    return(counter2);
}

int node::getTimetable(int a)
{
    return(timetable[a]);
}






void node::printRecord()
{
    int i;
    cout << "ID: " << ID << endl << "Previous processing times (in seconds): ";
    for (i=0;i<counter1;i++){cout << record[i] << "  ";}

}

void node::printTimetable()
{
    int i;
    cout << "ID: " << ID << endl << "Timetable: ";
    for (i=0;i<counter2;i++) {cout << timetable[i] << "  ";}
    cout << endl;
}
