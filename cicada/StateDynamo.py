#!/usr/bin/env python

import logging
import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, AllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

dynamo_schema = {
    'poll': {
        'schema': [
            HashKey('name')
        ]
    },
    'workers': {
        'schema': [
            HashKey('worker')
        ]
    },
    'project_job': {
        'schema': [
            HashKey('project'),
            RangeKey('job')
        ]
    },
    'job_history': {
        'schema': [
            HashKey('projectjob'),
            RangeKey('started', data_type=NUMBER)
        ]
    }
}

class StateDynamo(object):
    def __init__(self, region, prefix = 'cicada_'):
        self.prefix = prefix
        self.connection= boto.dynamodb2.connect_to_region(region)
        self.project_job = Table(prefix + 'project_job', connection=self.connection, **dynamo_schema['project_job'])
        self.job_history = Table(prefix + 'job_history', connection=self.connection, **dynamo_schema['job_history'])
        self.worker = Table(prefix + 'worker', connection=self.connection, **dynamo_schema['workers'])
        self.poll = Table(prefix + 'poll', connection=self.connection, **dynamo_schema['poll'])

    def tables_create(self):
        """
        Creates a new table.. throws exception if tables already exist
        """
        for table_name, schema in dynamo_schema.iteritems():
            logging.info("Creating " + self.prefix + table_name)
            Table.create(self.prefix + table_name, **schema)

    def tables_destroy(self):
        """
        """
        self.project_job.delete()
        self.job_history.delete()
        self.worker.delete()
        self.poll.delete()

    def tables_list(self):
        print self.connection.list_tables()['TableNames']


    def workers_list_all(self):
        return self.worker.scan()

    def workers_put(self, workerx, project, job, started):
        return self.worker.put_item(data={
            worker: workerx,
            job:"{0}.{1}".format(project, job),
            started:started}, overwrite=True)

    def projectjobs_list_all(self):
        """
        dumps all project/job states.
        """
        return self.project_job.scan()

    def projectjobs_list(self, projectname):
        """
        dumps all states for a given project
        """
        return self.project_job.scan(project__eq=projectname)

    def projectjobs_put(self, project, job, started, state, updated):
        """
        Designed for fast lookups of all projects.

        hash/range = (project, job)
        """
        self.project_job.put_item(data={
            'project': project,
            'job': job,
            'started': started,
            'state': state,
            'updated': updated
            }, overwrite=True)


    def jobhistory_put(self, project, job, started, state, updated):
        """
        combines project.job into one field for looking up history
        of a particular job.
        """
        self.job_history.put_item(data={
            'projectjob': '{0}.{1}'.format(project, job),
            'started': started,
            'state': state,
            'updated': updated
        }, overwrite=True)

    def poll_list_all(self):
        polls = self.poll.scan()
        return polls

    def poll_put(self, name, current, now):
        return self.poll.put_item(data={
            'name': name,
            'current': current,
            'now': now
        }, overwrite=True)

    def poll_get(self, name):
        lastpoll = self.poll.get_item(name=name)

        if lastpoll is None:
            return None
        else:
            return lastpoll['current']


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(process)d %(message)s")
    r = StateDynamo('us-west-2')

    r.tables_list()

    projects = {}
    for rs in r.projectjobs_list_all():
        job = {
            'project': str(rs['project']),
            'job': str(rs['job']),
            'start': int(rs['started']),
            'duration': int(rs['updated'] - rs['started']),
            'state': str(rs['state'])
        }
        if rs['project'] in projects:
            projects[rs['project']].append(job)
        else:
            projects[rs['project']] = [ job ]


    for k,v in projects.iteritems():
        print k
        for jobobj in v:
            print "   {job} {start} {duration} {state}".format(**jobobj)


    #r.create()
    #r.destroy()
    #print r.update_poll('foo', 'bar', 0)
    #print r.get_poll('foo')
