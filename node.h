#ifndef NODE_H
#define NODE_H

#include <iostream>

using namespace std;

class node
{
private:
    string ID;

    int timeIn;
    int plannedTimeOut;
    int timeOut;

    int record[50];
    int average;

    int timetable[50];

    int counter1;
    int counter2;

public:
    node();

    void setID(string);
    void setRecord (int, int); // inputs: start time, finish time.
    void setTimetable(int);
    void setAverage();

    string getID();
    int getAverage();
    int getTimetable(int);
    int getCounter2();

    void printRecord();
    void printTimetable();
};

#endif // NODE_H
