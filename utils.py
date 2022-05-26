from random import randint
from datetime import datetime
from numpy.random import choice

def gen_random_ip():
    a = randint(1, 254)
    b = randint(1, 254)
    c = randint(1, 254)
    d = randint(1, 254)

    return "%d.%d.%d.%d" % (a, b, c, d)

def create_os_port():
    return randint(49901, 65535)

def gen_wellknown_service_port():
    p = [
            {
                "port": 21,
                "protocol": "tcp"
            },
            {
                "port": 22,
                "protocol": "tcp"
            },
            {
                "port": 25,
                "protocol": "tcp"
            },
                {
                "port": 53,
                "protocol": "udp"
            },
            {
                "port": 80,
                "protocol": "tcp"
            },
            {
                "port": 123,
                "protocol": "udp"
            },
            {
            "port": 161,
            "protocol": "udp"
            },
            {
                "port": 443,
                "protocol": "tcp"
            },
            {
                "port": 1521,
                "protocol": "tcp"
            },
            {
                "port": 3306,
                "protocol": "tcp"
            },
            {
                "port": 7000,
                "protocol": "tcp"
            },
            {
                "port": 7070,
                "protocol": "tcp"
            },
            {
                "port": 7079,
                "protocol": "tcp"
            },
            {
                "port": 8000,
                "protocol": "tcp"
            },
            {
                "port": 8080,
                "protocol": "tcp"
            },
            {
                "port": 27017,
                "protocol": "tcp"
            }
        ]
    sz = len(p)
    idx = randint(0, sz-1)

    return p[idx]["port"], p[idx]["protocol"]

def get_current_time():
    now = datetime.now()
    time = now.strftime('%Y-%m-%d %H:%M:%S')

    return time

def weighted_choice(s):
    l, w = s
    c = choice(l, p=w)

    return c

