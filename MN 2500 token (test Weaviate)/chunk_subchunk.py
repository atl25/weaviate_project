import pandas as pd
from sentence_transformers import SentenceTransformer
import csv

# Load tokenizer model
model = SentenceTransformer("sentence-transformers/LaBSE")

def count_tokens(text):
    """Return number of tokens using model tokenizer"""
    return len(model.tokenizer.encode(text, add_special_tokens=False))

# Read source chunk file
df = pd.read_csv("MN5_chunk.csv")
chunks = df["pali_text"].tolist()
chunk_ids = df["chunk_id"].tolist()

# Prepare output
output_rows = []

for i, chunk in enumerate(chunks):
    main_chunk_id = chunk_ids[i]
    if not isinstance(chunk, str) or not chunk.strip():
        continue  # skip empty or non-string chunks

    words = chunk.strip().split()
    current_tokens = []
    token_count = 0
    subchunk_index = 1

    for word in words:
        word_token_len = count_tokens(word)
        if token_count + word_token_len <= 200:
            current_tokens.append(word)
            token_count += word_token_len
        else:
            subchunk_text = " ".join(current_tokens)
            output_rows.append({
                "main_chunk_id": main_chunk_id,
                "sub_chunk_id": f"{main_chunk_id}_{subchunk_index}",
                "text": subchunk_text
            })
            subchunk_index += 1
            current_tokens = [word]
            token_count = word_token_len

    # Add last subchunk
    if current_tokens:
        subchunk_text = " ".join(current_tokens)
        output_rows.append({
            "main_chunk_id": main_chunk_id,
            "sub_chunk_id": f"{main_chunk_id}_{subchunk_index}",
            "text": subchunk_text
        })

# Write to new CSV
output_file = "MN5_chunk_subchunks_only.csv"
pd.DataFrame(output_rows).to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

print(f"✅ Done. Output saved to: {output_file}")
