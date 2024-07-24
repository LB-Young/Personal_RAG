import chromadb
from chromadb.config import Settings
import json

class ChromadbClient:
    def __init__(self):
        # self.client = chromadb.Client()
        # self.local_db = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_data"))
        self.local_db = chromadb.Client()

    def create_db(self, db_name, slices):
        collection = self.local_db.create_collection(name=db_name)

        for slice in slices:
            embedding = slice['embedding']
            del slice['embedding']            
            collection.add(embeddings=embedding, metadatas=slice, ids=slice['id'])
        self.local_db.persist()
        with open("F:\Cmodels\Personal_RAG\personal_rag\slice_database\chroma_database\chromadb_mapping.json", "rw", encoding="utf-8") as f:
            all_dbs = json.load(f)
            all_dbs[db_name] = f"{db_name}.chroma"
            json.dump(all_dbs, f)
        self.local_db = chromadb.Database()
        return "{db_name} finished!"

    def collection_add_slice(self, db_name, slices):
        with open("F:\Cmodels\Personal_RAG\personal_rag\slice_database\chroma_database\chromadb_mapping.json", "r", encoding="utf-8") as f:
            all_dbs = json.load(f)
        if db_name not in all_dbs.keys():
            return self.create_db(db_name, slices)
        else:
            cur_db = chromadb.load(f"{db_name}.chroma")
            for slice in slices:
                embedding = slice['embedding']
                del slice['embedding']            
                cur_db.add(embedding, metadata=slice)
            cur_db.save(f"{db_name}.chroma")
        return  "slices added finished!"
    
    def do_query(self, db_name, query_vector, topk=20):
        used_db = chromadb.load(f"{db_name}.chroma")
        results = used_db.query(query_vector, topk=topk)
        return results
    

def ut():
    test_client = ChromadbClient()
    slices = [
        {'id': '1', 'embedding': [0.1, 0.2, 0.3], 'label': 'cat', 'metadata': 'image of a cat'},
        {'id': '2', 'embedding': [0.4, 0.5, 0.6], 'label': 'dog', 'metadata': 'image of a dog'},
        {'id': '3', 'embedding': [0.7, 0.8, 0.9], 'label': 'bird', 'metadata': 'image of a bird'}
    ]
    res = test_client.collection_add_slice("testdb", slices)

    print(res)
# ut()