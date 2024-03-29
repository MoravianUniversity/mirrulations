import redis


class BusyRedis():
    """
    Stub for testing in place of a Redis server that is busy loading the data
    to memory, ping raises a BusyLoadingError
    """
    def ping(self):
        raise redis.BusyLoadingError


class InactiveRedis():
    """
    Stub for testing in place of an active Redis server,
    ping raises a ConnectionErrorException
    """
    def __init__(self):
        self.dict = {}

    def ping(self):
        raise redis.ConnectionError

    def incr(self, key):
        if key in self.dict:
            self.dict[key] += 1

    def decr(self, key):
        if key in self.dict:
            self.dict[key] -= 1

    def exists(self, key):
        return key in self.dict

    def get(self, key):
        return self.dict[key]

    def set(self, key, value):
        self.dict[key] = value


class ReadyRedis():
    """
    Stub for testing in place of an active Redis server,
    ping replies with true
    """
    def __init__(self):
        self.dict = {}

    def ping(self):
        return True

    def incr(self, key):
        if key in self.dict:
            self.dict[key] += 1

    def decr(self, key):
        if key in self.dict:
            self.dict[key] -= 1

    def exists(self, key):
        return key in self.dict

    def get(self, key):
        return self.dict[key]

    def set(self, key, value):
        self.dict[key] = value

    def hset(self, key, value1, value2):
        self.dict[key] = [value1, value2]

    def hdel(self, key, value):
        self.dict.pop(key, value)


class MockRedisWithStorage():
    """
    Mock for testing in place of an active Redis server that has storage
    """
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        if key is None:
            self.data[key] = int(0)
        self.data[f'{key}'] = value

    def ping(self):
        return True

    def exists(self, key):
        return key in self.data

    def get(self, key):
        return self.data[f'{key}']

    def incr(self, key):
        try:
            self.data[key] += 1
        except KeyError:
            # self.data.set(key, 0)
            self.data[key] = 0
            self.data[key] += 1

    def decr(self, key):
        try:
            self.data[key] -= 1
        except KeyError:
            # self.data.set(key, 0)
            self.data[key] = 0
            self.data[key] -= 1

    def lpush(self, key, val):
        try:
            self.data[key] = [val]+self.data[key]
        except KeyError:
            self.data[key] = []
            self.data[key] = [val]+self.data[key]
