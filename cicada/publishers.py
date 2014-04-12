import logging
import os
import stat
import subprocess

class PublishArtifact(object):
    """
    Publish console ouput

    artifct is relative to workspace directory
    href/linktext is made for future linking
    """

    def __init__(self, artifact, destination, href, linktext):
        self.artifact = artifact
        self.destination = destination
        self.href = href
        self.linktext = linktext

    def link(self):
        return (self.href, self.linktext)

    def run(self, workspace, project, jobname, start):
        destdir = os.path.join(self.destination, project, jobname, str(start));
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        sourcedir = os.path.join(workspace, self.artifact)
        regular = False
        if (stat.S_ISREG == os.stat(sourcedir).st_mode):
            regular = True
            destdir = os.path.join(destdir, self.destination)
        logging.info('Copying {0} to {1}'.format(sourcedir, destdir))


        
        # creates an empty file if it's missing
        # works if directory or regular file
        subprocess.call(['touch', '-a', sourcedir])

        if regular:
            subprocess.call(['cp', sourcedir, destdir])
        else:
            subprocess.call(['cp', '-r', sourcedir, destdir])

        # portable? link to latest
        latestdir = os.path.join(self.destination, project, jobname, 'latest');
        subprocess.call(['rm', '-rf', latestdir])
        subprocess.call(['ln', '-s', destdir, latestdir])
        return destdir
