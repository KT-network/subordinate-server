import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

engine = create_engine('mysql://whose:kunshao@127.0.0.1:3306/whose_subordinate?charset=utf8mb4', pool_size=50,
                       max_overflow=100, pool_timeout=3)

SessionClass = sessionmaker(bind=engine)

db = SessionClass()

dbrPool = redis.ConnectionPool(decode_responses=True, password="kunshao")

dbr = redis.Redis(password="kunshao", connection_pool=dbrPool)

# 服务器地址
# host = 'mqtt.kt-network.cn'
host = '192.168.0.7'

# mqtt端口
port = 1883
# 连接的客户标识
client_id = "services"

userName = "services"
userPwd = "123456"

topicState = "ks/subordinate/+/+/state"

topicConnected = "$SYS/brokers/+/clients/+/connected"
topicDisconnected = "$SYS/brokers/+/clients/+/disconnected"


