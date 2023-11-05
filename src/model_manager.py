import json
import requests

useModel = False
modelURL = "http://localhost:8080/engine-rest"
process_instance_id = None

class ModelManager:
    def deploy_process():
        global process_instance_id
        if useModel and process_instance_id is None:
            response = requests.post(modelURL+"/process-definition/key/BuyVideo/start", json={})
            response_dict = json.loads(response.text)
            process_instance_id = response_dict['id']
    
    def complete_task(data={},end=False):
        global process_instance_id
        if(useModel):
            instance_info = requests.get(modelURL+"/task?processInstanceId="+process_instance_id)
            instance_info_dict = json.loads(instance_info.text)
            requests.post(modelURL+"/task/"+instance_info_dict[0]['id']+"/complete", json=data)
            if end:
                process_instance_id = None