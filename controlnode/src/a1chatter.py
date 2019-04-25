#!/usr/bin/env python

import rospy
import hashlib


from std_msgs.msg import String

def chatter():

    while 1:
        topic=raw_input("Input topic: ")
        pub=rospy.Publisher(topic, String, queue_size=1000)
        rospy.init_node('chatter',anonymous=True)


        msg=raw_input("Input message sent by node: ")
        checkSum=hashlib.sha256(msg.encode('utf-8')).hexdigest()
        msg=msg+checkSum
        rospy.loginfo(msg)
        pub.publish(msg)


if __name__ == '__main__':
    try:
        chatter()
    except rospy.ROSInterruptException:
        pass
