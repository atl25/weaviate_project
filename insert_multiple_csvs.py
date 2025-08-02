import weaviate
from weaviate.connect import ConnectionParams
import pandas as pd
import ast

# Weaviate client ချိတ်
connection_params = ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
client = weaviate.WeaviateClient(connection_params)
client.connect()

# CSV ဖိုင်စာရင်း
csv_files = [
    "TiVin_with_vectors.csv",
    "TiDNMNSN_with_vectors.csv",
    "TiANKNVin_with_vectors.csv",
    "TiAbh_with_vectors.csv",
    "MuVin_with_vectors.csv",
    "MuSNAN_with_vectors.csv",
    "MuKN_with_vectors.csv",
    "MuDNMN_with_vectors.csv",
    "MuAbh_with_vectors.csv",
    "AtKNcVinAbh_with_vectors.csv",
    "AtKNb_with_vectors.csv",
    "AtKNa_with_vectors.csv",
    "AtDNMNSNAN_with_vectors.csv",
    "AnVisSangLedi_with_vectors.csv",
    "AnVanVamBySihala_with_vectors.csv"
]

collection = client.collections.get("PaliChunk")

for filename in csv_files:
    print(f"Loading {filename} ...")
    df = pd.read_csv(filename)
    # vector column ကို string => list ပြန်ပြောင်း
    df["vector"] = df["vector"].apply(ast.literal_eval)
    for idx, row in df.iterrows():
        props = {
            "chunk_id": str(row['chunk_id']),
            "pali_text": str(row['pali_text']),
            # အခြား field လိုရင် ဒီမှာ ထပ်ထည့်
        }
        collection.data.insert(properties=props, vector=row["vector"])
    print(f"Inserted: {filename}")

client.close()
print("All files imported!")
