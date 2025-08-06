import pandas as pd
from sentence_transformers import SentenceTransformer
import csv

# CSV input file
input_file = "MN5_chunk.csv"
df = pd.read_csv(input_file)
chunks = df["pali_text"].dropna().tolist()
chunk_ids = df["chunk_id"].dropna().tolist()

# Load LaBSE model
model = SentenceTransformer("sentence-transformers/LaBSE")

# Token counting function
def count_tokens(text):
    return len(model.tokenizer.encode(text, add_special_tokens=False))

# Final output rows
final_rows = []

for i, chunk in enumerate(chunks):
    main_chunk_id = chunk_ids[i]

    # Step 1: Get sentences using '.'
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
            # save current subchunk
            for s in subchunk_sentences:
                final_rows.append({
                    "main_chunk_id": main_chunk_id,
                    "sub_chunk_id": f"{main_chunk_id}_{subchunk_index}",
                    "sentence": s
                })
            subchunk_index += 1
            subchunk_sentences = [sentence]
            subchunk_token_count = token_count

    # handle last subchunk
    if subchunk_sentences:
        for s in subchunk_sentences:
            final_rows.append({
                "main_chunk_id": main_chunk_id,
                "sub_chunk_id": f"{main_chunk_id}_{subchunk_index}",
                "sentence": s
            })

# Save output
output_file = "MN5_chunk_subchunk_sentences.csv"
pd.DataFrame(final_rows).to_csv(output_file, index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
print(f"✅ Done! Output saved to {output_file}")
