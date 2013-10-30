import boto.sqs
from boto.sqs.message import Message

class QueueAWS(object):
    def __init__(self, queuename, region, keyid=None, secret=None, timeout=30):
        conn = boto.sqs.connect_to_region(region)
        self.q = conn.create_queue(queuename, timeout)

    def put(self, msg):
        m = Message()
        m.set_body(msg)
        return self.q.write(m)

    def get_all(self, timeout=60):
        values = []
        rs = self.q.get_messages(visibility_timeout=60)
        for r in rs:
            values.append(r.get_body())
            r.delete()
        return values

    def get(self, visibility=60):
        m = self.q.read(visibility)
        if m is None:
            return None
        else:
            msg = m.get_body()
            self.q.delete_message(m)
            return msg
