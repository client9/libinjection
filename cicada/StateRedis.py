#!/usr/bin/env python

import logging
import redis


class StateRedis(object):
    def __init__(self, prefix = 'cicada_', eventq = 'cicada_events'):
        self.connection = redis.Redis()
        self.eventq = 'cicada_events'
        self.prefix = prefix

    # list of projects
    def jobs_put(self, name):
        # to do timeout
        self.connection.sadd('cicada_jobs', name)
    def jobs_get_all(self):
        jobs = self.connection.smembers('cicada_jobs')
        if jobs is None:
            return []
        else:
            return jobs

    def job_get(self, name):
        return self.connection.hgetall('cicada_job_' + name)
    def job_set(self, name, data):
        self.connection.hmset('cicada_job_' + name, data)
    def job_set_key(self, name, key, value):
        self.connection.hset('cicada_job_' + name, key, value)

    # mini event queue
    def event_put(self, msg):
        logging.debug("Pushing %s:%s", self.eventq, msg)
        self.connection.rpush(self.eventq, msg)
    def event_get(self):
        return self.connection.lpop(self.eventq)
    def event_get_all(self, timeout=60):
        result = []
        while True:
            val = self.connection.lpop(self.eventq)
            logging.debug("Popping %s:%s", self.eventq, val)
            if val is None:
                return result
            result.append(val)

    # source control poller state
    #  i.e. last commit to a repo
    def poll_list_all(self):
        pass

    def poll_put(self, name, current, now):
        key = self.prefix + 'poll_' + name
        return self.connection.hmset(key, {
            'name': name,
            'current': current,
            'now': now
        })

    def poll_get(self, name):
        key = self.prefix + 'poll_' + name
        lastpoll = self.connection.hgetall(key)
        return lastpoll.get('current', None)
