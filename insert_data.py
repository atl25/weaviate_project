import weaviate
import pandas as pd
import ast
from weaviate.connect import ConnectionParams

connection_params = ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
client = weaviate.WeaviateClient(connection_params)
client.connect()

df = pd.read_csv("test_with_vectors.csv")

for idx, row in df.iterrows():
    vector = ast.literal_eval(row['vector']) if isinstance(row['vector'], str) else row['vector']

    client.collections.get("PaliChunk").data.insert(
        properties={
            "chunk_id": str(row['chunk_id']),
            "pali_text": str(row['pali_text'])
        },
        vector=vector
    )

    if idx % 100 == 0:
        print(f"{idx} records uploaded...")

print("CSV data အကုန် Weaviate ထဲသို့ တင်ပြီးပါပြီ။")
client.close()
