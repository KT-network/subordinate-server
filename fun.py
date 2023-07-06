import hashlib


# 生成md5字符串
def getMd5(txt):
    hash_md5 = hashlib.md5()
    txt = txt + '-ks'
    data = txt.encode('utf-8')
    hash_md5.update(data)
    return hash_md5.hexdigest()


# 生成设备状态下发话题
def devicesStateIssueTopic(userId: str) -> str:
    return "ks/subordinate/" + userId + "/devices/state"


def devicesIssueTopic(devicesId: str) -> str:
    return "ks/subordinate/" + devicesId + "/action"
