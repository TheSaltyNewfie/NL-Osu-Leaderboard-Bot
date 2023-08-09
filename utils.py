'''
I am putting everything that is not command related into this file to make things a bit cleaner
'''
import os
from ossapi import Ossapi
import json
import db.sql_interaction as osudb
import redis
import time

api = Ossapi(os.environ.get("CLIENT_ID"), os.environ.get("CLIENT_SECRET"))

r = redis.Redis(host="192.168.4.35", port=6379, db=0)

def get_rank(id):
    key = f"rank:{id}"

    if r.exists(key):
        rank, pp_amnt, timestamp = r.hmget(key, 'rank', 'pp_amnt', 'timestamp')
        timestamp = float(timestamp)
        print(f"Keys exists for {id}.")

        if time.time() - timestamp > 3600:
            print(f"Time is longer than 1 hour for {id}.")
            try:
                user = api.user(id)
                rank = user.rank_history.data[-1]
                pp_amnt = user.statistics.pp
                if pp_amnt != 0:
                    print("Setting keys.")
                    r.hset(key, 'rank', rank)
                    r.hset(key, 'pp_amnt', pp_amnt)
                    r.hset(key, 'timestamp', time.time())
                    return rank
                else:
                    return None

            except AttributeError as error:
                return None
        else:
            return int(rank) if pp_amnt != 0 else None

    try:
        print(f"No key was returned for {id}.")
        rank = api.user(id).rank_history.data[-1]
        pp_amnt = api.user(id).statistics.pp
        if pp_amnt != 0:
            print(f"Setting keys for {id}.")
            r.hset(key, 'rank', rank)
            r.hset(key, 'pp_amnt', pp_amnt)
            r.hset(key, 'timestamp', time.time())
            return rank
        else:
            return None
    except AttributeError as error:
        return None
