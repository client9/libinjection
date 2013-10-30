

class PollHG(object):
    def __init__(object, repo, interval, binexe='hg'):
        self.repo = repo
        self.last = 0
        self.interval = interval * 60
        self.binexe = binexe

    def run(self, now):
        if (now - self.last) < self.interval:
            return False
        args = [self.binexe, 'log', '-l', '1', '--incremental',  self.repo]

class PollSVN(object):
    def __init__(self, repo, interval):
        self.repo = repo
        self.last = 0
        self.interval = interval * 60

    def run(self, now):
        if (now - self.last) < self.interval:
            return False
        args = ['svn', 'log', '-l', '1', '--incremental',  self.repo]

class PollGit(object):
    def __init__(self, repo, interval, branch='HEAD'):
        self.repo = repo
        self.last = 0
        self.interval = interval * 60
        self.branch = branch

    def run(self, now):
        if (now - self.last) < self.interval:
            return False
        args = ['git', 'ls-remote', self.repo, self.branch]



