#!/usr/bin/python
# -*- encoding=utf-8 -*-


import os
import time
import django

from django.core.cache import cache

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


def basic_use():
    s = 'Hello World, Hello Django Cache.'
    cache.set('key', s)
    cache_result = cache.get('key')
    print(cache_result)
    s2 = 'Hello World, Hello Django Timeout Cache.'
    cache.set('key2', s2, 5)
    cache_result = cache.get('key2')
    print(cache_result)
    time.sleep(5)
    cache_result = cache.get('key2')
    print(cache_result)
    pass


if __name__ == '__main__':
    basic_use()
