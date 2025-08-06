import pandas as pd
import csv
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

# Load CSV
df = pd.read_csv("MN5_chunk.csv")
chunks = df["pali_text"].tolist()
chunk_ids = df["chunk_id"].tolist()

# Create splitter
splitter = SentenceTransformersTokenTextSplitter(
    tokens_per_chunk=200,
    chunk_overlap=0,
    model_name="sentence-transformers/LaBSE"
)

# Output structure
final_rows = []

for i, chunk in enumerate(chunks):
    main_chunk_id = chunk_ids[i]
    subchunks = splitter.split_text(text=chunk)

    for idx, subchunk in enumerate(subchunks, start=1):
        sentences = [s.strip() + "." for s in subchunk.split(".") if s.strip()]
        for sent in sentences:
            final_rows.append({
                "main_chunk_id": main_chunk_id,
                "sub_chunk_id": f"{main_chunk_id}_{idx}",
                "sentence": sent
            })

# Export CSV
output_file = "MN5_chunk_subchunk_sentences_langchain.csv"
pd.DataFrame(final_rows).to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
print(f"✅ LangChain Splitter DONE. Output saved to: {output_file}")
