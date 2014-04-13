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
            logging.info("Making destination directory of %s", destdir)
            os.makedirs(destdir)

        sourcedir = os.path.join(workspace, self.artifact)

        # create empty file if it doesnt exist
        # this works for files and directories
        if not os.path.exists(sourcedir):
            subprocess.call(['touch', '-a', sourcedir])

        if (stat.S_ISREG(os.stat(sourcedir).st_mode)):
            destfile = os.path.join(destdir, self.href)   
            logging.info('Copying file %s to %s', sourcedir, destfile)
            subprocess.call(['cp', sourcedir, destdir])
        else:
            logging.info('Copying directory %s to %s', sourcedir, destdir)
            subprocess.call(['cp', '-r', sourcedir, destdir])

        # portable? link to latest
        latestdir = os.path.join(self.destination, project, jobname, 'latest');
        subprocess.call(['rm', '-rf', latestdir])
        subprocess.call(['ln', '-s', destdir, latestdir])
        return destdir
