import weaviate
import pandas as pd
import ast
from weaviate.connect import ConnectionParams
from weaviate.collections.classes.config import Property, DataType

# Step 1: Connect to Weaviate
connection_params = ConnectionParams.from_url("http://localhost:8081", grpc_port=50052)
client = weaviate.WeaviateClient(connection_params)
client.connect()

# Step 2: Create a new collection/class for LaBSE vectors
try:
    client.collections.create(
        name="LaBSEChunk",
        properties=[
            Property(name="main_chunk_id", data_type=DataType.TEXT),
            Property(name="sub_chunk_id", data_type=DataType.TEXT),
            Property(name="text", data_type=DataType.TEXT),
        ],
        description="Chunks with LaBSE vectors",
        vectorizer_config=None
    )
    print("✅ Created new collection: LaBSEChunk")
except Exception as e:
    print(f"⚠️ Collection creation skipped or failed: {e}")

# Step 3: Read and prepare data from CSV
df = pd.read_csv("vectorized_chunks_labse.csv")
df.columns = df.columns.str.strip()  # <- Fix for whitespace column names
df["embedding"] = df["embedding"].apply(ast.literal_eval)

# Step 4: Insert data into Weaviate
collection = client.collections.get("LaBSEChunk")

for idx, row in df.iterrows():
    collection.data.insert(
        properties={
            "main_chunk_id": str(row["main_chunk_id"]),
            "sub_chunk_id": str(row["sub_chunk_id"]),
            "text": str(row["text"])
        },
        vector=row["vector"]
    )
    if idx % 100 == 0:
        print(f"🔄 Inserted {idx} records...")

print("✅ All LaBSE vectors inserted into Weaviate.")
client.close()
