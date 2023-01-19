import uuid
import time
from django.core.cache import cache


class CacheLock(object):
    def __init__(self, lock_key: str, expires: int = 1 * 60 * 60, wait_timeout: int = 10, retry_interval: float = 0.1):
        self.cache = cache
        self.expires = expires  # 函数执行超时时间
        self.wait_timeout = wait_timeout  # 拿锁等待超时时间
        self.retry_interval = retry_interval
        self.lock_key = lock_key
        self.identifier = f"{uuid.uuid4()}"

    def acquire_lock(self) -> bool:
        # 获取cache锁
        while self.wait_timeout >= 0:
            if self.cache.add(self.lock_key, self.identifier, self.expires):
                return True
            time.sleep(self.retry_interval)
            self.wait_timeout -= self.retry_interval
        return False

    def release_lock(self) -> bool:
        # 释放cache锁
        lock_value = self.cache.get(self.lock_key)
        if lock_value == self.identifier:
            self.cache.delete(self.lock_key)
        return True
