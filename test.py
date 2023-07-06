import time
from datetime import datetime

from config import db
from dataBase import *

if __name__ == '__main__':
    # userDb = db.query(User).filter(User.user == "8413698461", User.delTime == None).first()
    # devicesDb = userDb.devices.filter(Devices.delTime == None).all()
    # print(userDb)
    # db.add(User(user="74123", passwd="123456", email="123456@com.cn"))
    # db.commit()

    a = db.query(User).filter(User.user == "123", User.delTime == None).first()
    de = a.devices.first()
    print(de.config.first().value.value)
    # print(a.devices.filter(Devices.id == 1).first().config.first().configType)
    # print(datetime.now().timestamp())

