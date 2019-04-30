#! /usr/bin/env python

import threading as th
import hashlib
import rospy
import time

from std_msgs.msg import String









def callbackT(data):
    msgC=data.data

    global checkT
    global back
    global pp

    msgTarget=msgC[0:2]
    msgSource=msgC[2:4]
    msgCode=msgC[4:7]
    msgDataLength=msgC[7:10]
    msgData=msgC[10:(10+int(msgDataLength))]
    checkSumR=msgC[(10+int(msgDataLength)):(10+int(msgDataLength)+64)]

    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    if checkSumR!=checkSumG:
        return

    if msgSource=="31" and msgCode=="045" and back==0:
        checkT=1
    elif msgSource=="31" and msgCode=="053" and back==1:
        checkT=1
    elif msgSource=="31" and msgCode=="055" and pp==1:
        checkT=1



def callbackP(data):
    msgC=data.data

    global checkCNC
    global checkLED
    global prdtCount

    msgTarget=msgC[0:2]
    msgSource=msgC[2:4]
    msgCode=msgC[4:7]
    msgDataLength=msgC[7:10]
    msgData=msgC[10:(10+int(msgDataLength))]
    checkSumR=msgC[(10+int(msgDataLength)):(10+int(msgDataLength)+64)]


    msgRF=msgTarget+msgSource+msgCode+msgDataLength+msgData
    checkSumG=hashlib.sha256(msgRF.encode('utf-8')).hexdigest()
    if checkSumR!=checkSumG:
        return

    if msgSource=="11" and msgCode=="046":
        CNC.change_past(CNC.state)
        #CNC.change_state(-1)
        i=CNC.past[-1]
        prdtArray[i].update_status(0)
        print ("Product free to go")
    elif msgSource=="61" and msgCode=="046":
        led.change_past(led.state)
        #led.change_state(-1)
        i=led.past[-1]
        prdtArray[i].update_status(0)
        print ("Product free to go")


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
    if checkSumR!=checkSumG:
        return

    if msgCode=="006":
        prdtArray.append(prdt(msgData))
        prdtCount+=1
        print ("Product added")







class node:
    def __init__(self, ID):
        self.ID=ID
        self.state=-1
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
        self.data=data
        self.led=data[4]
        if data[0]=="N" and data[1]=="N" and data[2]=="N" and data[3]=="N":
            self.cnc=0
        else:
            self.cnc=1

        self.cNode=""
        self.status=0
        self.past=[]

    def update_cNode(self,cNode):
        self.cNode=cNode

    def update_status(self,status):
        self.status=status

    def update_past(self, u):
        self.past.append(u)



def getMsg(node1,u,prdtNb):

    if u=="a2b":
        msg="4151018003("+str(node1.ID)+")"
    elif u=="go" and node1==CNC:
        temp=prdtArray[prdtNb].data
        temp=temp[0:4]
        msg="1151042004"+temp
    elif u=="go" and node1==led:
        msg="6151051000"
    elif u=="pick":
        msg="4151050003(1)"
    elif u=="place":
        msg="4151050003(0)"
    elif u=="back":
        msg="3151052000"
    elif u=="rfidWrite":
        temp=prdtArray[prdtNb].data.split('@')
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

    global checkT
    global back

    msg=getMsg(MB,"back",i)
    pubT.publish(msg)
    print ("Waiting for transport to go back")
    back=1
    while checkT==0:
        continue
    checkT=0
    back=0

    if prdtArray[i].cNode=="CNC":
        tempNode=CNC
    elif prdtArray[i].cNode=="led":
        tempNode==led
    msg=getMsg(tempNode, "a2b",i)
    pubT.publish(msg)
    print ("Waiting for done message by transport")
    while checkT==0:
        continue
    checkT=0







subT=rospy.Subscriber("/transport", String, callbackT)
checkT=0

subP=rospy.Subscriber("/process", String, callbackP)
checkCNC=0
checkLED=0

subOI=rospy.Subscriber("/ordered_item", String, callbackOI)
prdtArray=[]

pubT= rospy.Publisher("/transport", String, queue_size=1000)
pubP= rospy.Publisher("/process", String, queue_size=1000)
pubOT= rospy.Publisher("/order_tracker", String, queue_size=1000)
pubR= rospy.Publisher("/rfid", String, queue_size=1000)



rospy.init_node('controlNode', anonymous=True)




prdtCount=0;
prdtArray=[]
finish=0
pp=0
back=0
check=0
trackOrder=[0,0,0,0,0]


print ("Waiting for product info")
# time.sleep(1)
# t1=th.Thread(target=getProduct())
# t1.start()
while 1:
    currentNode=transport
    if prdtArray:
        for i in range(prdtCount):
            if (i not in MB.past):
                if check==1:
                    msg=getMsg(MB,"back",i)
                    pubT.publish(msg)
                    print ("Waiting for transport to go back")
                    back=1
                    while checkT==0:
                        continue

                    checkT=0
                    back=0
                check=1

                print ("GOING TO MB")
                prdtArray[i].update_cNode("MB")
                msg=getMsg(currentNode, "rfidWrite", i)
                pubR.publish(msg)

                msg=getMsg(MB,"a2b",i)
                pubT.publish(msg)
                print ("Transport to: MB")
                while checkT==0:
                    continue

                MB.change_past(i)
                checkT=0
                transport.change_location("MB")

                prdtArray[i].update_cNode("MB")

                previousNode=MB
                trackOrder[0]=(i+1)
                trackOrder[1]=2
                pubOT.publish(str(trackOrder))


            print ("Product", i, "FOR CNC")
            print ((i not in CNC.past),(prdtArray[i].cnc==1),(CNC.state==-1),(prdtArray[i].status==0))



            if (i not in CNC.past) and (prdtArray[i].cnc==1) and (CNC.state==-1) and (prdtArray[i].status==0):

                print ("GOING TO CNC")
                if (transport.location!=prdtArray[i].cNode):
                    goToPrdt(i)

                msg=getMsg(prdtArray[i].cNode,"pick",i)
                pubT.publish(msg)
                print("Waiting for transport to pick object")
                pp=1
                while checkT==0:
                    continue
                if previousNode=="led":
                        trackOrder[0]=(i+1)
                        trackOrder[3]=2
                        pubOT.publish(str(trackOrder))

                checkT=0
                pp=0
                if prdtArray[i].cNode=="led":
                    led.change_state(-1)

                msg=getMsg(MB,"back",i)
                pubT.publish(msg)
                print ("Waiting for transport to go back")
                back=1
                while checkT==0:
                    continue

                checkT=0
                back=0




                msg=getMsg(CNC,"a2b",i)
                pubT.publish(msg)
                print ("Transport to: CNC")
                while checkT==0:
                    continue
                checkT=0
                transport.change_location("CNC")

                msg=getMsg(CNC,"place",i)
                pubT.publish(msg)
                print ("Waiting for transport to place object")
                pp=1
                while checkT==0:
                    continue
                checkT=0
                pp=0
                prdtArray[i].update_cNode("CNC")
                prdtArray[i].update_status(1)


                msg=getMsg(CNC,"go",i)
                pubP.publish(msg)

                CNC.change_state(i)
                print ("CNC state: ", CNC.state)

                previousNode=CNC
                trackOrder[0]=(i+1)
                trackOrder[2]=1
                pubOT.publish(str(trackOrder))

            print ("Product",i,"To LED:")
            print ((i not in led.past), (prdtArray[i].led=="Y"), (led.state==-1), (prdtArray[i].status==0))
            if (i not in led.past) and (prdtArray[i].led=="Y") and (led.state==-1) and (prdtArray[i].status==0):
                print ("GOING TO LED")

                if (transport.location!=prdtArray[i].cNode):
                    goToPrdt(i)

                msg=getMsg(prdtArray[i].cNode,"pick",i)
                pubT.publish(msg)
                print("Waiting for transport to pick object")
                pp=1
                while checkT==0:
                    continue

                checkT=0
                pp=0

                if prdtArray[i].cNode=="CNC":
                    CNC.change_state(-1)

                if previousNode=="CNC":
                        trackOrder[0]=i
                        trackOrder[2]=2
                        pubOT.publish(str(trackOrder))

                msg=getMsg(MB,"back",i)
                pubT.publish(msg)
                print ("Waiting for transport to go back")
                back=1
                while checkT==0:
                    continue
                checkT=0
                back=0



                msg=getMsg(led,"a2b",i)
                pubT.publish(msg)
                print ("Transport to: LEDs")
                while checkT==0:
                    continue
                checkT=0
                transport.change_location("led")

                msg=getMsg(CNC,"place",i)
                pubT.publish(msg)
                print ("Waiting for transport to place object")
                pp=1
                while checkT==0:
                    continue
                checkT=0
                pp=0

                prdtArray[i].update_cNode("led")
                prdtArray[i].update_status(1)

                msg=getMsg(led,"go",i)
                pubP.publish(msg)
                led.change_state(i)

                previousNode=led

                trackOrder[0]=i
                trackOrder[3]=1
                pubOT.publish(str(trackOrder))

            print ("LED state: ", led.state)
            print ("Product",i,"To FB:")
            print ((prdtArray[i].led=="Y"), (i in led.past), (prdtArray[i].cnc==1), (i in CNC.past), (prdtArray[i].led=="Y"), (i in led.past), (prdtArray[i].cnc==0),(prdtArray[i].led=="N"), (i in CNC.past), (prdtArray[i].cnc==1),(prdtArray[i].led=="N"), (prdtArray[i].cnc==0), (prdtArray[i].status==0))


            if (((prdtArray[i].led=="Y") and (i in led.past) and (prdtArray[i].cnc==1) and (i in CNC.past)) or ((prdtArray[i].led=="Y") and (i in led.past) and (prdtArray[i].cnc==0)) or ((prdtArray[i].led=="N") and (i in CNC.past) and (prdtArray[i].cnc==1)) or ((prdtArray[i].led=="N") and (prdtArray[i].cnc==0))) and (prdtArray[i].status==0):


                print ("GOING TO FB")
                msg=getMsg(prdtArray[i].cNode,"pick",i)
                pubT.publish(msg)
                print("Waiting for transport to pick object")
                pp=1
                while checkT==0:
                    continue

                checkT=0
                pp=0

                if prdtArray[i].cNode=="CNC":
                    CNC.change_state(-1)
                elif prdtArray[i].cNode=="led":
                    led.change_state(-1)

                msg=getMsg(MB,"back",i)
                pubT.publish(msg)
                print ("Waiting for transport to go back")
                back=1
                while checkT==0:
                    continue


                checkT=0
                back=0

                if (transport.location!=prdtArray[i].cNode):
                    goToPrdt(i)

                msg=getMsg(FB,"a2b",i)
                pubT.publish(msg)
                print ("Transport to: FB")
                while checkT==0:
                    continue
                checkT=0

                msg=getMsg(CNC,"place",i)
                pubT.publish(msg)
                print ("Waiting for transport to place object")
                pp=1
                while checkT==0:
                    continue
                checkT=0
                pp=0


                prdtArray.pop(i)
                prdtCount-=1
                print ("Product number ", i, " is done")


                trackOrder[0]=i
                trackOrder[4]=2
                pubOT.publish(str(trackOrder))
