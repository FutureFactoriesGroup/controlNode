#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>

#include "node.h"
#include "product.h"

#define SIZE 4

using namespace std;

node nArray[SIZE];
product prdt;


int i,j,k,l,m,n=0;
bool tempb;
int tempi, tempi1, tempi2;
string temps;

int times[16]={0};
string sequence [16]={" "};

void importData ()
{


    ifstream testFile;
    testFile.open("testRecord.txt");

    i=0; k=0; l=0;
    tempb=0;

    while (testFile>>temps){
        i++;
        switch (i){
        case 1:
            for (j=0;j<SIZE;j++){
                if (nArray[j].getID()==temps) {
                    tempb=1;
                    l=j;
                }
            }
            if (tempb==0) {
                nArray[k].setID(temps);
                l=k;
                k++;
            }
            break;
        case 2:
            stringstream(temps)>>tempi1;
            break;
        case 3:
            stringstream(temps)>>tempi2;
            nArray[l].setRecord(tempi1,tempi2);
        }
        if (i==3) {i=0;tempb=0;}
    }

    testFile.close();


    ifstream timetableFile;
    timetableFile.open("timetable.txt");

    k=0; tempb=0; tempi=0;

    while (timetableFile>>temps) {
        for (j=0;j<SIZE;j++){
            if (nArray[j].getID()==temps) {
                tempb=1;
                k=j;
                break;
            }
        }
        if (tempb==0) {
            stringstream(temps)>>tempi;
            nArray[k].setTimetable(tempi);
        }

        tempb=0;
    }

    timetableFile.close();

    ifstream prdtFile;
    prdtFile.open("productInput.txt");

    i=0; j=0; k=0;
    int colour[4],shape[4];
    bool corner[4];

    while (prdtFile>>tempi) {
        if (i<4){corner[i]=tempi;}
        else if (i>3 && i<8){colour[j]=tempi;j++;}
        else if (i>7){shape[k]=tempi;k++;}
        i++;
    }

    prdtFile.close();

    prdt.setProduct(corner,colour,shape);

    cout<< "/// RECORD"<< endl << endl;
    for (i=0;i<SIZE;i++){
        nArray[i].setAverage();
        nArray[i].printRecord();
        cout << "Average: " << nArray[i].getAverage() << endl;
    }

    cout << endl << endl << endl << "/// TIMETABLE" << endl << endl;
    for (i=0;i<SIZE;i++){
        nArray[i].printTimetable();
    }

    cout << endl << endl << endl << "// PRODUCT" << endl << endl;
    cout << "corner" << setw(15)<<"colour"<<setw(20)<<"shape"<<endl;
    for (i=0;i<4;i++){
       cout << prdt.getCorner(i)<<setw(15)<<prdt.getColour(i)<<setw(20)<<prdt.getShape(i)<<endl;
    }
}





void ttblTest (string n1, string n2, int loop, int jvalue1, int jvalue2, int check, int times[16], string sequence[16])
{
    j=0; n=0;
    for (i=0;i<SIZE;i++){

        if (nArray[i].getID()==n1 || nArray[i].getID()==n2){
            if (nArray[i].getID()=="P1" && check==2) {j=4;n=0;}
            else if (nArray[i].getID()=="P2" && check==2) {j=0;}


            for (m=0;m<loop;m++){
                for (k=0; k<nArray[i].getCounter2(); k++) {
                    if (((nArray[i].getAverage() + times[j])>nArray[i].getTimetable(k)) && (times[j]<(nArray[i].getTimetable(k)+nArray[i].getAverage()))){
                        times [j]= nArray[i].getTimetable(k) + nArray[i].getAverage();
                    }
                }

                times[j]=times[j]+nArray[i].getAverage();
                sequence[j]=sequence[j]+ nArray[i].getID()+" ";
                tempi=times[j];
                temps=sequence[j];
                for (l=j;l<(j+jvalue1);l++){times[l]=tempi; sequence[l]=temps; }

                if (check==2){
                    if (n==0){j=j+2; n++;}
                    else if (n==1) {j=j+6;n=0;}}
                else {j=j+jvalue2;}
            }
            if (check==1) {j=jvalue2/2;}

        }
    }
}





void calculate ()
{


    int cornerCount=0, colour1Count=0, colour2Count=0;

    for (i=0;i<4;i++){
        if (prdt.getCorner(i)==1){
            cornerCount++;
            if (prdt.getColour(i)==1){colour1Count++;}
            else if (prdt.getColour(i)==2){colour2Count++;}
        }
    }

    ttblTest ("A1" , "A2", 1, 8, 8, 0, times, sequence);


    if (colour1Count>0 && colour2Count>0){
        ttblTest ("P1" , "P2", 2, 4, 8, 1, times, sequence);
//        for (u=0;u<colour1Count;u++){ttblTest ("P1" , "OO", 2, 4, 8, 1, times, sequence);}
//        for (u=0; u<colour2Count;u++){ttblTest ("P1" , "P2", 2, 4, 8, 1, times, sequence);}
    }
    else if (colour1Count>0 && colour2Count==0){
        for (int u=0;u<colour1Count;u++){ttblTest ("P1" , "OO", 2, 8, 8, 0, times, sequence);}
    }
    else if (colour1Count==0 && colour2Count>0){
        for (int u=0;u<colour2Count;u++){ttblTest ("OO" , "P2", 2, 8, 8, 0, times, sequence);}
    }


    if (colour1Count>0 && colour2Count>0){
        ttblTest ("A1" , "A2", 4, 2, 4, 1, times, sequence);
        ttblTest ("P1" , "P2", 4, 2, 0, 2, times, sequence);
    }

    ttblTest ("A1" , "A2", 8, 0, 2, 1, times, sequence);


    cout << endl << endl << "/////////" << endl;
    for (i=0;i<16;i++){cout << "Time: " << times[i] << " counter: " << i<< " sequence: " << sequence[i] << endl;}

    tempi2=times[0];
    for (i=1;i<=16;i++) {
        tempi1=times[i];
        if (tempi1<tempi2){tempi2=tempi1;}
    }
    cout << endl << "Best time: " << tempi2 << "s   Sequences: ";
    for (i=1;i<=16;i++) {
        if (times[i]==tempi2) {cout << sequence[i] << "         ";}
    }
    cout << endl << endl;
}


int getPathSteps()
{
    stringstream ss(sequence[0]);
    int pathSteps=0;
    while (ss>>temps){
        pathSteps++;
    }
    return (pathSteps);
}


void issueCommand(int pathCounter)
{
    int tempArr[5];
    i=0;

    stringstream ss(sequence[0]);
    while (ss>>temps){
        tempArr[i]=temps;
    }



}

