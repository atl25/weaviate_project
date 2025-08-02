import pandas as pd
import ast
from sentence_transformers import SentenceTransformer

df = pd.read_csv("test_with_vectors.csv")
df["vector"] = df["vector"].apply(ast.literal_eval)

# (1) vector တူမတူစစ်
print("Unique vectors:", len(set([tuple(v) for v in df["vector"]])))
print("Total rows:", len(df))

# (2) query encode
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
query = input("Search (Unicode/Pali/Myanmar/English): ").strip()
query_vector = model.encode(query).tolist()

# (3) weaviate client
import weaviate
from weaviate.connect import ConnectionParams
connection_params = ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
client = weaviate.WeaviateClient(connection_params)
client.connect()

collection = client.collections.get("PaliChunk")
results = collection.query.near_vector(
    query_vector,
    limit=5  # Result ၅ ခုသာပြ
)
for idx, obj in enumerate(results.objects, 1):
    print(f"({idx}) chunk_id: {obj.properties['chunk_id']}")
    print(f"    pali_text: {obj.properties['pali_text'][:120]}...")
    print("--------------------------------------------------")

client.close()
