import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def get(self, key):
        try:
            return self.client.get(key)
        except Exception as e:
            # 这里可以做异常分级处理
            print(f"Redis get error: {e}")
            return None

    def set(self, key, value, ex=None):
        try:
            self.client.set(key, value, ex=ex)
        except Exception as e:
            print(f"Redis set error: {e}")

    def incr(self, key):
        try:
            return self.client.incr(key)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return None
