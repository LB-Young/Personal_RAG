import requests
import json

url = "http://127.0.0.1:8013/retrival"

request_body = {
    "file_path": "",
    "need_embedding":True,
    "db_name":"tmp",
    "db_type":"local",
    "query": "结构化抽取是什么意思",
    "temperature": 1.0
}

response = requests.post(url, data=json.dumps(request_body))

response.encoding = 'utf-8'
print(response.text)