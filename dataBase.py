from config import engine
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    SUPER_USER = 0
    ADMIN_USER = 1
    NORMAL_USER = 2


class ProgramType(enum.Enum):
    PIXEL_SCREEN_21_29 = 0  # 21*29像素
    USER_CUSTOM = 1  # 自定义像素（涂鸦）
    USER_TEXT = 2  # 自定义Text（文本）


class ConfigType(enum.Enum):
    SWITCH = 0
    PROGRAM = 1


# 开关型的值
class SwitchValue(enum.Enum):
    OPEN = 0  # 只开
    CLOSE = 1  # 只关
    FLICKER = 2  # 开->关->开


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # 数据id
    user = Column(String(11), nullable=False)
    passwd = Column(String(255), nullable=False)
    email = Column(String(50), nullable=False)
    devices = relationship("Devices", backref='user', lazy='dynamic')
    role = Column(Enum(UserRole), default=UserRole.NORMAL_USER)
    state = Column(Boolean, default=False)
    createTime = Column(DateTime)
    delTime = Column(DateTime)


class Devices(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)  # 数据id
    name = Column(String(11), nullable=False)
    devicesId = Column(String(255), nullable=False)
    devicesType = Column(String(100), nullable=False)
    picUrl = Column(String(255), nullable=False)
    state = Column(Boolean, default=False)
    userId = Column(Integer, ForeignKey('user.id'))
    dev_state = relationship("DevicesHistoryState", backref='devices', lazy='dynamic')
    config = relationship("DevicesConfig", backref="devices", lazy="dynamic")
    createTime = Column(DateTime)
    delTime = Column(DateTime)


class DevicesHistoryState(Base):
    __tablename__ = 'deviceshistorystate'
    id = Column(Integer, primary_key=True)  # 数据id
    date = Column(DateTime, nullable=False)
    state = Column(Boolean, nullable=False)
    devicesId = Column(Integer, ForeignKey('devices.id'))


class DevicesType(Base):
    __tablename__ = 'devicestype'
    id = Column(Integer, primary_key=True)  # 数据id
    name = Column(String(11), nullable=False)
    type = Column(String(255), nullable=False)
    picUrl = Column(String(255), nullable=False)
    size = Column(String(20), nullable=True)
    createTime = Column(DateTime)
    delTime = Column(DateTime)


# 适用于支持节目播放的设备
class Program(Base):
    __tablename__ = 'program'
    id = Column(Integer, primary_key=True)  # 数据id
    programType = Column(Enum(ProgramType), nullable=True)
    filePath = Column(String(255))


class DevicesConfig(Base):
    __tablename__ = 'devicesconfig'
    id = Column(Integer, primary_key=True)  # 数据id
    devicesId = Column(Integer, ForeignKey('devices.id'))  # 设备id
    name = Column(String(11), nullable=False)  # 配置名称
    configType = Column(Enum(ConfigType), default=ConfigType.SWITCH)  # 配置类型（开关型，节目型）
    IO = Column(Integer, nullable=True)  # 引脚
    value = Column(Enum(SwitchValue), nullable=True)  # 开关型的值
    complete = Column(Boolean, default=False)  # 完成操作
    interval = Column(Integer, nullable=True)  # 保持间隔
    lasting = Column(Boolean, default=False)  # 保持


if __name__ == '__main__':

    Base.metadata.create_all(engine)
