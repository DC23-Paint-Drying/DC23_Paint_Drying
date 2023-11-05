import json
import requests

class ModelManager:
    def __init__(self):
        self.useModel = False
        self.modelURL = "http://localhost:8080/engine-rest"
        self.process_instance_id = None

    def deploy_process(self):
        if self.useModel and self.process_instance_id is None:
            response = requests.post(self.modelURL+"/process-definition/key/BuyVideo/start", json={})
            response_dict = json.loads(response.text)
            self.process_instance_id = response_dict['id']
    
    def complete_task(self, data={}, end=False):
        if(self.useModel):
            instance_info = requests.get(self.modelURL+"/task?processInstanceId="+self.process_instance_id)
            instance_info_dict = json.loads(instance_info.text)
            requests.post(self.modelURL+"/task/"+instance_info_dict[0]['id']+"/complete", json=data)
            if end:
                self.process_instance_id = None