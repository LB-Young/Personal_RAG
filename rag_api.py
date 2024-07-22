from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr, confloat
from uvicorn import Server, Config
from personal_rag.document_split.document_extractor import DocumentExtractor
from personal_rag.rag.rag_handler import RAG_Handler
from personal_rag.rag.utils.entities import QueryEntity

app = FastAPI()

class ChatParams(BaseModel):
    file_path: constr()
    query: constr()
    temperature: confloat()

@app.post("/chat")
def chat(request:Request, chat_params:ChatParams):
    query_entity = QueryEntity()
    query_entity.requests_param_extract(chat_params)
    if len(chat_params.file_path) != 0:
        file_path = chat_params.file_path
        res = DocumentExtractor(file_path).do_extract()
        if res:
            print("documents extract finished!")
    rag_handler = RAG_Handler(query_entity)
    response_entity = rag_handler.ado()
    
    response_body = {
        "answer":response_entity.answer
    }
    return JSONResponse(response_body)


if __name__ == "__main__":
    server_config = Config(
        app=app,
        host='127.0.0.1',
        port=8013,
    )
    Server(server_config).run()