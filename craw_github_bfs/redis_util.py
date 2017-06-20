# coding=utf-8
import redis

class RedisDBConfig:
    # HOST = '127.0.0.1'
    HOST ="10.103.90.151"
    PORT = 6379
    Default_list="list_github"
    Default_set="set_github_history"


def operator_status(func):
    '''get operatoration status
    '''
    def gen_status(*args, **kwargs):
        error, result = None, None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = str(e)
        if not error:
            return result
        else:
            return error
    return gen_status

class RedisCache(object):
    def __init__(self):
        if not hasattr(RedisCache, 'pool'):
            RedisCache.create_pool()
        self._connection = redis.Redis(connection_pool = RedisCache.pool)

    @staticmethod
    def create_pool():
        RedisCache.pool = redis.ConnectionPool(
                host = RedisDBConfig.HOST,
                port = RedisDBConfig.PORT,)

    @operator_status
    def set_data(self, key, value):
        '''set data with (key, value)
        '''
        return self._connection.set(key, value)

    @operator_status
    def get_data(self, key):
        '''get data by key
        '''
        return self._connection.get(key)

    @operator_status
    def del_data(self, key):
        '''delete cache by key
        '''
        return self._connection.delete(key)

    @operator_status
    def insert_list(self,*keys,listname=RedisDBConfig.Default_list):
        self._connection.lpush(listname,*keys)
        return self

    @operator_status
    def append_list(self,*keys,listname=RedisDBConfig.Default_list):
        self._connection.rpush(listname,*keys)
        return self

    @operator_status
    def size_list(self,listname=RedisDBConfig.Default_list):
        return self._connection.llen(listname)

    @operator_status
    def lpop_list(self,listname=RedisDBConfig.Default_list):
        return self._connection.lpop(listname).decode()

    @operator_status
    def rpop_list(self,listname=RedisDBConfig.Default_list):
        return self._connection.rpop(listname).decode()

    @operator_status
    def empty_list(self,listname=RedisDBConfig.Default_list):
        self._connection.delete(listname)
        return self

    @operator_status
    def push_set(self,*keys,setname=RedisDBConfig.Default_set):
        self._connection.sadd(setname,*keys)
        return self

    @operator_status
    def isin_set(self,key,setname=RedisDBConfig.Default_set):
        return self._connection.sismember(setname,key)

    @operator_status
    def size_set(self,setname=RedisDBConfig.Default_set):
        return self._connection.scard(setname)

    @operator_status
    def empty_set(self,setname=RedisDBConfig.Default_set):
        self._connection.delete(setname)
        return self



def demo1():
    r = RedisCache()
    r.insert_list(1,2,3,4)
    size = r.size_list()
    print(size)

def demo2():
    r = RedisCache()
    # r.insert_list(1,2,3,4)
    print(r.size_list())
    print(r.lpop_list())

def demo3():
    r = RedisCache()
    r.empty_set()
    r.push_set(4,11)
    print(r.isin_set("43"))
    print(r.size_set())


if __name__ == '__main__':
    r= RedisCache()
    print(r.size_list())
    print(r.size_set())

