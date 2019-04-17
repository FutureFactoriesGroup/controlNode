#include <iostream>
#include <fstream>  //
#include <string>
#include <sstream>  //
#include <iomanip>

#include "node.h"
#include "product.h"



#define SIZE 3

using namespace std;

node nArray[SIZE];
product prdt;


int i,j,k,l,m,n=0;
bool tempb;
int tempi, tempi1, tempi2;
string temps;

int times[2]={0};
string sequence [2]={" "};

string currentNode, nextNode;

void importData ()
{


//    ifstream testFile;
//    testFile.open("testRecord.txt");
//
//    i=0; k=0; l=0;
//    tempb=0;
//
//    while (testFile>>temps){
//        i++;
//        switch (i){
//        case 1:
//            for (j=0;j<SIZE;j++){
//                if (nArray[j].getID()==temps) {
//                    tempb=1;
//                    l=j;
//                }
//            }
//            if (tempb==0) {
//                nArray[k].setID(temps);
//                l=k;
//                k++;
//            }
//            break;
//        case 2:
//            stringstream(temps)>>tempi1;
//            break;
//        case 3:
//            stringstream(temps)>>tempi2;
//            nArray[l].setRecord(tempi1,tempi2);
//        }
//        if (i==3) {i=0;tempb=0;}
//    }
//
//    testFile.close();

    nArray[0].setID("P1");
    nArray[1].setID("P2");
    nArray[2].setID("A1");


//    ifstream timetableFile;
//    timetableFile.open("timetable.txt");
//
//    k=0; tempb=0; tempi=0;
//
//    while (timetableFile>>temps) {
//        for (j=0;j<SIZE;j++){
//            if (nArray[j].getID()==temps) {
//                tempb=1;
//                k=j;
//                break;
//            }
//        }
//        if (tempb==0) {
//            stringstream(temps)>>tempi;
//            nArray[k].setTimetable(tempi);
//        }
//
//        tempb=0;
//    }
//
//    timetableFile.close();

    ifstream prdtFile;
    prdtFile.open("productInput.txt");

    i=0; j=0; k=0;
    bool corner[4],stamp;

    while (prdtFile>>tempi) {
        if (i<4){corner[i]=tempi;}
        else if (i=4) {stamp=tempi;}
        i++;
    }

    prdtFile.close();

    prdt.setProduct(corner,stamp);

//    cout<< "/// RECORD"<< endl << endl;
//    for (i=0;i<SIZE;i++){
//        nArray[i].setAverage();
//        nArray[i].printRecord();
//        cout << "Average: " << nArray[i].getAverage() << endl;
//    }
//
//    cout << endl << endl << endl << "/// TIMETABLE" << endl << endl;
//    for (i=0;i<SIZE;i++){
//        nArray[i].printTimetable();
//    }
//
//    cout << endl << endl << endl << "// PRODUCT" << endl << endl;
//    cout << "corner" << setw(15)<<"colour"<<setw(20)<<"shape"<<endl;
//    for (i=0;i<4;i++){
//       cout << prdt.getCorner(i)<<setw(15)<<prdt.getColour(i)<<setw(20)<<prdt.getShape(i)<<endl;
//    }
}





//void ttblTest (string n1, string n2, int loop, int jvalue1, int jvalue2, int check, int times[16], string sequence[16])
//{
//    j=0; n=0;
//    for (i=0;i<SIZE;i++){
//
//        if (nArray[i].getID()==n1 || nArray[i].getID()==n2){
//            if (nArray[i].getID()=="P1" && check==2) {j=4;n=0;}
//            else if (nArray[i].getID()=="P2" && check==2) {j=0;}
//
//
//            for (m=0;m<loop;m++){
//                for (k=0; k<nArray[i].getCounter2(); k++) {
//                    if (((nArray[i].getAverage() + times[j])>nArray[i].getTimetable(k)) && (times[j]<(nArray[i].getTimetable(k)+nArray[i].getAverage()))){
//                        times [j]= nArray[i].getTimetable(k) + nArray[i].getAverage();
//                    }
//                }
//
//                times[j]=times[j]+nArray[i].getAverage();
//                sequence[j]=sequence[j]+ nArray[i].getID()+" ";
//                tempi=times[j];
//                temps=sequence[j];
//                for (l=j;l<(j+jvalue1);l++){times[l]=tempi; sequence[l]=temps; }
//
//                if (check==2){
//                    if (n==0){j=j+2; n++;}
//                    else if (n==1) {j=j+6;n=0;}}
//                else {j=j+jvalue2;}
//            }
//            if (check==1) {j=jvalue2/2;}
//
//        }
//    }
//}





void calculate (int pathCounter)
{
    if (pathCounter==0){currentNode="A1"; nextNode="MB";}
    else if (pathCounter==1){currentNode="A1"; nextNode="P1";}
    else if (pathCounter==2) {currentNode="P1"; nextNode="A1";}
    else if (pathCounter==3) {currentNode="A1"; nextNode="P2";}
    else if (pathCounter==4) {currentNode="P2"; nextNode="A1";}
    else if (pathCounter==5) {currentNode="A1"; nextNode="FB";}
}

//void updateTime()
//{
//    //?????
//}

//void addRecord(int t1, int t2, string node)
//{
//    for (i=0;i<SIZE;i++){
//        if (nArray[i].getID()==node){nArray[i].setRecord(t1,t2);}
//    }
//}

string getMsg(string currentNode, string nextNode)
{
    string msg;
    int cNode=0, nNode=0;

    if (nextNode=="A1"){nNode=13;}
    else if (nextNode=="P1"){nNode=11;}
    else if (nextNode=="P2") {nNode=21;}
    else if (nextNode=="MB") {nNode=17;}
    else if (nextNode=="FB") {nNode=18;}

    if (currentNode=="A1"){
        stringstream ss;
        ss<<nNode;
        msg="151303131"+ss.str();
    }
    else if (currentNode=="P1"){
        tempb=0;
        msg="1511036611"+nNode;
        for (i=0;i<4;i++){
            tempb=prdt.getCorner(i);
            stringstream ss;
            ss<<nNode;
            msg=msg+ss.str();
        }
        msg=msg+"0";
    }
    else if (currentNode=="P2"){
        msg="15110366P2"+nextNode+"00001";
    }
    return (msg);
}

string getCurrentNode ()
{
    return (currentNode);
}

string getNextNode ()
{
    return (nextNode);
}


