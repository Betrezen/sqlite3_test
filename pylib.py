# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2014/03/01.
# copyright

def get_random_mac():
    import random
    return ':'.join(map(lambda x: "%02x" % x, [0x00,0x16,0x3e,random.randint(0x00, 0x7f),random.randint(0x00, 0xff),random.randint(0x00, 0xff)]))

def get_random_ip4():
    import random
    return ".".join(map(lambda x: str(random.randint(0,256)), [i for i in range(0,4)]))

def get_random_ip4net():
    import random
    return get_random_ip4()+"/"+str(random.choice([16,24]))

def get_random_uuid():
    import uuid
    import hashlib
    import os
    l = os.urandom(30).encode('base64')[:-1]
    return hashlib.sha256(l).hexdigest()

# decorator which print how many time were spend on fucntion
def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        #print func.__name__
        print(time.clock() - t)
        return res
    return wrapper

# decorator which counting call of function
def counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        res = func(*args, **kwargs)
        print("{0} invoked: {1}x times".format(func.__name__, wrapper.count))
        return res
    wrapper.count = 0
    return wrapper

