import logging

class QueueNull(object):
    def __init__(self):
        pass

    def create(self, name):
        logging.info("Null Queue: creating {0}".format(name))

    def put(self, msg):
        logging.info("Null Queue: put {0}".format(msg))
        return True

    def get(self):
        logging.info("Null Queue: reading")
        return None

