#include <sstream>
#include <ros/ros.h>
#include <stdlib.h>

using namespace std;

void rosOut (string topic, string command,int argc, char **argv)
{
    ros::init(argc, argv, "control");
    ros::nodeHandle n;
    ros::Publisher pub=n.advertise <std_msgs::String> (topic, 1000);

    std_msgs::command;
    pub.publish (command)
}
