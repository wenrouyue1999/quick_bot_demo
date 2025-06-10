#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/23 下午10:49
# @Author  : wenrouyue
# @File    : redis_utils.py
import redis
from import_utils import *

config = load_config()
from log.logger import LoggerConfig

log = LoggerConfig(__name__).get_logger()


# noinspection PyDeprecation
class RedisUtil:
    def __init__(self, host=None, port=None, password=None, db=None):
        self.redis = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True
        )
        # todo 初始化admin 如果没有则不需要
        self.sadd(config["redisKey"]["adminList"], config["redisKey"]["adminId"])

    def _decode(self, value):
        """Helper method to decode bytes to string."""
        if isinstance(value, bytes):
            return value.decode('utf-8')
        return value

    def hset(self, redis_key, key, value):
        return self.redis.hset(redis_key, key, value)

    def hmset(self, redis_key, values):
        return self.redis.hmset(redis_key, values)

    def hmget(self, redis_key, *values):
        results = self.redis.hmget(redis_key, *values)
        return [self._decode(result) for result in results]

    def keys(self, redis_key):
        return self.redis.keys(redis_key)

    def hget(self, redis_key, key):
        return self._decode(self.redis.hget(redis_key, key))

    def hgetall(self, redis_key):
        results = self.redis.hgetall(redis_key)
        return {self._decode(k): self._decode(v) for k, v in results.items()}

    def hdel(self, redis_key, key):
        return self.redis.hdel(redis_key, key)

    def set(self, redis_key, value):
        return self.redis.set(redis_key, value)

    def set_by_time(self, redis_key, value, time):
        return self.redis.set(redis_key, value, ex=time)

    def lrange(self, redis_key, start_index, end_index):
        results = self.redis.lrange(redis_key, start_index, end_index)
        return [self._decode(result) for result in results]

    def delete(self, redis_key):
        return self.redis.delete(redis_key)

    def get(self, redis_key):
        return self._decode(self.redis.get(redis_key))

    def rpush(self, redis_key, *data):
        return self._decode(self.redis.rpush(redis_key, *data))

    def lpop(self, redis_key):
        return self._decode(self.redis.lpop(redis_key))

    def llen(self, redis_key):
        return self._decode(self.redis.llen(redis_key))

    def sadd(self, redis_key, value):
        return self.redis.sadd(redis_key, value)

    def smembers(self, redis_key):
        results = self.redis.smembers(redis_key)
        return {self._decode(member) for member in results}

    def ltrim(self, redis_key, start_index, end_index):
        return self.redis.ltrim(redis_key, start_index, end_index)

    def srem(self, redis_key, value):
        return self.redis.srem(redis_key, value)

    # def save_json_redis(self, hash_key, json_data):
    #     pipeline = self.redis.pipeline()
    #     for key, value in json_data.items():
    #         pipeline.hset(hash_key, key, value)
    #     return pipeline.execute()

    def save_json_redis(self, hash_key, json_data):
        pipeline = self.redis.pipeline()
        for key, value in json_data.items():
            if value is not None:  # 仅当值不为 None 时存储
                pipeline.hset(hash_key, key, value)
        return pipeline.execute()

    def hincrby(self, hash_key, field, increment=1):
        try:
            new_value = self.redis.hincrby(hash_key, field, increment)
            log.info("自增 '%s'  key '%s' %d", field, hash_key, new_value)
            return new_value
        except Exception as error:
            log.info('Error incrementing hash field: %s', error)

    def decrby(self, hash_key, field):
        try:
            new_value = self.redis.hincrby(hash_key, field, -1)
            log.info("扣除 '%s'  key '%s' %d", field, hash_key, new_value)
            return new_value
        except Exception as error:
            log.info('Error incrementing hash field: %s', error)

    def sismember(self, key, value):
        return self.redis.sismember(key, value)

    def incr(self, cache_key):
        return self.redis.incrby(cache_key, 1)

    def expire(self, key, RATE_LIMIT_WINDOW):
        return self.redis.expire(key, RATE_LIMIT_WINDOW)

    def exists(self, key):
        return self._decode(self.redis.exists(key))

    def find_all_key(self, key):
        cursor = 0
        report_keys = {}

        # 使用 SCAN 找到所有匹配的键
        while True:
            cursor, keys = self.redis.scan(cursor, match=f"{key}*")
            for k in keys:
                # 获取每个哈希键的全部字段和值
                report_keys[self._decode(k)] = self.hgetall(k)

            # 如果游标为0，表示扫描完成
            if cursor == 0:
                break

        return report_keys
