# Personal_RAG
基于个人的私有数据，定制RAG问答系统

## 使用
### 环境准备
pip install -r requirement.txt
安装其它必要的安装包；

### 启动服务
```
python rag_api.py
```

### 服务调用
python ./test/rag_test.py
```
import requests
import json
url = "http://127.0.0.1:8013/chat"
request_body = {
    "file_path": "./test/模型量化.pdf",
    "query": "介绍一下AWQ",
    "temperature": 1.0
}
response = requests.post(url, data=json.dumps(request_body))
response.encoding = 'utf-8'
print(response.text)
```
参数说明：
"file_path": 文档源（用于召回），可以为单个文件或者文件夹；
"query": 输入问题；
"temperature": 1.0（当前参数未起作用，可以传任意浮点数）；


## 支持文档格式
docx、pdf、或者仅包含这两种后缀的文件夹；
说明：
当请求传入新的文件路径时，上一次传递的文件提取的切片会被覆盖；如果文档未变、第一次请求传递文件路径、后续请求file_path可以传递空字符串"";

## License
本代码仓库仅为学习研究使用、禁止商用；