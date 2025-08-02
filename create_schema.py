import weaviate
from weaviate.connect import ConnectionParams
from weaviate.collections.classes.config import Property, DataType

# Connection parameters
connection_params = ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
client = weaviate.WeaviateClient(connection_params)
client.connect()  # <-- ဒီလို connect() ခေါ်ရန်လိုပါတယ်။

# Schema define
client.collections.create(
    name="PaliChunk",
    properties=[
        Property(name="chunk_id", data_type=DataType.TEXT),
        Property(name="pali_text", data_type=DataType.TEXT),
        Property(name="source_reference", data_type=DataType.TEXT),
    ],
    description="Pali Tipitaka text chunks and their references"
)

print("Schema/Class 'PaliChunk' ကို အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။")
client.close()