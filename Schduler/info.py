import math
import boto3


def init():
    
    global _deploy
    _deploy.update(sqs=SqsDeploy(), noop=NoOpDeploy())


def get(deploy_name):
    return _deploy.get(deploy_name, _deploy['noop'])


class NoOpDeploy:

    def task_count(self, job_data):
        return job_data['taskCount']


class SqsDeploy:

    def __init__(self):
        self._sqs = boto3.resource('sqs')

    def task_count(self, job_data):
       
        queue = self._sqs.get_queue_by_name(
            QueueName=job_data['deploy']['queueName']
        )
        task_count = queue.attributes['current']
        if task_count > 0:
            return self.Tcal(task_count, job_data)
        else:
            return 0
    def Tcal(self, task_count, job_data):
       job_data['task_count'].update('T_Cold')=math.ceil((job_data['task_count'].get('Payload')/job_data['unit'].get('Payload'))*job_data['unit'].get('unit_cold'))
       job_data['task_count'].update('T_Exec')=math.ceil((job_data['task_count'].get('Source')/job_data['unit'].get('Source'))*job_data['unit'].get('unit_source')+(job_data['task_count'].get('Ninput')/job_data['unit'].get('Ninput'))*job_data['unit'].get('unit_Ninput'))


        


        