# PorkBun API

Porkbun API to change dns using built in python library
based on this https://porkbun.com/api/json/v3/documentation

## Requirement
- Porkbun api key and secret key 
- Python

## Getting Started
1. Clone this repo,
2. Getting porkbun api key, you can just follow along this link here https://porkbun.com/account/api
3. Put the secret key and api key in the config.json
```
{
    "endpoint": "https://porkbun.com/api/json/v3",
    "apikey": "pk1_api_key_here",
    "secretapikey": "sk1_secret_api_key_here"
}
```
4. Write simple command for your domain
```
from api import PorkBunAPI

porkbun = PorkBunAPI(domain="example.com")
myIp = porkbun.ping()
for subdomain in ("", "www"):
    status = porkbun.set_record("A", subdomain, myIp)
```

## Initializing API
```python
porkbun = PorkBunAPI("example.com", config_file="~/porkbun.json", log_file="~/porkbun.log")
```
PorkBunAPI take 3 parameter for initialization
1. domain
2. config_file containing api key and secret key
3. log_file for writing log

## Commands
```python
from api import PorkBunAPI

porkbun = PorkBunAPI(domain="example.com")
my_ip = porkbun.ping()
print(my_ip)

new_record = porkbun.create_record("A", "www", "8.8.8.8", ttl=600)    
print(new_record)
record = porkbun.read_record("A", "www")
print(record)
update = porkbun.update_record("A", "www", "1.1.1.1")
print(update)
delete = porkbun.delete_record("A", "www")
print(delete)

# Read all available records
records = porkbun.get_records()
for record in records:
    print(records)

# set_record use read_record, update_record, and create_record
for subdomain in ("", "www"):
    status = porkbun.set_record("A", subdomain, my_ip)
```

1. ping : get your current IP address
2. get_records : get all records for the domain
3. set_record : set record for the domain, if record already exist will update, if not will create a new one
4. create_record : create a new record
5. read_record : read one record from the domain
6. update_record : update an existing record
7. delete_record : delete an existing record

