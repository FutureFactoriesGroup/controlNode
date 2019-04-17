#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>


#include "funcs.cpp"
#include "node.h"
#include "product.h"
#include "picosha2.h"

#define SIZE 4

using namespace std;
std::condition_variable cv;
std::mutex mtx;

bool A1Ready=0;
bool A1Done=0;
bool nodeReady() {return (A1Ready==1);}
bool nodeDone() {return (A1Done==1);}

int check=0;
//void callback(const std_msgs::String::ConstPtr& msg)
//{
//    string msg= msg->data;
//    if (msg="513104211"){A1Ready=1; cv.notify_all();}
//    else {
//        i=0; check=0;
//        for(char&c:msg){
//            if (c=='5' && i==0){check=1;}
//            else if (i==4) {temps=c;}
//            else if (i==5||i==6) {temps=temps+c;}
//        }
//    }
//
//    if (check==1 && temps=="043") {A1Done=1;}
//}
//
//int rosIn (int argc, char **argv, string topic)
//{
//    ros::init(argc, argv, "controlNode");
//    ros::NodeHandle n;
//    ros::Subscriber sub = n.subscribe(topic, 1000, callback);
//
//    unique_lock<std::mutex> lck(mtx);
//
//
//}

void rosInTest ()
{
    A1Ready=0; A1Done=0;
    string msg,temps;
    cin >> msg;
    if (msg=="513104211"){A1Ready=1; cv.notify_all();}
    else {
        i=0; check=0;
        for(char&c:msg){
            if (c=='5' && i==0){check=1;}
            else if (i==4) {temps=c;}
            else if (i==5||i==6) {temps=temps+c;}
            i++;
        }
    }

    if (check==1 && temps=="043") {A1Done=1;cv.notify_all();}
}

int main()
{

    string action;

    //product prdt;

    int i;

    int pathCounter=0;
    int currentTime=0, previousTime=0;
    string currentNode, nextNode;
    string msg, topic;

    importData();

    while (pathCounter<6){
        A1Ready=0;

        calculate(pathCounter);
        currentNode=getCurrentNode(); nextNode=getNextNode();
        cout << "Current node: " << currentNode << "     Next node: " << nextNode;

        cout << endl << endl << "Waiting for ready message sent by " << currentNode<< ": ";
        thread t1 (rosInTest);
        unique_lock<std::mutex> lck(mtx);
        cv.wait(lck, nodeReady);

        msg=getMsg(currentNode, nextNode);
        if (currentNode=="A1"){topic="/transport";}
        else if (currentNode=="P1" || currentNode=="P2"){topic="/process";}
        cout << endl << endl << "Message sent by Control node: " << msg << " on topic: " << topic << endl;
        //rosOut(topic, msg, int argc, char **argv);                 // edit rosOut I guess?

        std::string src_str = msg;
        std::vector<unsigned char> hash(picosha2::k_digest_size);
        picosha2::hash256(src_str.begin(), src_str.end(), hash.begin(), hash.end());
        std::string hex_str = picosha2::bytes_to_hex_string(hash.begin(), hash.end());

        cout << "Checksum: " << msg << " " <<hex_str<<endl;


        cout << endl << "Waiting for finished message of " << currentNode << ": ";
        thread t2 (rosInTest);
        //unique_lock<std::mutex> lck(mtx);
        cv.wait(lck, nodeDone);

        pathCounter++;

        t1.join();
        t2.join();
        //previousTime=currentTime;
    }


}
