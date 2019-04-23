#!/usr/bin/env python

import rospy


from std_msgs.msg import String

def chatter():
    
    while 1:
        topic=raw_input("Input topic: ")
        pub=rospy.Publisher(topic, String, queue_size=1000)
        rospy.init_node('chatter',anonymous=True)


        msg=raw_input("Input message sent by node: ")
        rospy.loginfo(msg)
        pub.publish(msg)


if __name__ == '__main__':
    try:
        chatter()
    except rospy.ROSInterruptException:
        pass
