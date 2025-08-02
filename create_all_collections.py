import weaviate
from weaviate.connect import ConnectionParams
from weaviate.collections.classes.config import Property, DataType

collection_names = [
    "TiVin", "TiDNMNSN", "TiANKNVin", "TiAbh",
    "MuVin", "MuSNAN", "MuKN", "MuDNMN", "MuAbh",
    "AtKNcVinAbh", "AtKNb", "AtKNa", "AtDNMNSNAN",
    "AnVisSangLedi", "AnVanVamBySihala"
]

connection_params = ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
client = weaviate.WeaviateClient(connection_params)
client.connect()

for cname in collection_names:
    try:
        client.collections.create(
            name=cname,
            properties=[
                Property(name="chunk_id", data_type=DataType.TEXT),
                Property(name="pali_text", data_type=DataType.TEXT),
                # ဗဟုသုတလိုရင် Property(name="other_field", data_type=DataType.TEXT), ...
            ],
            description=f"{cname} Tipitaka text chunks and their references",
            vectorizer_config=None   # 🟢 external vectors, so don't use internal vectorizer
        )
        print(f"✅ Created collection: {cname}")
    except Exception as e:
        print(f"⚠️  {cname}: {e}")

client.close()
