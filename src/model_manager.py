import json
import requests

class ModelManager:
    def __init__(self):
        """
        Creates the ModelManager object

        If you are not eunning camunda server set self.useModel to False
        """
        self.useModel = True
        self.modelURL = "http://localhost:8080/engine-rest"
        self.process_instance_id = None

    def deploy_process(self):
        """
        Deployes process to camunda server

        """
        if self.useModel and self.process_instance_id is None:
            response = requests.post(self.modelURL+"/process-definition/key/BuyVideo/start", json={})
            response_dict = json.loads(response.text)
            self.process_instance_id = response_dict['id']

    def delete_process(self):
        """
        Deleates current process

        """
        if self.useModel and self.process_instance_id is not None:
            requests.delete(self.modelURL+"/process-instance/"+self.process_instance_id)
            self.process_instance_id = None

    
    def complete_user_task(self, data=None, end=False):
        """
        Completes current task. It has to be a user task.

        :param data: json data that will be sent in Post request
        :param end: boolean that specifies whether it is last task of the process.

        """
        if data is None:
            data = {}
        if self.useModel and self.process_instance_id is not None:
            instance_info = requests.get(self.modelURL+"/task?processInstanceId="+self.process_instance_id)
            instance_info_dict = json.loads(instance_info.text)
            requests.post(self.modelURL+"/task/"+instance_info_dict[0]['id']+"/complete", json=data)
            if end:
                self.process_instance_id = None

    def lock_service_task(self, worker_id, topic_name):
        """
        Assignes and lockes worker to service task

        :param worker_id: id of worker that is responsible for this task
        :param topic_name: topic of task set in camunda model
        """
        if self.useModel and self.process_instance_id is not None:
            data = {
                "workerId": worker_id,
                "maxTasks": 1,
                "topics": [
                    {
                    "topicName": topic_name,
                    "lockDuration": 600000
                    }
                ]
            }
            requests.post(self.modelURL+"/external-task/fetchAndLock", json=data)
    
    def complete_service_task(self,worker_id, variables=None, end=False):
        """
        Completes current task. It has to be a service task.

        :param variables: json data that will be sent in Post request on varables field
        :param end: boolean that specifies whether it is last task of the process.

        """
        if variables is None:
            variables = {}
        if self.useModel and self.process_instance_id is not None:
            instance_info = requests.get(self.modelURL+"/external-task?processInstanceId="+self.process_instance_id)
            instance_info_dict = json.loads(instance_info.text)
            data = {
                "workerId": worker_id,
                "variables": variables
            }
            requests.post(self.modelURL+"/external-task/"+instance_info_dict[0]['id']+"/complete", json=data)
            if end:
                self.process_instance_id = None