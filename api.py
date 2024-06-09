import os
import json 
import logging
from enum import Enum
from urllib import request
from urllib.error import HTTPError

class Mode(Enum):
    CREATE = "create"
    READALL = "retrieve"
    READ = "retrieveByNameType"
    UPDATE = "editByNameType"
    DELETE = "deleteByNameType"
    
    def __str__(self):
        return self.value
    
class PorkBunAPI():
    def __init__(self, domain="", config_file="config.json", log_file="porkbun.log"):
        self.logger = logging.getLogger("PorkBunAPI")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        for handler, level in ((logging.FileHandler(log_file), logging.DEBUG),
                               (logging.StreamHandler(), logging.INFO)):
            handler.setLevel(level)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.info(f"{domain} initialized using {os.path.abspath(config_file)}")
        self.domain = domain
        with open(config_file) as f:
            self.config = json.load(f)
            
    def _api(self, target="ping", data=None):
        data = data or self.config
        req = request.Request(self.config["endpoint"]+"/"+target)
        req.data = json.dumps(data).encode("utf-8")
        try:
            response = request.urlopen(req, timeout=10).read()
        except HTTPError as err:
            self.logger.error(f"{str(err)}")
            self.logger.error(f"Url : {err.url}")
            self.logger.error(f"Data: {str(data)}")
            raise err
        return json.loads(response.decode("utf-8"))
            
    def ping(self):
        return self._api("ping")["yourIp"]
    
    def get_records(self):
        self.logger.info(f"Getting records for {self.domain}")
        target = f'dns/{Mode.READALL}/{self.domain}'
        return self._api(target)["records"]
    
    def set_record(self, type, name, content, ttl=600):
        record = self.read_record(type, name)
        if record:
            if record["content"] == content: return {'status': 'No Change were made'}
            return self.update_record(type, name, content, ttl)
        else:
            return self.create_record(type, name, content, ttl)
        
    def create_record(self, type, name, content, ttl):
        self.logger.info(f"Creating {type} record for {name+'.' if name else ''}{self.domain} pointing to {content}")
        target = f'dns/{Mode.CREATE}/{self.domain}'
        return self._api(target=target, data={
            "apikey": self.config["apikey"],
            "secretapikey": self.config["secretapikey"],
            "type": type,
            "name": name,
            "content": content,
            "ttl": str(ttl)
        })
        
    def read_record(self, type, name):
        self.logger.info(f"Reading {type} record of {name+'.' if name else ''}{self.domain}")
        target = f'dns/{Mode.READ}/{self.domain}/{type}/{name}'
        records = self._api(target=target)["records"]
        return records[0] if records else None
        
    def update_record(self, type, name, content, ttl):
        self.logger.info(f"Updating {type} record of {name+'.' if name else ''}{self.domain} pointing to {content}")
        target = f'dns/{Mode.UPDATE}/{self.domain}/{type}/{name}'
        return self._api(target=target, data={
            "apikey": self.config["apikey"],
            "secretapikey": self.config["secretapikey"],
            "content": content,
            "ttl": str(ttl)
        })
        
    def delete_record(self, type, name):
        self.logger.info(f"Deleting {type} record from {name+'.' if name else ''}{self.domain}")
        target = f'dns/{Mode.DELETE}/{self.domain}/{type}/{name}'
        return self._api(target=target)