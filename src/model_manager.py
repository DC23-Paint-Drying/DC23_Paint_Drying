import json
import requests

class ModelManager:
    def __init__(self):
        self.useModel = True
        self.modelURL = "http://localhost:8080/engine-rest"
        self.process_instance_id = None

    def deploy_process(self):
        if self.useModel and self.process_instance_id is None:
            response = requests.post(self.modelURL+"/process-definition/key/BuyVideo/start", json={})
            response_dict = json.loads(response.text)
            self.process_instance_id = response_dict['id']

    def delete_process(self):
        if self.useModel and self.process_instance_id is not None:
            requests.delete(self.modelURL+"/process-instance/"+self.process_instance_id)
            self.process_instance_id = None

    
    def complete_user_task(self, data={}, end=False):
        if self.useModel and self.process_instance_id is not None:
            instance_info = requests.get(self.modelURL+"/task?processInstanceId="+self.process_instance_id)
            instance_info_dict = json.loads(instance_info.text)
            requests.post(self.modelURL+"/task/"+instance_info_dict[0]['id']+"/complete", json=data)
            if end:
                self.process_instance_id = None

    def lock_service_task(self, worker_id, topic_name):
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
            requests.post(self.modelURL+"/external-task/fetchAndLock", json=data).text
    
    def complete_service_task(self,worker_id, variables={}, end=False):
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