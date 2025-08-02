import weaviate
from weaviate.connect import ConnectionParams
from sentence_transformers import SentenceTransformer

# (၁) Query encode
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
query = input("Search (Unicode/Pali/Myanmar/English): ").strip()
query_vector = model.encode(query).tolist()

# (၂) Weaviate client
connection_params = ConnectionParams.from_url("http://localhost:8080", grpc_port=50051)
client = weaviate.WeaviateClient(connection_params)
client.connect()

# (၃) Collection name detection (for all modern weaviate-py versions)
collections_info = client.collections.list_all()
# collections_info is probably a list of dicts: [{'name': 'TiVin', ...}, ...]
# Let's debug print it if not sure:
if isinstance(collections_info, dict):
    # Very old format: {'collections': [ ... ]}
    collection_names = [col['name'] for col in collections_info['collections']]
else:
    # Modern: just a list of collection dicts
    collection_names = [col['name'] for col in collections_info]

print("\n========= 🔍 Searching in all collections =========\n")

for cname in collection_names:
    try:
        collection = client.collections.get(cname)
        # Count objects (debug)
        try:
            obj_count = collection.aggregate().count
        except Exception:
            obj_count = "?"
        print(f"===== [Collection: {cname}] (objects: {obj_count}) =====")
        
        # Vector search
        try:
            results = collection.query.near_vector(
                query_vector,  # vector as positional argument
                limit=3
            )
        except Exception as e:
            print(f"  ⚠️ Search API error: {e}")
            print("--------------------------------------------------")
            continue
        
        # API version compatibility
        objs = getattr(results, "objects", None)
        if objs is None:
            # Maybe dict/other
            objs = getattr(results, "data", None)
            if objs is None and isinstance(results, dict):
                objs = results.get("objects")
        if not objs:
            print("  ❗ No results found.")
        else:
            for idx, obj in enumerate(objs, 1):
                props = getattr(obj, "properties", obj)
                print(f"({idx}) chunk_id: {props.get('chunk_id','')}")
                text = props.get('pali_text', '') or props.get('text', '')
                print(f"    text: {text[:160]}...")
        print("--------------------------------------------------")
    except Exception as e:
        print(f"  ⚠️  Error searching in '{cname}': {e}")
        print("--------------------------------------------------")

client.close()
print("\n✅ Search Complete.")

collections_info = client.collections.list_all()
print(collections_info)   # ဒီလို ထည့်ပါ
