#! /usr/bin/env python

import threading as th
import hashlib
import rospy
import time



rospy.init_node('controlNode', anonymous=True)



subT=rospy.Subscriber("/transport", string, callbackT)
checkT=0

subP=rospy.Subscriber("/process", string, callbackP)
checkCNC=0
checkLED=0

subOI=rospy.Subscriber("/ordered_item", string, callbackOI)
prdtArray=[]

pubT= rospy.Publisher("/transport", String, queue_size=1000)
pubP= rospy.Publisher("/process", String, queue_size=1000)
pubOT= rospy.Publisher("/order_tracker", String, queue_size=1000)
pubR= rospy.Publisher("/rfid", String, queue_size=1000)







def callbackT(data):
    msgC=data.data

    global checkT

    msgTarget=msgC[0:2]
    msgSource=msgC[2:4]
    msgCode=msgC[4:7]
    msgDataLength=msgC[7:10]
    msgData=msgC[10:(10+int(msgDataLength))]
    checkSumR=msgC[(10+int(msgDataLength)):(10+int(msgDataLength)+64)]

    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    if checkSumRF!=checkSumG:
        return

    if msgSource=="31" and msgCode=="045":
        checkT=1



def callbackP(data):
    msgC=data.data

    global checkCNC
    global checkLED

    msgTarget=msgC[0:2]
    msgSource=msgC[2:4]
    msgCode=msgC[4:7]
    msgDataLength=msgC[7:10]
    msgData=msgC[10:(10+int(msgDataLength))]
    checkSumR=msgC[(10+int(msgDataLength)):(10+int(msgDataLength)+64)]


    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    if checkSumRF!=checkSumG:
        return

    if msgSource=="11" and msgCode=="046":
        CNC.change_past(CNC.state)
        CNC.change_state(0)
    elif msgSource=="12" and msgCode=="046":
        led.change_past(led.state)
        led.change_state(0)



def callbackOI(data):
    msgC=data.data

    global prdtArray
    global prdtCount

    msgTarget=msgC[0:2]
    msgSource=msgC[2:4]
    msgCode=msgC[4:7]
    msgDataLength=msgC[7:10]
    msgData=msgC[10:(10+int(msgDataLength))]
    checkSumR=msgC[(10+int(msgDataLength)):(10+int(msgDataLength)+64)]

    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    if checkSumRF!=checkSumG:
        return

    if msgCode=="006":
        prdtArray.append(prdt(msgData))
        prdtCount+=1
        print ("Product added")







class node:
    def __init__(self, ID):
        self.ID=ID
        self.state=0
        self.past=[]
        self.location=""

    def change_state(self, state):
        self.state=state

    def change_past(self,newPrdt):
        self.past.append(newPrdt)

    def change_location(self,loc):
        self.location=loc


transport=node(3)
CNC=node(1)
led=node(6)
MB=node(7)
FB=node(8)




class prdt:
    def __init__(self,data):
        self.prdtData=data
        self.led=data[4]
        if (data[0] and data[1] and data[2] and data[3])=="N":
            self.cnc=0
        else:
            self.cnc=1
        self.cNode="MB"

    def update_cNode(self,cNode):
        self.cNode=cNode



def getMsg(node1,u,prdtNb):

    if u=="a2b":
        msg="4151018003("+node1.ID+")"
    elif u=="go" and node1==CNC:
        temp=prdtArray[prdtNb]
        temp=temp[0:4]
        msg="1151042004"+temp
    elif u=="go" and node1==led:
        msg="12510151000"
    elif u=="pick":
        msg="4151050003(1)"
    elif u=="place":
        msg="4151050003(0)"
    elif u=="back":
        msg="3151052000"
    elif u=="rfidWrite":
        temp=prdtArray[prdtNb].split("@")
        temp=temp[0]
        if len(temp)<10:
            length="00"+str(len(temp))
        elif len(temp)>9 and len(temp)<100:
            length="0"+str(len(temp))
        elif len(temp)>99:
            length=str(len(temp))
        msg="9151048"+length+temp

     checkSum=msg+hashlib.sha256(msg.encode('utf-8')).hexdigest()
     return checkSum;


def goToPrdt(i):
    msg=getMsg(prdtArray[i].cNode, "a2b",i)
    pubT.publish(msg)
    print ("Waiting for done message by transport")
    while checkT==0:
        continue
    checkT=0

    msg=getMsg(MB,"pick",i)
    pubT.publish(msg)
    print("Waiting for transport to pick object")
    while checkT==0:
        continue
    checkT=0




prdtCount=0;
prdtArray=[]
finish=0




print ("Waiting for product info")
# time.sleep(1)
# t1=th.Thread(target=getProduct())
# t1.start()
while 1:
    currentNode=transport
    if prdtArray:
        for i in range(prdtCount):
            if (i not in MB.past):
                msg=getMsg(currentNode, "rfidWrite", i)
                pubR.publish(msg)

                msg=getMsg(MB,"a2b",i)
                pubT.publish(msg)
                print ("Waiting for done message by transport")
                while checkT==0:
                    continue

                MB.change_past(i)
                checkT=0
                transport.change_location("MB")

                msg=getMsg(MB,"pick",i)
                pubT.publish(msg)
                print("Waiting for transport to pick object")
                while checkT==0:
                    continue

                checkT=0

                msg=getMsg(MB,"back",i)
                pubT.publish(msg)
                print ("Waiting for transport to go back")
                while checkT==0:
                    continue

                checkT=0

            if (i not in CNC.past) and (prdtArray[i].cnc==1) and (CNC.state==0):
                if (transport.location!=prdtArray[i].cNode):
                    gotoPrdt(i)

                msg=getMsg(CNC,"a2b",i)
                pubT.publish(msg)
                print ("Waiting for done message by transport")
                while checkT==0:
                    continue
                checkT=0
                transport.change_location("CNC")

                msg=getMsg(CNC,"place",i)
                pubT.publish(msg)
                print ("Waiting for transport to place object")
                while checkT==0:
                    continue
                checkT=0
                prdtArray[i].update_cNode("CNC")

                msg=getMsg(CNC,"go",i)
                pubP.publish(msg)
                CNC.change_state(i)

            elif (i not in led.past) and (prdtArray[i].led==1) and (led.state==0):
                if (transport.location!=prdtArray[i].cNode):
                    gotoPrdt(i)

                msg=getMsg(led,"a2b",i)
                pubT.publish(msg)
                print ("Waiting for done message by transport")
                while checkT==0:
                    continue
                checkT=0
                transport.change_location("led")

                msg=getMsg(CNC,"place",i)
                pubT.publish(msg)
                print ("Waiting for transport to place object")
                while checkT==0:
                    continue
                checkT=0
                prdtArray[i].update_cNode("led")

                checkT=0
                msg=getMsg(led,"go",i)
                pubP.publish(msg)
                led.change_state(i)


            elif ((prdtArray[i].led==1) and (i in led.past) and (prdtArray[i].cnc==1) and (i in CNC.past)) or ((prdtArray[i].led==1) and (i in led.past) and (prdtArray[i].cnc==0)) or ((prdtArray[i].led==0) and (i in CNC.past) and (prdtArray[i].cnc==1)) or ((prdtArray[i].led==0) and (prdtArray[i].cnc==0)):
                if (transport.location!=prdtArray[i].cNode):
                    gotoPrdt(i)

                msg=getMsg(FB,"a2b",i)
                pubT.publish(msg)
                print ("Waiting for done message by transport")
                while checkT==0:
                    continue
                checkT=0

                prdtArray.pop(i)
                prdtCount-=1
                print ("Product number ", i, " is done")
