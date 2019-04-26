#! /usr/bin/env python

import threading as th
import hashlib
import rospy
import time

from std_msgs.msg import String

prdt=""
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
        elif i in range (7,10):
            msgDataLength=msgDataLength+c
        elif i in range (10, (10+int(msgDataLength))):
            msgData=msgData+c
        else:
            checkSumRF=checkSumRF+c
        i+=1

    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    if checkSumRF!=checkSumG:
        return

    if msgCode=="006":
        list = msgData.split("@")
        prdt=list[0]
        checkC=1
    elif msgSource=="31" and msgCode=="045" and currentNode=="A1":
        checkC=1
    elif msgSource=="31" and msgCode=="045" and (currentNode == "P1" or currentNode=="P2") and pp==1:
        checkC=1
    elif msgSource=="11" and msgCode=="046" and currentNode=="P1":
        checkC=1
    elif msgSource=="12" and msgCode=="046" and currentNode=="P2":
        checkC=1



def rosOut(msg,topicOut):

    if pp==0 and topicOut=="/transport":
        topicOut="/vision"

    pub= rospy.Publisher(topicOut, String, queue_size=1000)
    time.sleep(1)

    print ("In topic: ", topicOut)
    rospy.loginfo(msg)

    pub.publish(msg)




def rosIn(topicIn):
    rate=rospy.Rate(5)
    while checkC==0:
        sub=rospy.Subscriber(topicIn, String, callback)
        rate.sleep()





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
        previousNode="MB"
        currentNode="A1"
        nextNode="P1"
    elif pathCounter==2:
        previousNode="A1"
        currentNode="P1"
        nextNode="A1"
    elif pathCounter==3:
        previousNode="P1"
        currentNode="A1"
        nextNode="P2"
    elif pathCounter==4:
        previousNode="A1"
        currentNode="P2"
        nextNode="A1"
    elif pathCounter==5:
        previousNode="P2"
        currentNode="A1"
        nextNode="FB"

    return (currentNode, nextNode)



def getMsg(u):
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
        if u=="0":
            msg="415101800431"+nNode
        elif u=="pick":
            msg="41510500011"
        elif u=="place":
            msg="41510500010"
        topic="/transport"
    elif currentNode=="P1":
        if u=="pick":
            msg="41510500011"
            topic="/transport"
        else:
            temp=prdt[0:4]
            msg="1151042004"+temp
            topic="/process"
    elif currentNode=="P2":
        if u=="pick":
            msg="41510501001"
            topic="/transport"
        else:
            msg="1251042000"
            topic="/process"
    elif currentNode=="RFID":
        if len(prdt)<10:
            length="00"+str(len(prdt))
        elif len(prdt)>9 and len(prdt)<100:
            length="0"+str(len(prdt))
        elif len(prdt)>99:
            length=str(len(prdt))
        msg="9151048005"+length+prdt
        topic="/rfid"

    return msg, topic




currentNode=""
nextNode=""
previousNode=""
pp=0


rospy.init_node('controlNode', anonymous=True)




nArray= importData()

pathCounter=0

print ("Waiting for product info")
rosIn("/ordered_item")

currentNode="RFID"
msg,topic=getMsg("0")
checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
rosOut(checkSum, topic)


while pathCounter<6:
    pp=0
    currentNode, nextNode= calculate(pathCounter)
    print ("currentNode=", currentNode, " nextNode=", nextNode, ": " )


    msg,topic=getMsg("0")

    checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
    rosOut(checkSum, topic)



    print ("Waiting for done message from node: ", currentNode)

    check=0
    checkC=0
    rosIn(topic)



    checkC=0

    if (currentNode=="A1" and nextNode=="MB") or ((currentNode=="P1" or currentNode=="P2") and nextNode=="A1"):
        pp=1
        msg,topic=getMsg("pick")
        checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
        rosOut(checkSum, "/transport")
        print ("Waiting for transport to pick object")
        rosIn(topic)
    elif currentNode=="A1" and (nextNode=="P1" or nextNode=="P2" or nextNode=="FB"):
        pp=1
        msg,topic=getMsg("place")
        checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
        rosOut(checkSum, "/transport")
        print ("Waiting for transport to place object")
        rosIn(topic)


    pathCounter+=1
