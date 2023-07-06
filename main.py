import json
import os
import threading
import time
from datetime import datetime
from config import *
from dataBase import *
from paho.mqtt import client as mqtt_client
import fun

mClient = mqtt_client.Client(client_id=client_id)

# {"key":{"now":0,"last":5}}
a = {"uesr": [{"devicesId": True}, {"devicesId1": False}]}

devicesAndUser = {}

tick = 61
tickMin = 61

lock = threading.RLock()


def msgCallback(client, userdata, msg):
    topics = msg.topic.split("/")
    print(msg.topic)
    lock.acquire()
    if topics[len(topics) - 1] == "connected":
        jo = json.loads(msg.payload)
        userName = jo.get("username")
        userId = fun.getMd5(userName)

        if jo.get("clientid")[- 3:] == "app":
            # 判断clientid等不等userid
            # 当用户上线之后
            # 修改用户的在线状态
            # 查询用户所属的设备
            if jo.get("clientid")[:-4] == userId:
                db.query(User).filter(User.user == userName, User.delTime == None).update({"state": True})
                db.commit()
                devices = db.query(User).filter(User.user == userName, User.delTime == None).first().devices.filter(
                    Devices.delTime == None).all()
                devicesState = {}
                for item in devices:
                    devicesState.update({item.devicesId: item.state})
                mClient.publish(fun.devicesStateIssueTopic(userId), json.dumps(devicesState))

        else:
            # 当设备上线之后
            # 修改当前设备的在线状态
            # 查询用户所属的设备
            user = db.query(User).filter(User.user == userName, User.delTime == None).first()
            if user is not None:
                db.query(User).filter(User.user == userName, User.delTime == None).first() \
                    .devices.filter(Devices.delTime == None, Devices.devicesId == jo.get("clientid")).update(
                    {"state": True})
                db.commit()
                if user.state:
                    devices = db.query(User).filter(User.user == userName, User.delTime == None).first().devices.filter(
                        Devices.delTime == None).all()
                    devicesState = {}
                    for item in devices:
                        devicesState.update({item.devicesId: item.state})
                    mClient.publish(fun.devicesStateIssueTopic(userId), json.dumps(devicesState))


    elif topics[len(topics) - 1] == "disconnected":
        jo = json.loads(msg.payload)
        userName = jo.get("username")
        userId = fun.getMd5(userName)
        if jo.get("clientid")[- 3:] == "app":
            if jo.get("clientid")[:-4] == userId:
                db.query(User).filter(User.user == userName, User.delTime == None).update({"state": False})
                db.commit()
        else:
            user = db.query(User).filter(User.user == userName, User.delTime == None).first()
            if user is not None:
                db.query(User).filter(User.user == userName, User.delTime == None).first() \
                    .devices.filter(Devices.delTime == None, Devices.devicesId == jo.get("clientid")).update(
                    {"state": False})
                db.commit()
                if user.state:
                    devices = db.query(User).filter(User.user == userName, User.delTime == None).first().devices.filter(
                        Devices.delTime == None).all()
                    devicesState = {}
                    for item in devices:
                        devicesState.update({item.devicesId: item.state})
                    mClient.publish(fun.devicesStateIssueTopic(userId), json.dumps(devicesState))
    lock.release()


def connectCallback(client, userdata, flags, rc):
    if rc == 0:
        print("连接成功")
        mClient.subscribe(topicConnected)
        mClient.subscribe(topicDisconnected)
        mClient.on_message = msgCallback


def disconnectedCallback(client, userdata, rc):
    print("断开连接")


while True:
    if not mClient.is_connected():
        print("mqtt开始连接!")
        mClient.on_connect = connectCallback
        mClient.on_disconnect = disconnectedCallback
        mClient.username_pw_set(userName, userPwd)
        mClient.connect(host, port)
        mClient.loop_start()
        time.sleep(3)
        continue

    if tick != datetime.now().second:
        tick = datetime.now().second

    # 策略
    if datetime.now().second % 2 == 0 and tick != datetime.now().second:
        lock.acquire()
        for devices in db.query(Devices).filter(Devices.state == True, Devices.delTime == None).all():

            for config in devices.config.all():
                if config.configType == ConfigType.SWITCH:
                    if not config.complete:
                        if not config.lasting:

                            if int(dbr.get(config.devicesId+"/"+str(config.id))) < 10:

                            # 不保持(完成操作)并且发布
                            config.update({"complete": True})
                        else:
                            if datetime.now().minute % config.interval and tickMin != datetime.now().minute:
                                config.value.value
                            pass

            # data = open("3133123.png", 'rb').read()
            # data = bytes([1, 0, 0, 1, 0, 0, 1, 0]) + data
            s = "ks".encode()
            mClient.publish(fun.devicesIssueTopic(devices.devicesId), bytes([11, 22, 0, 1, 0, 0, 1, 0]))
        lock.release()

    # if tick != datetime.now().second:
    #     tick = datetime.now().second
    #     # print(tick % 6)
    #     # print(devicesStateMsg)
    #
    # if datetime.now().second % 6 == 0 and tick != datetime.now().second:
    #     for key in devicesStateMsg.keys():
    #         devicesS = devicesStateMsg.get(key)
    #         lastTime = devicesS.get("last")
    #         nowTime = devicesS.get("now")
    #         if (lastTime != nowTime) and (abs(lastTime - nowTime) < 6) and (abs(nowTime - lastTime) < 6):
    #             devicesS.update({"last": nowTime})
    #
    #             # devicesStateMsg.update({key: {"last": nowTime}})
    #
    # # global message_received
    # # if message_received :
    # #     continue
    # lock.acquire()
    # for key in devicesStateMsg.keys():
    #     devicesS = devicesStateMsg.get(key)
    #     lastTime = devicesS.get("last")
    #     nowTime = devicesS.get("now")
    #     if (lastTime != nowTime) and (abs(lastTime - nowTime) < 6) and (abs(nowTime - lastTime) < 6):
    #         print("在线")
    #
    #     else:
    #         print("==========================")
    #
    # lock.release()
