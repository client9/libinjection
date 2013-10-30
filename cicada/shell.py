import logging
import subprocess

class ExecuteShell(object):
    """
    Executes a bash script
    """
    def __init__(self, script):
        self.script = script

    def run(self, name):
        logging.info("Shell exec at {0}".format(name))
        p = subprocess.Popen(['/bin/bash', '-v', '-c', self.script],
                             cwd=name,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.STDOUT,
                             shell=False)
        (sout, serr) = p.communicate()

        return (sout, serr, p.returncode)
