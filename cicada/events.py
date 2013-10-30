import datetime

class TestOnEvent(object):
    def __init__(self, event):
        self.event = event
    def run(self, now, events):
        return self.event in events

class TestOnInterval(object):
    def __init__(self, minutes=10):
        self.interval = minutes * 60
        self.last = 0

    def run(self, now, events):
        if (now - self.last) > self.interval:
            self.last = now
            return True
        return False

class TestOnQueue(object):
    def __init__(self, name):
        self.name = name
    def run(self, now, events):
        pass
        # do AWS queue check

class TestOnTime(object):

    @staticmethod
    def parse_cronstring(pattern, rmax):
        if pattern == '*':
            return range(rmax)
        values = set()
        for parts in pattern.split(','):
            arange = [ int(i.strip()) for i in parts.split('-') ]
            if len(arange) == 1:
                values.add(arange[0])
            else:
                for i in range(arange[0], arange[1]):
                    values.add(i)
        ints = list(values)
        sorted(ints)
        return ints

    def __init__(self, minute='*', hour='*', dayofmonth='*', weekday='*'):
        self.minute     = TestOnTime.parse_cronstring(minute, 60)
        self.hour       = TestOnTime.parse_cronstring(hour, 24)
        self.dayofmonth = TestOnTime.parse_cronstring(dayofmonth, 32)
        self.weekday    = TestOnTime.parse_cronstring(weekday, 8)

    def run(self, now, events):
        now = datetime.datetime.utcnow()
        return now.minute in self.minute and \
            now.hour in self.hour and \
            now.day in self.dayofmonth and \
            now.weekday() in self.weekday

