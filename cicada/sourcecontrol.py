import logging
import os
import subprocess
import time

class CheckoutSVN(object):
    """
    """
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def run(self, workspace):
        co = os.path.join(workspace, self.name)
        if os.path.exists(co):
            cmd = ['svn', 'update']
            cwd = co
            logging.info("{0}: SVN update from {1}".format(self.name, self.url))
        else:
            cmd = ['svn', 'co', self.url, self.name]
            cwd = workspace
            logging.info("{0}: SVN checkout (from {1})".format(self.name, self.url))

        logging.info("Executing: {0}".format( ' '.join(cmd)))

        p = subprocess.Popen(cmd,
                             cwd=cwd,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT)

        (sout,serr) = p.communicate()
        return (sout,serr,p.returncode)

class CheckoutGit(object):
    """
    does a pull or clone from a git repo as needed
    """

    def __init__(self, url, name):
        self.url = url
        self.name = name

    def run(self, workspace):
        co = os.path.join(workspace, self.name)
        if os.path.exists(co):
            cmd = ['git', 'pull']
            cwd = co
            logging.info("git pull {0} {1} at {2}".format(self.url, self.name, cwd))
        else:
            cwd = workspace
            cmd = ['git', 'clone', '--depth', '1', self.url, self.name]
            logging.info("git clone {0} {1} at {2}".format(self.url, self.name, cwd))

        p = subprocess.Popen(cmd,
                             cwd=cwd,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT)
        (sout,serr) = p.communicate()
        if sout is None:
            sout = ''
        if serr is None:
            serr = ''

        cmd = ['git', 'log', '-1', '--oneline']
        p = subprocess.Popen(cmd,
                             cwd=cwd,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT)

        (sout2, serr2) = p.communicate()
        if sout2 is None:
            sout2 = ''
        if serr2 is None:
            serr2 = ''

        # append output, but use first return code
        return (sout + sout2, serr + serr2, p.returncode)



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
    def __init__(self, name, repo, queue):
        self.repo = repo
        self.last = 0
        self.db = queue
        self.name = name

    def run(self, workspace):
        """
------------------------------------------------------------------------
r360 | nickg@client9.com | ... etc
"""

        current = self.db.poll_get(self.name)
        logging.info("SVN Poll for {0} with {1}: reading {2}".format(self.name, current, self.repo))

        args = ['svn', 'log', '-l', '1', '--incremental',  self.repo]
        p = subprocess.Popen(args,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT,
                             cwd=workspace,
                             shell=False)
        (sout, serr) = p.communicate()
        if p.returncode == 0:
            lines = sout.split()
            rev = lines[1].split('|')[0].strip()
            if rev != current:
                logging.info("Got update for {0} with {1}".format(self.name, rev))
                self.db.poll_put(self.name, rev, int(time.time()))
                self.db.event_put(self.name)
        return (sout, serr, p.returncode)

class PollGit(object):
    def __init__(self, name, repo, eventq, branch='HEAD'):
        self.name = name
        self.repo = repo
        self.branch = branch
        self.db = eventq

    def run(self, now):
        current = self.db.poll_get(self.name)
        logging.info("Git Poll for {0} with {1}: reading {2}".format(self.name, current, self.repo))
        args = ['git', 'ls-remote', self.repo, self.branch]
        p = subprocess.Popen(args,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT,
                             shell=False)
        (sout, serr) = p.communicate()
        if p.returncode == 0:
            rev = sout.split()[0]
            if rev != current:
                logging.info("Got update for {0} with {1}".format(self.name, rev))
                self.db.poll_put(self.name, rev, int(time.time()))
                self.db.event_put(self.name)
            else:
                logging.info("Git revision for {0} unchanged with {1}".format(self.name, rev))

        return (sout, serr, p.returncode)
