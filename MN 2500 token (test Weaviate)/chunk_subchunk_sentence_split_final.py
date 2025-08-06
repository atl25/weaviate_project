import pandas as pd
import csv
from sentence_transformers import SentenceTransformer

# Load LaBSE model
model = SentenceTransformer("sentence-transformers/LaBSE")

def count_tokens(text):
    return len(model.tokenizer.encode(text, add_special_tokens=False))

# Load the chunk CSV
df = pd.read_csv("MN5_chunk.csv")

chunks = df["pali_text"].tolist()
chunk_ids = df["chunk_id"].tolist()

final_rows = []

for i, chunk in enumerate(chunks):
    main_chunk_id = chunk_ids[i]

    # Skip if chunk is NaN or not string
    if not isinstance(chunk, str) or not chunk.strip():
        continue

    # Split sentences by "." and reattach "." for each
    sentences = [s.strip() + "." for s in chunk.split(".") if s.strip()]

    subchunk_sentences = []
    subchunk_token_count = 0
    subchunk_index = 1

    for sentence in sentences:
        token_count = count_tokens(sentence)

        if subchunk_token_count + token_count <= 200:
            subchunk_sentences.append(sentence)
            subchunk_token_count += token_count
        else:
            for s in subchunk_sentences:
                final_rows.append({
                    "main_chunk_id": main_chunk_id,
                    "sub_chunk_id": f"{main_chunk_id}_{subchunk_index}",
                    "sentence": s
                })
            subchunk_index += 1
            subchunk_sentences = [sentence]
            subchunk_token_count = token_count

    if subchunk_sentences:
        for s in subchunk_sentences:
            final_rows.append({
                "main_chunk_id": main_chunk_id,
                "sub_chunk_id": f"{main_chunk_id}_{subchunk_index}",
                "sentence": s
            })

# Export final CSV
output_file = "MN5_chunk_subchunk_sentences_final.csv"
pd.DataFrame(final_rows).to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

print(f"✅ DONE: Output saved to {output_file}")
