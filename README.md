# Personal_RAG
基于个人的私有数据，定制RAG问答系统

## 使用
### 环境准备
pip install -r requirement.txt
安装其它必要的安装包；

### 启动服务
```
python rag_api.py
或者
sh .\scripts\server_api.sh
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
当前版本的文档切片未做向量存于向量数据库、仅在本地文件中保存了切片信息；
### 切片说明：
1、当通过API请求传入新的文件路径时，上一次传递的文件提取的切片会被覆盖；如果文档未变、第一次请求传递文件路径、后续请求file_path可以传递空字符串"";
2、可以通过document_split.py文件首先对文档库切片之后；基于API做问答，此时API请求体不需要传递文件路径信息；

## 计划
    - 引入embedding模型对切片做语义提取、并保存至向量数据库；
    - 引入rerank模型做切片排序处理；
    - 支持其他文件格式；
    - 支持API更新切片数据，不会每次覆盖；
    - 支持更多LLM；

## License
本代码仓库仅为学习研究使用、禁止商用；