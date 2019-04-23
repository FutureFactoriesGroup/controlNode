#! /usr/bin/env python

import threading as th
import hashlib
import rospy

from std_msgs.msg import String

prdt=None
rd=0            # 0 if ready, 1 if done
checkC=0

class node:
    def __init__(self, ID):
        self.ID=ID





def callback(data):
    global checkC
    global prdt
    global rd
    checkC=0
    msgR=data.data

    msgTarget= ""
    msgSource= ""
    msgCode= ""
    msgDataLength= ""
    msgData= ""
    checkSumRF=""
    check=0
    temps=""
    i=0

    for c in msgR:
        if i==0 or i==1:
            msgTarget=msgTarget+c
        elif i==2 or i==3:
            msgSource=msgSource+c
        elif i in range(4,7):
            msgCode=msgCode+c
        elif i==7:
            msgDataLength=c
        elif i in range (8, (8+int(msgDataLength))):
            msgData=msgData+c
        else:
            checkSumRF=checkSumRF+c
        i+=1

    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    # checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    # if checkSumRF!=checkSumG
    #     return

    if msgCode=="006":
        prdt=msgData
        checkC=1
    elif msgSource=="31" and msgCode=="043" and currentNode=="A1" and rd==0:
        checkC=1
    elif msgSource=="31" and msgCode=="045" and currentNode=="A1" and rd==1:
        checkC=1
    elif msgSource=="11" and msgCode=="046" and currentNode=="P1" and rd==1:
        checkC=1
    elif msgSource=="12" and msgCode=="046" and currentNode=="P2" and rd==1:
        checkC=1

    # while (nodeReady==0 and nodeDone==0):
    #     if msgR=="513104211" and currentNode=="A1":
    #         nodeReady=1
    #     elif msgR=="511104411" and currentNode=="P1":
    #         nodeReady=1
    #     elif msgR=="511204411" and currentNode=="P2":
    #         nodeReady=1
    #     else:
    #         i=0
    #
    #         for c in msgR:
    #             if c=="5" and i==0:
    #                 check=1
    #             elif i==2:
    #                 temps=c
    #             elif i in range (3,7):
    #                 temps=temps+c
    #             i+=1
    #
    #
    #     if check==1 and temps=="31043" and currentNode=="A1":
    #         nodeDone=1
    #
    #     elif check==1 and temps=="11044" and currentNode=="P1":
    #         nodeDone=1
    #     elif check==1 and temps=="12044" and currentNode=="P2":
    #         nodeDone=1
    #
    #
    #
    # if nodeReady==1 or nodeDone==1:
    #     checkC=1
    # else:
    #     checkC=0



def rosOut(msg,topic):

    pub= rospy.Publisher(topic, String, queue_size=1000)

    if topic=="/transport":
        topic="/vision"

    print ("In topic: ", topic)
    rospy.loginfo(msg)

    pub.publish(msg)

    # if (currentNode=="A1"):
    #     pub= rospy.Publisher("/UI", String, queue_size=1000)








def importData():
    nArray=[]
    nArray.append(node("P1"))
    nArray.append(node("P2"))
    nArray.append(node("A1"))
    return nArray


def calculate(pathCounter):
    if pathCounter==0:
        currentNode="A1"
        nextNode="MB"
    elif pathCounter==1:
        currentNode="A1"
        nextNode="P1"
    elif pathCounter==2:
        currentNode="P1"
        nextNode="A1"
    elif pathCounter==3:
        currentNode="A1"
        nextNode="P2"
    elif pathCounter==4:
        currentNode="P2"
        nextNode="A1"
    elif pathCounter==5:
        currentNode="A1"
        nextNode="FB"

    return (currentNode, nextNode)



def getMsg(currentNode, nextNode):
    msg= None
    topic= None
    global prdt
    if nextNode=="A1":
        nNode="31"
    elif nextNode=="P1":
        nNode="11"
    elif nextNode=="P2":
        nNode="12"
    elif nextNode=="MB":
        nNode="71"
    elif nextNode=="FB":
        nNode="81"

    if currentNode=="A1":
        msg="4151018431"+nNode
        topic="/transport"
    elif currentNode=="P1":
        msg="11510420"
        topic="/process"
    elif currentNode=="P2":
        msg="12510420"
        topic="/process"
    elif currentNode=="RFID":
        msg="91510485"+prdt
        topic="/rfid"

    return msg, topic




currentNode=""
nextNode=""


rospy.init_node('controlNode', anonymous=True)

nArray= importData()

pathCounter=0

print ("Waiting for product info")
rate=rospy.Rate(5)
while checkC==0:
    sub=rospy.Subscriber("/UI", String, callback)
    rate.sleep()

msg,topic=getMsg("RFID", "0")
checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
rosOut(checkSum, topic)


while pathCounter<6:
    currentNode, nextNode= calculate(pathCounter)
    print ("currentNode=", currentNode, " nextNode=", nextNode, ": " )
    msg,topic=getMsg(currentNode, nextNode)

    if currentNode=="A1":
        rd=0
        print ("Waiting for ready message from: ", currentNode)
        check=0
        checkC=0

        rate=rospy.Rate(5)
        while checkC==0:
            sub=rospy.Subscriber(topic, String, callback)
            rate.sleep()
    #t1=th.Thread(target=goSpin())

    #t1.start()
    #if callback==0:
    #    t1.join()



    checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
    rosOut(checkSum, topic)

    rd=1
    print ("Waiting for done message from node: ", currentNode)

    check=0
    checkC=0


    while checkC==0:
        rospy.Subscriber(topic, String, callback)
        rate.sleep()


    pathCounter+=1









#                              ~~~~~TESTS~~~~~




# class leClass:
#     def __init__(self,value):
#         self.value=value
#
#     # def change_value (self, i):
#     #     self.value=i
#
# def doStuff():
#     arr=[leClass(i+1) for i in range (3)]
#     return arr
#
# arroo=doStuff()
# print (arroo[0].value)
# print (arroo[1].value)
# print (arroo[2].value)
#
# # print ("\n")
# # for i in range (3):
# #     arroo[i].change_value(i+2)
# #     print (arroo[i].value)
