# -*- coding: UTF-8 -*-

import time
import redis

# 获取锁
def get_lock(uid):
    # 链接redis
    r = redis.StrictRedis(host='192.168.11.131', port=6379, db=0, socket_timeout=1, socket_connect_timeout=3)

    # 当前时间戳，用户删除锁时check
    sec = str(time.time())

    # 处理超时时间
    timeout = 300

    # 试图锁住uid
    while True:
        res = r.set(uid, sec, ex=timeout, nx=True)
        if res == True:
            print('Get lock succeed, return')
            return True, sec
        else:
            print('Get lock failed, lock exist, wait')
            time.sleep(1)
    return False, None

# 释放锁
def del_lock(uid, sec):
    # 链接redis
    r = redis.StrictRedis(host='192.168.11.131', port=6379, db=0, socket_timeout=1, socket_connect_timeout=3)

    # 校验
    redis_sec = r.get(uid)
    if sec != redis_sec:
        print('check permission failed: %s' % uid)
        return False
    print('check permission succeed : %s' % uid)

    # 删除
    res = r.delete(uid)
    if res:
        print("del key success : %s" % uid)
        return False
    else:
        print('def key failed : %s' % uid)
        return True

if __name__ == '__main__':
    uid = '001'
    while True:
        status, sec = get_lock(uid)
        if status:
            del_lock(uid, sec)
        time.sleep(1)