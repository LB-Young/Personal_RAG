import requests
import json

url = "http://127.0.0.1:8013/chat"

request_body = {
    "file_path": r"C:\Users\86187\Desktop\test\模型量化.pdf",
    "query": "介绍",
    "temperature": 1.0
}

response = requests.post(url, data=json.dumps(request_body))

response.encoding = 'utf-8'
print(response.text)