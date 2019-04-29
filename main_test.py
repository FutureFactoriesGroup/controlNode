#! /usr/bin/env python

import threading as th
import hashlib
import rospy
import time

from std_msgs.msg import String

prdt=[]
checkC=0

class node:
    def __init__(self, ID):
        self.ID=ID




def callback1(data):
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

    if msgSource=="31" and msgCode=="045" and currentNode=="A1":
        checkC=1
    elif msgSource=="31" and msgCode=="045" and (currentNode == "P1" or currentNode=="P2") and pp==1:
        checkC=1
    elif msgSource=="11" and msgCode=="046" and currentNode=="P1":
        checkC=1
    elif msgSource=="12" and msgCode=="046" and currentNode=="P2":
        checkC=1
    elif msgSource=="31" and msgCode=="053" and currentNode=="A1" and pp==2:
        checkC=1


def callback2(data):
    global prdt
    global prdtLength
    msgR=data.data

    msgTarget= ""
    msgSource= ""
    msgCode= ""
    msgDataLength= ""
    msgData= ""
    checkSumRF=""

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
    elif msgCode=="006":
        prdt.append(msgData)
        prdtLength=msgDataLength
        print ("Product added")





def rosOut(msg,topicOut):

    pub= rospy.Publisher(topicOut, String, queue_size=1000)
    time.sleep(2)
    pub.publish(msg)




def rosIn(topicIn):
    rate=rospy.Rate(5)
    while checkC==0:
        sub=rospy.Subscriber(topicIn, String, callback1)
        rate.sleep()
        time.sleep(1)
        # print("checkC= " ,checkC)


def getProduct():
    rate=rospy.Rate(5)
    sub1=rospy.Subscriber("/ordered_item", String, callback2)
    rate.sleep()



def importData():
    nArray=[]
    nArray.append(node("P1"))
    nArray.append(node("P2"))
    nArray.append(node("A1"))
    return nArray


def calculate(pathCounter):
    global previousNode
    if pathCounter==0:
        cNode="A1"
        nNode="MB"
    elif pathCounter==1:
        previousNode="MB"
        cNode="A1"
        nNode="P1"
    elif pathCounter==2:
        previousNode="A1"
        cNode="P1"
        nNode="A1"
    elif led=="Y" and pathCounter==3:
        previousNode="P1"
        cNode="A1"
        nNode="P2"
    elif led=="N" and pathCounter==3:
        previousNode="P1"
        cNode="A1"
        nNode="FB"

    elif led=="Y" and pathCounter==4:
        previousNode="A1"
        cNode="P2"
        nNode="A1"
    elif led=="Y" and pathCounter==5:
        previousNode="P2"
        cNode="A1"
        nNode="FB"

    return (cNode, nNode)



def getMsg(u):
    msg= None
    topic= None
    global prdt
    if nextNode=="A1":
        nNode="3"
    elif nextNode=="P1":
        nNode="1"
    elif nextNode=="P2":
        nNode="6"
    elif nextNode=="MB":
        nNode="7"
    elif nextNode=="FB":
        nNode="8"

    if currentNode=="A1":
        if u=="0":
            msg="4151018003("+nNode+")"
        elif u=="pick":
            msg="4151050003(1)"
        elif u=="place":
            msg="4151050003(0)"
        topic="/transport"
    elif currentNode=="P1":
        if u=="pick":
            msg="4151050003(1)"
            topic="/transport"
        else:
            temp=prdt[0]
            temp=temp[0:4]
            msg="1151042004"+temp
            topic="/process"
    elif currentNode=="P2":
        if u=="pick":
            msg="4151050003(1)"
            topic="/transport"
        else:
            msg="1251051000"
            topic="/process"
    elif currentNode=="RFID":
        temp=prdt[0].split("@")
        temp=temp[0]
        if len(temp)<10:
            length="00"+str(len(temp))
        elif len(temp)>9 and len(temp)<100:
            length="0"+str(len(temp))
        elif len(temp)>99:
            length=str(len(temp))
        msg="9151048"+length+temp
        topic="/rfid"

    return msg, topic





def findLed():
    temp=prdt[0]
    return temp[4]

def findCNC():
    temp=prdt[0]
    if (temp[0] and temp[1] and temp[2] and temp[3])=="N":
        return 0
    else:
        return 1


currentNode=""
nextNode=""
previousNode=""
pp=0
led=""
cnc=""
checkC=0
UItrack=[1,0,0,0,0]
UIcount=1


rospy.init_node('controlNode', anonymous=True)




nArray= importData()

pathCounter=0



print ("Waiting for product info")
#rosIn("/ordered_item")
#sub=rospy.Subscriber("/ordered_item", String, callback1)

time.sleep(1)
t1=th.Thread(target=getProduct())
t1.start()



while 1:
    if prdt:
        led=findLed()
        cnc=findCNC()
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


            if (currentNode=="A1" and pathCounter==1):
                UItrack[UIcount]=2
                UIcount+=1
            elif  currentNode=="P1" or currentNode=="P2":
                UItrack[UIcount]=1
            rosOut(str(UItrack),"/order_tracker")




            print ("Waiting for done message from node: ", currentNode)

            check=0
            checkC=0
            rosIn(topic)

            checkC=0


            #pick/place
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


            # go back a bit
            if (currentNode=="A1" and previousNode=="MB") or currentNode=="P1" or currentNode=="P2":
                pp=2
                msg="3151052000"
                topic="/transport"
                checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
                rosOut(checkSum, topic)
                rosIn (topic)


            if currentNode=="P1" or currentNode=="P2":
                UItrack[UIcount]=2
                rosOut(str(UItrack),"/order_tracker")
                UIcount+=1



            if pathCounter==3 and led=="N":
                break

            if pathCounter==0 and cnc==0
                pathCounter==2

            pathCounter+=1



        UItrack[4]=2
        rosOut(str(UItrack),"/order_tracker")

        prdt.pop(0)
