import os
import json

class configHelper(object):

    def __new__(self):
        if not hasattr(self,"instance"):
            self.instance = super(configHelper,self).__new__(self)
            print("creando")
            self.root_path = "/".join(os.path.abspath(__file__).split("/")[:-2])
            path_to_config_file = self.root_path+"/config.json"
            file = open(path_to_config_file)
            self.config = json.load(file)
            file.close()
        return self.instance

    def get_dataset_path(self)->str:
        return f"{self.root_path}/{self.config.get('DatasetPath')}"

    def get_datamarket_path(self)->str:
        return f"{self.root_path}/{self.config.get('DataMarketPath')}"
    
    def get_context_path(self)->str:
        return f"{self.root_path}/{self.config.get('ContextPath')}"

    def get_mtg_api_card(self)->str:
        return self.config.get("mtgApi_card")